import os
import uuid
from django.conf import settings
from django.http import FileResponse
from django.core.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import UnsupportedMediaType

from .serializers import (
    EntitySerializer,
    ActSerializer,
    OcurrencyEntitySerializer,
    EntSerializer,
    LearningModelSerializer,
)
from .models import Entity, Act, OcurrencyEntity, LearningModel
from .exceptions import nameTooLong

from .utils_spacy import get_all_entity_ner, get_risk
from .utils_oodocument import (
    anonimyzed_text,
    generate_data_for_anonymization,
    convert_document_to_format,
    extract_text_from_file,
    anonimyzed_convert_document,
)
from .utils_publicador import publish_document
from .utils import check_exist_act, open_file, calculate_ents_anonimyzed
from .exceptions import ActFileNotFound

# Para usar Python Template de string
ANON_REPLACE_TPL = "<$name>"
# Color de fondo para texto anonimizado
ANON_FONT_BACK_COLOR = [255, 255, 0]


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def create(self, request):
        new_file = request.FILES.get("file", False)
        if new_file is False:
            raise ActFileNotFound()
        output_path = settings.MEDIA_ROOT_TEMP_FILES + "output.txt" + str(uuid.uuid4())
        # Creo el acta base
        new_act = Act(file=new_file)
        try:
            new_act.full_clean()
        except (ValidationError):
            raise UnsupportedMediaType(media_type=new_file.content_type, detail=settings.ERROR_TEXT_FILE_TYPE)
        except (nameTooLong):
            raise nameTooLong()
        else:
            new_act.save()
        # Transformo el docx,en txt
        convert_document_to_format(new_act.file.path, output_path, "txt")
        # Guardo el texto en la instancia
        new_act.text = extract_text_from_file(output_path)
        new_act.save()
        # Analizo el texto
        ents = get_all_entity_ner(new_act.text)
        ocurrency_list = EntSerializer(ents, many=True)
        # Una vez procesado,guardar la info
        dataReturn = {
            "text": new_act.text,
            "ents": ocurrency_list.data,
            "id": new_act.id,
        }
        os.remove(output_path)
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
        act_check = check_exist_act(pk)
        new_ents = request.data.get("ents")
        ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
        all_query = list()
        if ocurrency_query.exists():
            ocurrency_query.delete()
        # Recorrido sobre las ents nuevas
        for ent in new_ents:
            # Chequeo por un flujo que me puede llegar entitades del front sin datos
            if ent["start"] is not None and ent["end"] is not None:
                ocurrency = OcurrencyEntity.objects.create(
                    act=act_check,
                    startIndex=ent["start"],
                    endIndex=ent["end"],
                    entity=Entity.objects.get(name=ent["tag"]),
                    should_anonymized=ent["should_anonymized"],
                )
                all_query.append(ocurrency)
        # Definicion de rutas
        output_text = settings.MEDIA_ROOT_TEMP_FILES + "anonymous.txt" + str(uuid.uuid4())
        output_format = act_check.filename()
        extension = os.path.splitext(output_format)[1][1:]
        # Generar el archivo en formato de entrada anonimizado
        anonimyzed_convert_document(
            act_check.file.path,
            settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + output_format,
            extension,
            generate_data_for_anonymization(all_query, act_check.text, ANON_REPLACE_TPL),
            output_text,
            "txt",
            ANON_FONT_BACK_COLOR,
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
        # Construyo el response
        dataReturn = {
            "anonymous_text": read_result,
            "data_visualization": {
                "entitiesResult": calculate_ents_anonimyzed(all_query),
                "total": {"name": "Cantidad de Entidades totales", "value": len(all_query)},
                "risk": get_risk(len(all_query)),
                "efectivity_average": 85,
            },
        }
        return Response(dataReturn)

    @action(methods=["get"], detail=True)
    def getAnonymousDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        dataResponse = open_file(settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + act_check.filename())
        return FileResponse(dataResponse, as_attachment=True)

    @action(methods=["post"], detail=True)
    def publishDocument(self, request, pk=None):
        act_check = check_exist_act(pk)
        publish_document(
            act_check.file.path,
            settings.LIBERAJUS_CLOUDFOLDER_STORE,
            settings.LIBERAJUS_CLOUD_STORAGE_PROVIDER,
        )
        dataResponse = {
            "status": "Ok",
            "text": "Se publico en  {}".format(settings.LIBERAJUS_CLOUD_STORAGE_PROVIDER),
        }
        return Response(data=dataResponse)

    @action(methods=["post"], detail=True)
    def publishDocumentInDrive(self, request, pk=None):
        act_check = check_exist_act(pk)
        publish_document(
            act_check.file.path,
            settings.LIBERAJUS_CLOUDFOLDER_STORE,
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


class LearningModelViewSet(viewsets.ModelViewSet):
    queryset = LearningModel.objects.all()
    serializer_class = LearningModelSerializer

    @action(methods=["post"], detail=True)
    def useSubject(self, request, pk=None):
        select_model = LearningModel.objects.get(id=pk)
        ## Aca va estar la logica que cambie el modelo-a futuro-
        return Response(data="Se ha elegido la materia {}".format(select_model.name_subject))
