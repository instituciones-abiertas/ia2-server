from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import EntitySerializer,ActSerializer,OcurrencyEntitySerializer,FakeSerializer
from .models import Entity,Act,OcurrencyEntity


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer



class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer
    
    def create(self, validated_data):
       ## Una vez procesado,guardar la info
       fake_entity = [      { 
                               "start": 28,
                                "end":45,
                                "tag":"Juez"
                            },
                            {
                                "start": 20,
                                "end": 24,
                                "tag":"Domicilio"
                            },
                            {
                                "start": 56,
                                "end":58,
                                "tag":"Edad"
                            }
                    ]

       dataReturn = { "text" : "Soy un texto de prueba aca tengo un numero y un juez y una edad",
                    "ents" : fake_entity
              }
       return Response(dataReturn)

    def update(self, validated_data):
       ## Aca se deberia procesar con la util de spacy o la solucion que utilicemos.
       ## Una vez procesado,guardar la info
       fake_entity = [      { 
                               "starIndex": 28,
                                "endIndex":45,
                                "entityName":"Juez"
                            },
                            {
                                "starIndex": 15,
                                "endIndex": 21,
                                "entityName":"Domicilio"
                            },
                            {
                                "starIndex": 56,
                                "endIndex":58,
                                "entityName":"Edad"
                            }
                    ]

       #print(fake_entity.values())
       return Response( fake_entity)   
 

class OcurrencyEntityViewSet(viewsets.ModelViewSet):
    queryset = OcurrencyEntity.objects.all()
    serializer_class = OcurrencyEntitySerializer


class FakeViewSet(APIView):
     queryset = []

def post(self, request):
        print(request.data)
        fake_entity = [      { 
                               "starIndex": 28,
                                "endIndex":45,
                                "entityName":"Juez"
                            },
                            {
                                "starIndex": 20,
                                "endIndex": 24,
                                "entityName":"Domicilio"
                            },
                            {
                                "starIndex": 56,
                            "endIndex":58,
                            "entityName":"Edad"
                            }]
        results = FakeSerializer(fake_entity, many=True).data
        print(results)                    
        return Response(results)