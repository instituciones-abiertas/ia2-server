import string
import logging
import os
import time

from oodocument import oodocument
from .utils.oodocument import init_oo
from .exceptions import ServiceOddDocumentUnavailable
from .models import OcurrencyEntity

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from ia2.celery import app
from apps.data.helpers import extraer_datos


celery = app

# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")

# Esta dependencia esta solamente en produccion
try:
    from sentry_sdk import capture_exception
except ImportError:

    def capture_exception(err):
        print(err)


@shared_task
def train_model():
    print("Starting async task...")
    time.sleep(1)
    model_path = f"{settings.MODELS_PATH}/test_model/test.txt"

    model = None
    with open(model_path, "r") as reader:
        model = reader.readlines()

    line_to_change = int(model[2])
    model[line_to_change] = f"{line_to_change}." + f"Call number {line_to_change - 3} changed this line.\n "
    increased_line_to_change = line_to_change + 1
    model[2] = f"{str(increased_line_to_change)}\n"

    with open(model_path, "w") as reader:
        model = reader.writelines(model)

    print("RESULT MODEL")
    print(model)

    return "wait: secs and train, task Done!"


@shared_task
def extraer_datos_de_ocurrencias(act_id):
    act_number = act_id[0]  # Llega un array con un solo elemento y se extrae el id
    ocurrencias = list(OcurrencyEntity.objects.filter(act__id=act_number))
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

    return "wait: secs and extract, task Done!"


HEADER_STYLE_NAME = "First Page"


@shared_task
def reemplazo_asincronico_en_texto(
    path_document,
    path_output,
    format_output,
    data_to_replace,
    color=None,
    offset=0,
):
    oo = init_oo(path_document)
    # Cambio de color en caso que venga parametrizado
    if color and isinstance(color, list) and len(color) == 3:
        r, g, b = color
        oo.set_font_back_color(r, g, b)
    # Division entre entidades de header y body de texto
    data_replace_header = data_to_replace[0]
    data_replace_body = data_to_replace[1]
    try:
        # Reemplazo en body
        oo.replace_with_index(data_replace_body, path_output, format_output, offset, settings.NEIGHBOR_CHARS_SCAN)
        # Reemplazo en header si esta habilitado
        if settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION:
            oo.replace_with_index_in_header(
                data_replace_header, path_output, format_output, 0, settings.NEIGHBOR_CHARS_SCAN, HEADER_STYLE_NAME
            )
        oo.dispose()
        return f"Esta reemplazando el texto del documento{path_document}"
    except Exception:
        logger.exception(settings.ERROR_STORAGE_FILE_NOT_EXIST)
        raise ServiceOddDocumentUnavailable()
