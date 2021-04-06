from django.contrib import admin
from datetime import timedelta
from .models import Entity, Act, OcurrencyEntity, ActStats

admin.site.register(Entity)
admin.site.register(Act)
admin.site.register(OcurrencyEntity)


class ActStatsAdmin(admin.ModelAdmin):
    list_display = (
        "act_id",
        "load_time_seconds",
        "detection_time_seconds",
        "anonymization_time_seconds",
        "extraction_time_seconds",
    )


admin.site.register(ActStats, ActStatsAdmin)
