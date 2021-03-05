from rest_framework import serializers

from .models import Act, Entity, OcurrencyEntity, LearningModel


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = (
            "id",
            "text",
            "created_date",
        )


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ("id", "name", "description", "should_anonimyzation")


class OcurrencyEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OcurrencyEntity
        fields = ("id", "startIndex", "endIndex", "entity", "should_anonymized")
        depth = 1


class EntSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField("get_id")
    start = serializers.SerializerMethodField("get_start_label")
    end = serializers.SerializerMethodField("get_end_label")
    tag = serializers.SerializerMethodField("get_tag_label")
    should_anonymized = serializers.BooleanField(default=True)
    human_marked_ocurrency = serializers.BooleanField(default=False)

    def get_start_label(self, obj):
        return obj.startIndex

    def get_end_label(self, obj):
        return obj.endIndex

    def get_tag_label(self, obj):
        return obj.entity.name

    def get_id(self, obj):
        return obj.id


class LearningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningModel
        fields = ("name_subject", "last_update")
