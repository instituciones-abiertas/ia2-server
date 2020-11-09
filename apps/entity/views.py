import os,uuid
from django.conf import settings
from django.http import FileResponse

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import UnsupportedMediaType

from .serializers import EntitySerializer, ActSerializer, OcurrencyEntitySerializer, EntSerializer,LearningModelSerializer
from .models import Entity, Act, OcurrencyEntity,LearningModel

from oodocument.oodocument import oodocument
from .utils_spacy import get_all_entity_ner
from .utils_oodocument import anonimyzed_text,generate_data_for_anonymization,convert_document_to_format,extract_text_from_file
from .utils_publicador import publish_document

ANONYMIZED_MASK = "???"

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def create(self, request):
        file_catch = request.FILES
        output_path = settings.MEDIA_ROOT_TEMP_FILES + 'output.txt' + str(uuid.uuid4()) 
        #Creo el acta base
        new_file = file_catch['file']
        new_act = Act(file=new_file)
        try:
            new_act.full_clean()
        except:
            raise UnsupportedMediaType(media_type=new_file.content_type,detail=settings.ERROR_TEXT_FILE_TYPE)
        else:
            new_act.save()
        # Transformo el docx,en txt
        convert_document_to_format(new_act.file.path,output_path,'txt')
        # Guardo el texto en la instancia
        new_act.text=extract_text_from_file(output_path)
        new_act.save()
        # Analizo el texto
        ents = get_all_entity_ner(new_act.text)
        ocurrency_list = EntSerializer(ents,many=True)
       # Una vez procesado,guardar la info
        dataReturn = {
            "text": new_act.text,
            "ents": ocurrency_list.data,
            "id": new_act.id
        }
        os.remove(output_path)
        return Response(dataReturn)

    def update(self, request, pk):
        actCheck = Act.objects.get(id=pk)
        ocurrency_query = OcurrencyEntity.objects.filter(act=actCheck)
        if ocurrency_query.exists():
            ocurrency_query.delete()
        newEnts = request.data.get('ents')
        for ent in newEnts:
            OcurrencyEntity.objects.create(act=actCheck, startIndex=ent['start'],
                                           endIndex=ent['end'], entity=Entity.objects.get(name=ent['tag']),
                                           should_anonymized=ent['should_anonymized'])

        return Response()

    @action(methods=['post'], detail=True)
    def addAnnotations(self,request,pk=None):
        act_check = Act.objects.get(id=pk)
        new_ents = request.data.get('ents')
        ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
        all_query = list()
        if ocurrency_query.exists():
            ocurrency_query.delete()
        # Recorrido sobre las ents nuevas
        for ent in new_ents:
            #Chequeo por un flujo que me puede llegar entitades del front sin datos
            if (ent['start'] is not None and ent['end'] is not None):
                ocurrency = OcurrencyEntity.objects.create(act=act_check, startIndex=ent['start'],
                                                           endIndex=ent['end'], entity=Entity.objects.get(name=ent['tag']),
                                                           should_anonymized=ent['should_anonymized'])
                all_query.append(ocurrency)
        #Definicion de rutas
        output_text= settings.MEDIA_ROOT_TEMP_FILES + 'anonymous.txt'+ str(uuid.uuid4())
        output_docx = act_check.filename()
        # Generar el archivo en formato .docx anonimizado
        anonimyzed_text(act_check.file.path,settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + output_docx,
                        generate_data_for_anonymization (all_query,act_check.text,
                        ANONYMIZED_MASK ),'docx')
        # Generar el archivo para poder extraer el texto
        convert_document_to_format(settings.PRIVATE_STORAGE_ROOT + output_docx,output_text,'txt')
        # Leo el archivo anonimizado
        read_result = extract_text_from_file(output_text)
        # Borrado de archivo auxiliares
        os.remove(output_text)
        os.remove(act_check.file.path)
        # Guardado del archivo anonimizado
        act_check.file = settings.PRIVATE_STORAGE_ANONYMOUS_URL + output_docx
        act_check.save()
        #Construyo el response
        dataReturn = {
            "anonymous_text": read_result,
            "data_visualization": { "anonymous_ents": all_query.__len__() }
        }
        return Response(dataReturn)

    @action(methods=['post'], detail=True)
    def getAnonymousDocument(self,request,pk=None):
        act_check = Act.objects.get(id=pk)
        dataResponse = open(settings.PRIVATE_STORAGE_ANONYMOUS_FOLDER + act_check.filename(),'rb')
        return FileResponse(dataResponse,as_attachment=True)

    @action(methods=['post'], detail=True)
    def publishDocument(self,request,pk=None):
        act_check = Act.objects.get(id=pk)
        publish_document(act_check.file.path,settings.LIBERAJUS_CLOUDFOLDER_STORE,settings.LIBERAJUS_CLOUD_STORAGE_PROVIDER)
        dataResponse = {
            "status": "Ok",
            "text":"Se publico en  {}".format(settings.LIBERAJUS_CLOUD_STORAGE_PROVIDER)
        }
        return Response(data=dataResponse)


class OcurrencyEntityViewSet(viewsets.ModelViewSet):
    queryset = OcurrencyEntity.objects.all()
    serializer_class = OcurrencyEntitySerializer

class LearningModelViewSet(viewsets.ModelViewSet):
    queryset = LearningModel.objects.all()
    serializer_class = LearningModelSerializer

    @action(methods=['post'], detail=True)
    def useSubject(self,request,pk=None):
        select_model = LearningModel.objects.get(id=pk)
        ## Aca va estar la logica que cambie el modelo-a futuro-
        return Response(data="Se ha elegido la materia {}".format(select_model.name_subject))