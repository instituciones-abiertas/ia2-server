from rest_framework import serializers

from .models import Act,Entity,OcurrencyEntity,LearningModel

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

class EntSerializer(serializers.Serializer):
    start = serializers.IntegerField()
    end = serializers.IntegerField()
    tag = serializers.SerializerMethodField('get_tag_label')

    def get_tag_label(self, obj):
            return obj.label_

class LearningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ('name_subject','last_update')
