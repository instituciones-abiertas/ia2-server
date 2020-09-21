from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import EntitySerializer,ActSerializer,OcurrencyEntitySerializer
from .models import Entity,Act,OcurrencyEntity


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer



class ActViewSet(viewsets.ModelViewSet):
    queryset = Act.objects.all()
    serializer_class = ActSerializer
    
    
    def create(self, validated_data):
        return Act.objects.create(**validated_data)
 

class OcurrencyEntityViewSet(viewsets.ModelViewSet):
    queryset = OcurrencyEntity.objects.all()
    serializer_class = OcurrencyEntitySerializer
