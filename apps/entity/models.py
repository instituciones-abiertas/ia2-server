from django.db import models
from django.utils import timezone


class Entity(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    should_anonimyzation = models.BooleanField(default=True)
    should_trained = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return 


class Act(models.Model):
    text = models.TextField(default="En Proceso")
    file = models.FileField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return  self.text

    def __unicode__(self):
        return 

class OcurrencyEntity(models.Model):
    act = models.ForeignKey(Act, on_delete=models.CASCADE,related_name='listOfEntity')
    startIndex = models.PositiveIntegerField()
    endIndex = models.PositiveIntegerField()
    entity = models.ForeignKey(to=Entity, on_delete=models.CASCADE)
    should_anonymized = models.BooleanField(default=True)
    
    def __str__(self):
        return self.entity.name

class LearningModel(models.Model):
    name_subject = models.CharField(max_length=60)
    last_update = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return  self.name_subject