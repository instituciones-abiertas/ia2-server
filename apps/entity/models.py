from django.db import models
from django.utils import timezone


class Entity(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return 


class Act(models.Model):
    text = models.TextField()
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
    
    def __str__(self):
        return self.entity.name
     