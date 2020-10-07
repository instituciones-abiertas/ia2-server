from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import EntitySerializer, ActSerializer, OcurrencyEntitySerializer, EntSerializer,LearningModelSerializer
from .models import Entity, Act, OcurrencyEntity,LearningModel
from .utils_spacy import get_all_entity_ner


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer

    def create(self, request):
        newAct = Act.objects.create(text=request.data.get('text'))
        ents = get_all_entity_ner(newAct.text)
        ocurrency_list = []
        for ent in ents:
            OcurrencyEntity.objects.create(act=newAct, startIndex=ent.start_char,
                                           endIndex=ent.end_char, entity=Entity.objects.get(name=ent.label_))
            entSerializer = EntSerializer(ent)
            ocurrency_list.append(entSerializer.data)
        print(ocurrency_list)
       # Una vez procesado,guardar la info
        dataReturn = {
            "text": newAct.text,
            "ents": ocurrency_list,
            "id": newAct.id
        }
        return Response(dataReturn)

    def update(self, validated_data, pk):
        actCheck = Act.objects.get(id=validated_data.data.get('id'))
        ocurrency_query = OcurrencyEntity.objects.filter(act=actCheck)
        if ocurrency_query.exists():
            ocurrency_query.delete()
        newEnts = validated_data.data.get('ents')
        for ent in newEnts:
            OcurrencyEntity.objects.create(act=actCheck, startIndex=ent['start'],
                                           endIndex=ent['end'], entity=Entity.objects.get(name=ent['tag']))

        return Response()

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