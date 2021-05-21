import os
import uuid
import ast
import logging
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

from .tasks import train_model
from .utils.spacy import write_model_test_in_file
from .utils.oodocument import (
    generate_data_for_anonymization,
    convert_document_to_format,
    extract_text_from_file,
    anonimyzed_convert_document,
    extract_header,
    convert_offset_header_to_cursor,
)

from .utils.publicador import publish_document
from .utils.general import (
    check_exist_act,
    open_file,
    extraer_datos_de_ocurrencias,
    check_delete_ocurrencies,
    check_add_annotations_request,
    check_new_ocurrencies,
)
from .utils.data_visualization import generate_data_visualization

from .utils.vistas import (
    timeit_save_stats, 
    create_act, detect_entities, 
    find_all_ocurrencies, 
    format_spans, 
    set_initial_review_time, 
    calculate_and_set_elapsed_review_time
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
        new_file = request.FILES.get("file", False)
        # Persists a document
        act = create_act(new_file)
        # Traigo todas las entidades para hacer busquedas mas rapida
        entities = Entity.objects.all()
        timeit_detect_ents = timeit_save_stats(act, "detection_time")(detect_entities)
        ocurrencies = timeit_detect_ents(act)
        # Se crean las nuevas ocurrencias identificadas por el modelo
        self.create_new_occurrencies(ocurrencies, act, False, entities)
        ents = EntSerializer(OcurrencyEntity.objects.filter(act=act.id), many=True)

        data = {
            "text": act.text,
            "ents": ents.data,
            "id": act.id,
        }

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
        # Traigo todas las entidades para hacer busquedas mas rapida
        entities = Entity.objects.all()
        # Se crean las nuevas entidades marcadas por usuarix
        self.create_new_occurrencies(new_ents, act_check, True, entities)
        # Actualización de ocurrencias eliminadas por usuarix
        self.delete_ocurrencies(delete_ents, act_check)
        # Definicion de rutas
        output_text = settings.MEDIA_ROOT_TEMP_FILES + "anonymous.txt" + str(uuid.uuid4())
        output_format = act_check.filename()
        extension = os.path.splitext(output_format)[1][1:]
        # Todas las ocurrencias actualizadas para el texto
        all_query = list(OcurrencyEntity.objects.filter(act=act_check))
        # Generar el archivo en formato de entrada anonimizado
        timeit_anonimyzation = timeit_save_stats(act_check, "anonymization_time")(anonimyzed_convert_document)
        timeit_anonimyzation(
            act_check.file.path,
            settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + output_format,
            extension,
            generate_data_for_anonymization(all_query, act_check.text, ANON_REPLACE_TPL, act_check.offset_header),
            output_text,
            "txt",
            ANON_FONT_BACK_COLOR,
            convert_offset_header_to_cursor(act_check.offset_header),
        )
        # Generar el archivo para poder extraer el texto
        # convert_document_to_format(settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + output_format, output_text, "txt")
        # Leo el archivo anonimizado
        read_result = extract_text_from_file(output_text)
        # Borrado de archivo auxiliares
        os.remove(output_text)
        os.remove(act_check.file.path)
        # Guardado del archivo anonimizado
        act_check.file = settings.PRIVATE_STORAGE_ANONYMOUS_URL + output_format

        timeit_extract = timeit_save_stats(act_check, "extraction_time")(extraer_datos_de_ocurrencias)
        timeit_extract(all_query)
        act_check.save()

        # Construyo el response
        dataReturn = {
            "anonymous_text": read_result,
            "data_visualization": generate_data_visualization(all_query, act_check),
        }
        return Response(dataReturn)

    def create_new_occurrencies(self, ocurrencies, act, human_mark, entity_list=[]):
        ocurrencies_to_create = []
        for ocurrency in ocurrencies:
            entity = entity_list.get(name=ocurrency["tag"])
            ocurrencies_to_create.append(
                OcurrencyEntity(
                    act=act,
                    startIndex=ocurrency["start"],
                    endIndex=ocurrency["end"],
                    entity=entity,
                    should_anonymized=entity.should_anonimyzation,
                    human_marked_ocurrency=human_mark,
                    text=act.text[ocurrency["start"] : ocurrency["end"]],
                )
            )
        OcurrencyEntity.objects.bulk_create(ocurrencies_to_create)

    def delete_and_save(self, ocurrency):
        ocurrency.human_deleted_ocurrency = True
        ocurrency.save()

    def delete_ocurrencies(self, ocurrencies, act_check):
        ocurrencies_ids = [ocur["id"] for ocur in ocurrencies]
        ocurrencies_to_delete = OcurrencyEntity.objects.filter(id__in=ocurrencies_ids, act_id=act_check.id)
        list(map(self.delete_and_save, ocurrencies_to_delete))

    @action(methods=["post"], detail=True)
    def addAllOccurrencies(self, request, pk=None):
        entities = Entity.objects.all()
        act_check = check_exist_act(pk)
        new_ents = check_new_ocurrencies(
            request.data.get("newOcurrencies"), list(entities.values_list("name", flat=True)), act_check
        )
        # Ocurrencias para marcar eliminadas
        deleted_ents = check_delete_ocurrencies(request.data.get("deleteOcurrencies"))
        entity_list_for_multiple_selection = request.data.get("entityList")
        # Se crean las nuevas entidades marcadas por usuarix
        self.create_new_occurrencies(new_ents, act_check, True, entities)
        # Actualización de ocurrencias eliminadas por usuarix
        self.delete_ocurrencies(deleted_ents, act_check)
        # Busco todas las ocurrencias en db
        all_ocurrencies_query = OcurrencyEntity.objects.filter(human_deleted_ocurrency=False, act=act_check)
        # Busco todas las multiples apariciones de las ocurrencias filtradas por el listado de tags
        # Logueo el tiempo de este proceso
        timeit_new_ocurrencies = timeit_save_stats(act_check, "find_all_ocurrencies")(find_all_ocurrencies)
        new_occurencies = timeit_new_ocurrencies(
            act_check.text, all_ocurrencies_query, entity_list_for_multiple_selection
        )
        # Creo las nuevas ocurrencias encontradas a través de la búsqueda
        self.create_new_occurrencies(new_occurencies, act_check, True, entities)
        result = EntSerializer(OcurrencyEntity.objects.filter(human_deleted_ocurrency=False, act=act_check), many=True)
        dataReturn = {
            "text": act_check.text,
            "ents": result.data,
            "id": act_check.id,
        }
        return Response(dataReturn)

    @action(methods=["get"], detail=True)
    def getAnonymousDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        dataResponse = open_file(settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + act_check.filename(), "rb")
        return FileResponse(dataResponse, as_attachment=True)

    @action(methods=["post"], detail=True)
    def publishDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        publish_document(
            act_check.file.path,
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
            act_check.file.path,
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
