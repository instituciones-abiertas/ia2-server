from ..models import Act
from ..exceptions import ActNotExist, StorageFileNotExist
from apps.data.helpers import extraer_datos
import logging
from django.conf import settings

# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")

# Esta dependencia esta solamente en produccion
try:
    from sentry_sdk import capture_exception
except ImportError:

    def capture_exception(err):
        print(err)


def check_exist_act(pk):
    try:
        return Act.objects.get(id=pk)
    except Act.DoesNotExist:
        logger.exception(settings.ERROR_ACT_NOT_EXIST)
        raise ActNotExist()


def open_file(path, type):
    try:
        output = open(path, type)
    except OSError:
        logger.exception(settings.ERROR_STORAGE_FILE_NOT_EXIST)
        raise StorageFileNotExist()
    else:
        return output


def extraer_datos_de_ocurrencias(ocurrencias):
    # Consideracion: solo se queda con la 1er ocurrencia de estas entiedades

    def buscar(entidad):
        return next((o.text for o in ocurrencias if o.entity.name == entidad), None)

    entidades = [
        "CONTEXTO_VIOLENCIA",
        "CONTEXTO_VIOLENCIA_DE_GÉNERO",
        "LUGAR_HECHO",
        "FECHA_HECHO",
        "EDAD_ACUSADX",
        "EDAD_VICTIMA",
    ]
    contexto_violencia, contexto_violencia_de_genero, lugar, fecha, edad_acusadx, edad_victima = list(
        map(buscar, entidades)
    )

    if contexto_violencia or contexto_violencia_de_genero or lugar or fecha or edad_acusadx or edad_victima:
        try:
            extraer_datos(contexto_violencia, contexto_violencia_de_genero, lugar, fecha, edad_acusadx, edad_victima)
        except Exception as error:
            capture_exception(error)


def filter_spans(a_list, b_list):
    # filtra spans de a_list que se overlapeen con algun span de b_list
    def overlap(span, span_list):
        for s in span_list:
            if (span.start_char >= s.startIndex and span.end_char < s.endIndex) or (
                s.startIndex >= span.start_char and s.endIndex <= span.end_char
            ):
                return True
        return False

    return [span for span in a_list if not overlap(span, b_list)]
