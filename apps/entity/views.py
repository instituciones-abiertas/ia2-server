import os
import uuid
import ast
import logging
from time import time
from django.conf import settings
from django.http import FileResponse
from django.db.models import Q

from rest_framework import mixins, parsers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .serializers import (
    EntitySerializer,
    ActSerializer,
    OcurrencyEntitySerializer,
    EntSerializer,
    LearningModelSerializer,
)
from .models import Entity, Act, OcurrencyEntity, LearningModel

from .tasks import train_model, extraer_datos_de_ocurrencias
from celery.result import AsyncResult


from .utils.spacy import write_model_test_in_file, Nlp

from .utils.oodocument import (
    generate_data_for_anonymization,
    convert_document_to_format,
    extract_text_from_file,
    extract_header,
    convert_offset_header_to_cursor,
)

from .utils.publicador import publish_document
from .utils.general import (
    check_exist_act,
    open_file,
    # extraer_datos_de_ocurrencias,
    check_delete_ocurrencies,
    check_add_annotations_request,
    check_new_ocurrencies,
    check_exist_and_type_field,
    check_request_params,
    calculate_hash,
)
from .utils.data_visualization import generate_data_visualization
from .utils.vistas import (
    timeit_save_stats,
    detect_entities,
    find_all_ocurrencies,
    format_spans,
    set_initial_review_time,
    calculate_and_set_elapsed_review_time,
    create_new_occurrencies,
    delete_ocurrencies,
    add_entities_by_multiple_selection,
    save_act_stats,
    extraccion_de_datos,
    anonimizacion_de_documentos,
    detect_and_create_ocurrencies,
    create_proto_act,
    remove_anonymus_previous_file,
)

# Para usar Python Template de string
ANON_REPLACE_TPL = "<$name>"
# Color de fondo para texto anonimizado
ANON_FONT_BACK_COLOR = [255, 255, 0]
# Entidades a no mostrar


# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False)
    def retrain(self, request):
        r = train_model.apply_async()

        print("Responses")
        print(r)
        print(r.get())

        return Response({"status": "ok"})

    def list(self, request):
        queryset = Entity.objects.all()
        for ent_name in settings.DISABLED_ENTITIES:
            queryset = queryset.exclude(name=ent_name)
        queryset = queryset.order_by("name")
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)


class CreateActMixin(mixins.CreateModelMixin):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        new_act = False
        new_file = request.FILES.get("file", False)
        act = create_proto_act(new_file)
        generate_hash = calculate_hash(act.text)
        exist_act = Act.objects.filter(hash_text=generate_hash)
        if exist_act.exists():
            act = exist_act[0]  # Access a unique option
            ents = EntSerializer(OcurrencyEntity.objects.filter(act=act.id, human_deleted_ocurrency=False), many=True)

        else:
            act.hash_text = generate_hash
            act.save()
            all_entities = Entity.objects.all()
            detect_and_create_ocurrencies(act, all_entities, act_id=act.id, key="detection_time")
            ents = EntSerializer(OcurrencyEntity.objects.filter(act=act.id), many=True)
            new_act = True

        data = {"text": act.text, "ents": ents.data, "id": act.id, "new_act": new_act}

        set_initial_review_time(act)
        return Response(data, status=status.HTTP_201_CREATED)


