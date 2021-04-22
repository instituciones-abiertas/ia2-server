import os
import uuid
import ast
import logging
from django.conf import settings
from django.http import FileResponse
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    EntitySerializer,
    ActSerializer,
    OcurrencyEntitySerializer,
    EntSerializer,
    LearningModelSerializer,
)
from .models import Entity, Act, OcurrencyEntity, LearningModel

from .tasks import train_model
from .utils.spacy import write_model_test_in_file, find_all_entity_ocurrencies, filter_ents
from .utils.oodocument import (
    generate_data_for_anonymization,
    convert_document_to_format,
    extract_text_from_file,
    anonimyzed_convert_document,
    extract_header,
    convert_offset_header_to_cursor,
)

from .utils.publicador import publish_document
from .utils.general import check_exist_act, open_file, extraer_datos_de_ocurrencias, filter_spans
from .utils.data_visualization import generate_data_visualization
from .utils.vistas import timeit_save_stats, create_act, detect_entities

# Para usar Python Template de string
ANON_REPLACE_TPL = "<$name>"
# Color de fondo para texto anonimizado
ANON_FONT_BACK_COLOR = [255, 255, 0]
# Entidades a no mostrar
DISABLE_ENTITIES = settings.IA2_DISABLED_ENTITIES


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
        if DISABLE_ENTITIES:
            for ent in ast.literal_eval(DISABLE_ENTITIES):
                queryset = queryset.exclude(name=ent)
        queryset = queryset.order_by("name")
        serializer = EntitySerializer(queryset, many=True)
        return Response(serializer.data)


class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        new_file = request.FILES.get("file", False)
        act = create_act(new_file)

        timeit_detect_ents = timeit_save_stats(act, "detection_time")(detect_entities)
        ocurrencies = timeit_detect_ents(act)
        ents = EntSerializer(ocurrencies, many=True)

        dataReturn = {
            "text": act.text,
            "ents": ents.data,
            "id": act.id,
        }

        return Response(dataReturn)

    def update(self, request, pk):
        act_check = check_exist_act(pk)
        ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
        if ocurrency_query.exists():
            ocurrency_query.delete()
        new_ents = request.data.get("ents")
        for ent in new_ents:
            OcurrencyEntity.objects.create(
                act=act_check,
                startIndex=ent["start"],
                endIndex=ent["end"],
                entity=Entity.objects.get(name=ent["tag"]),
                should_anonymized=ent["should_anonymized"],
            )

        return Response()

    @action(methods=["post"], detail=True)
    def addAnnotations(self, request, pk=None):
        print("act")
        print(pk)
        act_check = check_exist_act(pk)
        # Ocurrencias marcadas por humanx
        new_ents = request.data.get("newOcurrencies")
        # Ocurrencias para marcar eliminadas
        delete_ents = request.data.get("deleteOcurrencies")
        text = act_check.text
        # Traigo todas las entidades para hacer busquedas mas rapida
        entities = Entity.objects.all()
        # Recorrido sobre las ents nuevas
        for ent in new_ents:
            # Chequeo por un flujo que me puede llegar entitades del front sin datos
            if ent["start"] is not None and ent["end"] is not None:
                entity = entities.get(name=ent["tag"])
                should_be_anonymized = entity.should_anonimyzation
                ocurrency = OcurrencyEntity.objects.create(
                    act=act_check,
                    startIndex=ent["start"],
                    endIndex=ent["end"],
                    entity=Entity.objects.get(name=ent["tag"]),
                    should_anonymized=should_be_anonymized,
                    human_marked_ocurrency=True,
                    text=text[ent["start"] : ent["end"]],
                )
        # Actualización de ocurrencias a borrar
        for ent in delete_ents:
            # Caso que sea eliminada la ocurrencia por accion humana
            ocurrency = OcurrencyEntity.objects.get(id=ent["id"])
            ocurrency.human_deleted_ocurrency = True  # cambio del campo
            ocurrency.save()

        # Definicion de rutas
        output_text = settings.MEDIA_ROOT_TEMP_FILES + "anonymous.txt" + str(uuid.uuid4())
        output_format = act_check.filename()
        extension = os.path.splitext(output_format)[1][1:]
        # Todas las ocurrencias actualizadas para el texto
        all_query = list(OcurrencyEntity.objects.filter(act=act_check))
        print(OcurrencyEntity.objects.filter(act=act_check))
        print(EntSerializer(OcurrencyEntity.objects.filter(act=act_check), many=True))
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
        act_check.save()

        extraer_datos_de_ocurrencias(all_query)

        # Construyo el response
        dataReturn = {
            "anonymous_text": read_result,
            "data_visualization": generate_data_visualization(all_query, act_check),
        }
        return Response(dataReturn)

    @action(methods=["post"], detail=True)
    def addAllOccurrencies(self, request, pk=None):
        act_check = check_exist_act(pk)
        print(act_check)
        # Ocurrencias marcadas por humanx
        new_ents = request.data.get("newOcurrencies")
        # Ocurrencias para marcar eliminadas
        delete_ents = request.data.get("deleteOcurrencies")
        text = act_check.text

        entity_list_for_multiple_selection = request.data.get("entityList")

        entities = Entity.objects.all()
        # Recorrido sobre las ents nuevas
        for ent in new_ents:
            # Chequeo por un flujo que me puede llegar entitades del front sin datos
            if ent["start"] is not None and ent["end"] is not None:
                entity = entities.get(name=ent["tag"])
                should_be_anonymized = entity.should_anonimyzation
                ocurrency = OcurrencyEntity.objects.create(
                    act=act_check,
                    startIndex=ent["start"],
                    endIndex=ent["end"],
                    entity=Entity.objects.get(name=ent["tag"]),
                    should_anonymized=should_be_anonymized,
                    human_marked_ocurrency=True,
                    text=text[ent["start"] : ent["end"]],
                )
        # Actualización de ocurrencias a borrar
        for ent in delete_ents:
            # Caso que sea eliminada la ocurrencia por accion humana
            ocurrency = OcurrencyEntity.objects.get(id=ent["id"])
            ocurrency.human_deleted_ocurrency = True  # cambio del campo
            ocurrency.save()

        # Filtro las ocurrencias cuyo nombre de tag coincide con los de las entidades sobre las que aplicar la funcionalidad de múltiple selección
        # Todas las ocurrencias actualizadas para el texto
        all_query = EntSerializer(
            OcurrencyEntity.objects.filter(
                human_deleted_ocurrency=False, act=act_check, entity__in=entity_list_for_multiple_selection
            ),
            many=True,
        )
        new_filtered_entities = []
        for entity in all_query.data:
            ents = find_all_entity_ocurrencies(text, entity)
            new_filtered_entities = new_filtered_entities + ents

        filtered_ents = filter_ents(new_filtered_entities)
        print("filtered_ents")
        print(filtered_ents)
        # A las nuevas entidades le doy caracter de OcurrencyEntity
        for ent in filtered_ents:
            entity_name = ent.label_
            entity = entities.get(name=entity_name)
            should_be_anonymized = entity.should_anonimyzation
            ocurrency = OcurrencyEntity.objects.create(
                act=act_check,
                startIndex=ent.start_char,
                endIndex=ent.end_char,
                entity=entity,
                should_anonymized=should_be_anonymized,
                human_marked_ocurrency=True,
                text=ent.text,
            )

        result = EntSerializer(OcurrencyEntity.objects.filter(human_deleted_ocurrency=False, act=act_check), many=True)

        dataReturn = {
            "text": text,
            "ents": result.data,
            "id": act_check.id,
        }
        print("result")
        print(result)
        print("result data")
        print(result.data)

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
