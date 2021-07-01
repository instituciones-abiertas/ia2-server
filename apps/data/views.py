from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EdadStatsSerializer, HechoStatsSerializer, LugarStatsSerializer, DateRangeSerializer
from .models import Hecho
from django.db.models import Count, F, Avg, Sum, Q
from django.db.models.functions import Coalesce
from rest_framework import mixins, parsers, status, viewsets
from ..entity.exceptions import BadRequestAPI
import logging

logger = logging.getLogger("django.server")


def validate_range_dates(data):
    dates = DateRangeSerializer(data=data)
    if not dates.is_valid():
        logger.error(f"Envio mal los parametros de filtro start y end, {dates.data}")
        raise BadRequestAPI()

    start = dates.validated_data["start"]
    end = dates.validated_data["end"]
    return (start, end)


class LugarStatsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LugarStatsSerializer
    permission_classes = [IsAuthenticated]

    # Count Ocurrences of every "Lugar"
    def get_queryset(self):
        queryset = Hecho.objects
        if self.request.query_params.get("start") is not None and self.request.query_params.get("end") is not None:
            start, end = validate_range_dates(self.request.query_params)
            queryset = queryset.filter(_fecha__range=(start, end))
        return queryset.values("lugares___nombre").annotate(
            nombre=F("lugares___nombre"), cantidad=Count("lugares___nombre")
        )


class EdadStatsView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EdadStatsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Hecho.objects
        if self.request.query_params.get("start") is not None and self.request.query_params.get("end") is not None:
            start, end = validate_range_dates(self.request.query_params)
            queryset = queryset.filter(_fecha__range=(start, end))
        return queryset.aggregate(
            promedio_acusadx=Coalesce(Avg("_edad_acusadx"), 0), promedio_victima=Coalesce(Avg("_edad_victima"), 0)
        )

    def get(self, request):
        qs = self.get_queryset()
        sr = EdadStatsSerializer(qs)
        return Response(sr.data)


class HechoStatsView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = HechoStatsSerializer
    permission_classes = [IsAuthenticated]

    # Count violencia, violencia_genero, total, otros (ninguno de las violencias)
    def get_queryset(self):
        queryset = Hecho.objects
        if self.request.query_params.get("start") is not None and self.request.query_params.get("end") is not None:
            start, end = validate_range_dates(self.request.query_params)
            queryset = Hecho.objects.filter(_fecha__range=(start, end))
        return queryset.aggregate(
            total=Count("historico_id"),
            violencia_genero=Sum("_contexto_violencia_de_genero"),
            violencia=Sum("_contexto_violencia"),
            otros=Count("historico_id", filter=(Q(_contexto_violencia=0) & Q(_contexto_violencia_de_genero=0))),
        )

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        sr = HechoStatsSerializer(qs)
        return Response(sr.data)
