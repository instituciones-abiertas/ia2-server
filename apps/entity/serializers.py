from rest_framework import serializers

from .models import Act, Entity, OcurrencyEntity

class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ('id','text', 'created_date',)

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id','name', 'description')

class OcurrencyEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OcurrencyEntity
        fields = ('id','startIndex', 'endIndex','entity')
        depth = 1

class FakeSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    startIndex = serializers.IntegerField()
    endIndex = serializers.IntegerField()
    entity = serializers.CharField(max_length=256)
