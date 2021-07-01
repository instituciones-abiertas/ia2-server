from ..models import Act, OcurrencyEntity
from ..exceptions import ActNotExist, StorageFileNotExist, BadRequestAPI, NoEntitiesDetected

from apps.data.helpers import extraer_datos
import logging
import numbers
import hashlib
from django.conf import settings


# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")


def check_exist_act(pk):
    try:
        return Act.objects.get(id=pk)
    except Act.DoesNotExist:
        logger.exception(settings.ERROR_ACT_NOT_EXIST)
        raise ActNotExist()


def open_file(path, type, encode):
    try:
        output = open(path, type, encoding=encode)
    except OSError:
        logger.exception(settings.ERROR_STORAGE_FILE_NOT_EXIST)
        raise StorageFileNotExist()
    else:
        return output


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


def check_delete_ocurrencies(list_ocurrencies):
    # Valido que todas  las ocurrencias tengan campo id
    ids = map(lambda ocurrency: "id" in ocurrency, list_ocurrencies)
    if all(ids):
        return list_ocurrencies
    else:
        logger.error("Lista de ocurrencias mal formada")
        logger.error(f"La lista de ocurrencias es {list_ocurrencies} ")
        raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer
def check_add_annotations_request(request_data):
    if request_data and len(request_data.keys()) == 2:  # Valido ademas que solo venga las dos keys esperadas
        check_request_params(request_data, ["newOcurrencies", "deleteOcurrencies"])
        return request_data
    else:
        logger.error(f"Formato no esperado {request_data}")
        raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer
def check_request_params(request_data, list_params):
    for param in list_params:
        if param not in request_data.keys() or not check_type_params(request_data.get(param), [], param):
            logger.error(f"Formato no esperado {request_data} ")
            raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer
def check_type_params(data, expected_type, param_name):
    if type(data) != type(expected_type):
        logger.error(f"Es incorrecto el formato del parametro {param_name}")
        raise BadRequestAPI()
    else:
        return True


# TODO: Migrar a Json Schema o Serializer
def check_new_ocurrencies(list_ocurrencies, list_ent, act):
    result = list(map(lambda ocurrency: check_new_ocurrency(ocurrency, list_ent), list_ocurrencies))
    if all(result):
        return check_act_with_ocurrency(act, list_ocurrencies)
    else:
        logger.error("Lista de ocurrencias mal formada")
        logger.error(f"La lista de ocurrencias es {list_ocurrencies} ")
        raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer


def check_new_ocurrency(ocurrency, list_ent_name):
    try:
        return (
            check_tag(ocurrency["tag"], list_ent_name)  # Validacion que corresponda a una etiqueta del sistema
            and check_start_end(ocurrency["start"], ocurrency["end"])  # Validacion de indices
            # and ocurrency.keys() == 3  # Validacion para agregar en un futuro cuando desde el front solo se envie lo minimo
        )
    except Exception as e:
        logger.error(f"No encuentra el campo {e}")
        logger.error(f"Nueva ocurrencia erronea {ocurrency}")
        raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer
def check_tag(tag, list_ent_name):
    return tag in list_ent_name


# TODO: Migrar a Json Schema o Serializer
# Se valida que sean numeros, que sea valido el intervalo
def check_start_end(start, end):
    return isinstance(start, numbers.Integral) and isinstance(end, numbers.Integral) and start < end and start >= 0


def check_act_with_ocurrency(act, new_ocurrency_list):
    model_ocurrency = OcurrencyEntity.objects.filter(act=act)
    if model_ocurrency.exists() or (not model_ocurrency.exists() and new_ocurrency_list):
        return new_ocurrency_list
    else:
        logger.error(
            f"El texto de la siguiente acta {act.id} no contiene entidades detectadas ni cargadas por usuarixs"
        )
        raise NoEntitiesDetected()


# TODO: Migrar a Json Schema o Serializer
def check_exist_and_type_field(data, field, type_expected):
    if type(data.get(field)) == type_expected:
        return data.get(field)
    else:
        logger.error(f"No es el tipo esperado en {data}")
        raise BadRequestAPI()


def calculate_hash(text):
    def hash(string):
        return hashlib.sha256(str(string).encode("utf-8")).digest()

    return hash(text)
