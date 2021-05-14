from rest_framework import serializers
from .models import Historico, Lugar, Hecho


# Date default Format "%y-%m-%d"
class DateRangeSerializer(serializers.Serializer):
    start = serializers.DateField(required=False)
    end = serializers.DateField(required=False)

    def validate(self, attrs):
        if not attrs.keys() == {"start", "end"}:
            raise serializers.ValidationError("Ambas fechas son requeridas")

        if attrs["start"] > attrs["end"]:
            raise serializers.ValidationError("Fecha de fin debe ser mayor a fecha de comienzo")
        return attrs


class LugarStatsSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=True, allow_blank=False, max_length=200)
    cantidad = serializers.IntegerField(required=True)


class EdadStatsSerializer(serializers.Serializer):
    promedio_acusadx = serializers.IntegerField(required=True)
    promedio_victima = serializers.IntegerField(required=True)


class HechoStatsSerializer(serializers.Serializer):
    violencia = serializers.IntegerField(required=True)
    violencia_genero = serializers.IntegerField(required=True)
    total = serializers.IntegerField(required=True)
    otros = serializers.IntegerField(required=True)
