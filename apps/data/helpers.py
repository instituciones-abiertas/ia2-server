from .models import Lugar, Hecho, Historico
from django.db import transaction, DatabaseError


def extraer_datos(contexto_violencia, contexto_violencia_de_genero, lugar, fecha, edad_acusadx, edad_victima):
    try:
        with transaction.atomic():
            # Se crea histórico para dejar rastro de lo hecho y refinar la inteligencia de extracción
            h = Historico.objects.create(
                contexto_violencia=contexto_violencia,
                contexto_violencia_de_genero=contexto_violencia_de_genero,
                lugar=lugar,
                fecha=fecha,
                edad_acusadx=edad_acusadx,
                edad_victima=edad_victima,
            )
            # Se crea un nuevo lugar del hecho o se trae uno repetido
            comuna = None
            if h.lugar:
                comuna = Lugar.objects.get_or_create_lugar(h.lugar)

            # Se crea un hecho y se lo vincula con el historico y el lugar donde se produjo

            hecho = Hecho.objects.create(
                contexto_violencia=h.contexto_violencia,
                contexto_violencia_de_genero=h.contexto_violencia_de_genero,
                fecha=h.fecha,
                edad_acusadx=h.edad_acusadx,
                edad_victima=h.edad_victima,
                historico=h,
            )

            if comuna:
                hecho.lugares.add(comuna)
    except DatabaseError:
        # Deberiamos loguear
        print("Error al grabar la extracción de datos")
        raise
