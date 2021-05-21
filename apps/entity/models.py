from django.db import models
from django.utils import timezone
from private_storage.fields import PrivateFileField
from datetime import timedelta
import os
from .validator import get_file_extension, name_length


class Entity(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    should_anonimyzation = models.BooleanField(default=True)
    should_trained = models.BooleanField(default=True)
    enable_multiple_selection = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return


class Act(models.Model):
    text = models.TextField(default="En Proceso")
    file = PrivateFileField(max_length=200, validators=[get_file_extension, name_length])
    created_date = models.DateTimeField(default=timezone.now)
    offset_header = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return

    def filename(self):
        return os.path.basename(self.file.name)


class ActStats(models.Model):
    act = models.OneToOneField(
        Act,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    load_time = models.DurationField(default=timedelta())
    detection_time = models.DurationField(default=timedelta())
    anonymization_time = models.DurationField(default=timedelta())
    find_all_ocurrencies = models.DurationField(default=timedelta())
    extraction_time = models.DurationField(default=timedelta())
    review_time = models.DurationField(default=timedelta())
    begin_review_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Estadisticas Acta Id {self.act.id}"

    def act_id(self):
        return str(self.act.id)


class OcurrencyEntity(models.Model):
    act = models.ForeignKey(Act, on_delete=models.CASCADE, related_name="listOfEntity")
    startIndex = models.PositiveIntegerField()
    endIndex = models.PositiveIntegerField()
    entity = models.ForeignKey(to=Entity, on_delete=models.CASCADE)
    should_anonymized = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    human_marked_ocurrency = models.BooleanField(default=False)
    human_deleted_ocurrency = models.BooleanField(default=False)

    def __str__(self):
        return self.entity.name


class LearningModel(models.Model):
    name_subject = models.CharField(max_length=60)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name_subject
