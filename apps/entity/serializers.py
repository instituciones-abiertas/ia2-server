from rest_framework import serializers

from .models import Act,Entity,OcurrencyEntity,LearningModel

class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ('id','text', 'created_date',)

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('id','name', 'description','should_anonimyzation')

class OcurrencyEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OcurrencyEntity
        fields = ('id','startIndex', 'endIndex','entity','should_anonymized')
        depth = 1

class EntSerializer(serializers.Serializer):
    start = serializers.SerializerMethodField('get_start_label')
    end = serializers.SerializerMethodField('get_end_label')
    tag = serializers.SerializerMethodField('get_tag_label')
    should_anonymized = serializers.BooleanField(default=True)

    def get_start_label(self,obj):
        return obj.start_char

    def get_end_label(self,obj):
        return obj.end_char

    def get_tag_label(self, obj):
            return obj.label_

class LearningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ('name_subject','last_update')
