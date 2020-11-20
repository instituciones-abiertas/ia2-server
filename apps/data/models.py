from django.db import models


class Lugar(models.Model):
    name = models.CharField(max_length=200)


class Hecho(models.Model):
    contexto_violencia = models.BooleanField(default=False)
    contexto_violencia_de_genero = models.BooleanField(default=False)
    fecha = models.DateField()
    lugares = models.ManyToManyField(Lugar)
