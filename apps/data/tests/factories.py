import random
from factory import Faker as FactoryFaker, LazyAttribute, SubFactory, LazyFunction, Maybe, post_generation
from factory.django import DjangoModelFactory
from apps.data.models import Lugar, Hecho, Historico
from faker import Faker
import datetime

Faker.seed(0)
fake = Faker(locale="es_ES")


class HistoricoFactory(DjangoModelFactory):
    class Meta:
        model = Historico
        exclude = (
            "is_contexto_violencia",
            "is_contexto_violencia_de_genero",
            "is_fecha",
            "is_lugar",
            "is_edad_victima",
            "is_edad_acusadx",
        )

    is_contexto_violencia = FactoryFaker("pybool")
    contexto_violencia = Maybe("is_contexto_violencia", "Texto", None)

    is_contexto_violencia = FactoryFaker("pybool")
    contexto_violencia_de_genero = Maybe("is_contexto_violencia_de_genero", "Texto", None)

    is_fecha = FactoryFaker("pybool")
    fecha = Maybe("is_fecha", str(fake.date_time()), None)

    is_lugar = FactoryFaker("pybool")
    lugar = Maybe("is_lugar", fake.country(), None)

    is_edad_acusadx = FactoryFaker("pybool")
    edad_acusadx = Maybe("is_edad_acusadx", str(random.randint(10, 100)), None)

    is_edad_victima = FactoryFaker("pybool")
    edad_victima = Maybe("is_edad_victima", str(random.randint(10, 100)), None)


class LugarFactory(DjangoModelFactory):
    class Meta:
        model = Lugar

    _nombre = LazyAttribute(lambda h: fake.country())


class HechoFactory(DjangoModelFactory):
    class Meta:
        model = Hecho

    historico = SubFactory(HistoricoFactory)
    _contexto_violencia = LazyAttribute(lambda h: True if h.historico.contexto_violencia else False)
    _contexto_violencia_de_genero = LazyAttribute(
        lambda h: True if h.historico.contexto_violencia_de_genero else False
    )
    _fecha = LazyAttribute(
        lambda h: datetime.datetime.strptime(h.historico.fecha, "%Y-%m-%d %H:%M:%S") if h.historico.fecha else None
    )
    _edad_acusadx = LazyAttribute(
        lambda h: int(h.historico.edad_acusadx[:1] + "0") if h.historico.edad_acusadx else False
    )
    _edad_victima = LazyAttribute(
        lambda h: int(h.historico.edad_victima[:1] + "0") if h.historico.edad_victima else False
    )

    @post_generation
    def lugares(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for lugar in extracted:
                self.lugares.add(lugar)