class ActViewSet(CreateActMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=True)
    def addAnnotations(self, request, pk=None):
        # Traigo todas las entidades para hacer busquedas mas rapida
        entities = Entity.objects.all()
        request_check = check_add_annotations_request(request.data)
        act_check = check_exist_act(pk)

        calculate_and_set_elapsed_review_time(act_check)

        # Ocurrencias marcadas por humanx,se provee el nombre de todas las entidades
        new_ents = check_new_ocurrencies(
            request_check.get("newOcurrencies"), list(entities.values_list("name", flat=True)), act_check
        )
        # Ocurrencias para marcar eliminadas
        delete_ents = check_delete_ocurrencies(request_check.get("deleteOcurrencies"))
        # Se crean las nuevas entidades marcadas por usuarix
        create_new_occurrencies(new_ents, act_check, True, entities)
        # Actualización de ocurrencias eliminadas por usuarix
        delete_ocurrencies(delete_ents, act_check)
        # Definicion de rutas
        output_format = act_check.filename()
        extension = os.path.splitext(output_format)[1][1:]
        # Todas las ocurrencias actualizadas para el texto
        all_query = list(OcurrencyEntity.objects.filter(act=act_check))
        # Generar el archivo en formato de entrada anonimizado
        task = anonimizacion_de_documentos(
            act_check.file.path,
            settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + output_format,
            extension,
            generate_data_for_anonymization(all_query, act_check.text, ANON_REPLACE_TPL, act_check.offset_header),
            ANON_FONT_BACK_COLOR,
            convert_offset_header_to_cursor(act_check.offset_header),
            act_id=act_check.id,
            key="anonymization_time",
        )
        # TODO Pasar la logica de actualización de modelo a tarea asincronica
        remove_anonymus_previous_file(act_check, settings.PRIVATE_STORAGE_ANONYMOUS_URL + output_format)

        extraccion_de_datos([act_check.id], act_id=act_check.id, key="extraction_time")

        # Construyo el response
        dataReturn = {
            "data_visualization": generate_data_visualization(all_query, act_check),
            "task_id": task.id,
        }
        return Response(dataReturn)

    def add_entities(self, request, act_check, entities):
        new_ents = check_new_ocurrencies(
            request.data.get("newOcurrencies"), list(entities.values_list("name", flat=True)), act_check
        )
        create_new_occurrencies(new_ents, act_check, True, entities)

    def delete_entities(self, request, act_check):
        deleted_ents = check_delete_ocurrencies(request.data.get("deleteOcurrencies"))
        # Actualización de ocurrencias eliminadas por usuarix
        delete_ocurrencies(deleted_ents, act_check)

    @action(methods=["post"], detail=True)
    def addAllOccurrencies(self, request, pk=None):
        all_entities = Entity.objects.all()
        act_check = check_exist_act(pk)

        self.add_entities(request, act_check, all_entities)
        self.delete_entities(request, act_check)

        nlp = Nlp()
        doc = nlp.generate_doc(act_check.text)
        entity_list_for_multiple_selection = request.data.get("entityList")

        add_entities_by_multiple_selection(
            entity_list_for_multiple_selection,
            act_check,
            doc,
            all_entities,
            True,
            act_id=act_check.id,
            key="find_all_ocurrencies",
        )
        result = EntSerializer(OcurrencyEntity.objects.filter(human_deleted_ocurrency=False, act=act_check), many=True)
        dataReturn = {
            "text": act_check.text,
            "ents": result.data,
            "id": act_check.id,
            "new_act": True,  # TODO HOTFIX
        }

        return Response(dataReturn)

    @action(methods=["get"], detail=True)
    def getStatusDocument(self, request, pk=None):
        task_id = check_exist_and_type_field(request.query_params.dict(), "taskid", str)
        status_task = AsyncResult(task_id).successful()
        return Response({"status": status_task})

    @action(methods=["get"], detail=True)
    def getAnonymousDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        task_id = check_exist_and_type_field(request.query_params.dict(), "taskid", str)
        if AsyncResult(task_id).successful():
            dataResponse = open_file(settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + act_check.filename(), "rb", None)
            return FileResponse(dataResponse, as_attachment=True)
        else:
            return Response(
                data=f"Se esta procesando el archivo del acta {act_check.id}, espere unos segundos", status=409
            )

    @action(methods=["post"], detail=True)
    def publishDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        publish_document(
            act_check.anonymous_file.path,
            settings.PUBLICADOR_CLOUDFOLDER_STORE,
            settings.PUBLICADOR_CLOUD_STORAGE_PROVIDER,
        )
        dataResponse = {
            "status": "Ok",
            "text": "Se publico en  {}".format(settings.PUBLICADOR_CLOUD_STORAGE_PROVIDER),
        }
        return Response(data=dataResponse)

    @action(methods=["post"], detail=True)
    def publishDocumentInDrive(self, request, pk=None):
        act_check = check_exist_act(pk)
        publish_document(
            act_check.anonymous_file.path,
            settings.PUBLICADOR_CLOUDFOLDER_STORE,
            "drive",
        )
        dataResponse = {
            "status": "Ok",
            "text": "Se publico en  {}".format("drive"),
        }
        return Response(data=dataResponse)


class OcurrencyEntityViewSet(viewsets.ModelViewSet):
    queryset = OcurrencyEntity.objects.all()
    serializer_class = OcurrencyEntitySerializer
    permission_classes = [IsAuthenticated]


class LearningModelViewSet(viewsets.ModelViewSet):
    queryset = LearningModel.objects.all()
    serializer_class = LearningModelSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=True)
    def useSubject(self, request, pk=None):
        select_model = LearningModel.objects.get(id=pk)
        ## Aca va estar la logica que cambie el modelo-a futuro-
        return Response(data="Se ha elegido la materia {}".format(select_model.name_subject))
