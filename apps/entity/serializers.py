from rest_framework import serializers

from .models import Act,Entity,OcurrencyEntity

class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ('text', 'created_date',)

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('name', 'description')        

class OcurrencyEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OcurrencyEntity
        fields = ('startIndex', 'endIndex','act','entity')     