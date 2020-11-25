from django.db import models
from .utils.lugares import get_comuna_caba
from .utils.fechas import procesa_fecha


class Historico(models.Model):
    fecha = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)
    contexto_violencia = models.CharField(max_length=200)
    contexto_violencia_de_genero = models.CharField(max_length=200)


class LugarManager(models.Manager):
    def get_or_create_lugar(self, nombre):
        comuna = get_comuna_caba(nombre)
        lugar, create = self.get_or_create(_nombre=comuna["nombre"])
        return lugar


# Agregar campos de lon y lat
class Lugar(models.Model):
    _nombre = models.CharField(max_length=200)
    objects = LugarManager()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        try:
            comuna = get_comuna_caba(value)
            self._nombre = comuna["nombre"]
        except Exception:
            self._nombre = None


class Hecho(models.Model):
    _contexto_violencia = models.BooleanField(default=False)
    _contexto_violencia_de_genero = models.BooleanField(default=False)
    _fecha = models.DateField()
    lugares = models.ManyToManyField(Lugar)
    historico = models.OneToOneField(
        Historico,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, value):
        fecha = procesa_fecha(value)
        self._fecha = fecha

    @property
    def contexto_violencia_de_genero(self):
        return self._contexto_violencia_de_genero

    @contexto_violencia_de_genero.setter
    def contexto_violencia_de_genero(self, value):
        b = False
        if value:
            b = True
        self._contexto_violencia_de_genero = b

    @property
    def contexto_violencia(self):
        return self._contexto_violencia

    @contexto_violencia.setter
    def contexto_violencia(self, value):
        b = False
        if value:
            b = True
        self._contexto_violencia = b
