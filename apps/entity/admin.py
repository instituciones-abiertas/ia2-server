from django.contrib import admin
from datetime import timedelta
from .models import Entity, Act, OcurrencyEntity, ActStats
from django.utils.translation import ugettext_lazy as _

admin.site.register(Entity)
admin.site.register(Act)
admin.site.register(OcurrencyEntity)


class ActStatsAdmin(admin.ModelAdmin):
    list_display = (
        "act_id_show",
        "load_time_seconds",
        "detection_time_seconds",
        "anonymization_time_seconds",
        "extraction_time_seconds",
        "review_time_seconds",
    )

    def act_id_show(self, obj):
        return obj.act_id

    act_id_show.short_description = _("act_id")

    def load_time_seconds(self, obj):
        return obj.load_time.total_seconds()

    load_time_seconds.short_description = _("load_time_seconds")

    def detection_time_seconds(self, obj):
        return obj.detection_time.total_seconds()

    detection_time_seconds.short_description = _("detection_time_seconds")

    def anonymization_time_seconds(self, obj):
        return obj.anonymization_time.total_seconds()

    anonymization_time_seconds.short_description = _("anonymization_time_seconds")

    def extraction_time_seconds(self, obj):
        return obj.extraction_time.total_seconds()

    extraction_time_seconds.short_description = _("extraction_time_seconds")

    def review_time_seconds(self, obj):
        return obj.review_time.total_seconds()

    review_time_seconds.short_description = _("review_time_seconds")


admin.site.register(ActStats, ActStatsAdmin)
