from ..models import Act, OcurrencyEntity
<<<<<<< HEAD
from ..exceptions import ActNotExist, StorageFileNotExist, BadRequestAPI, ZeroOcurrencyDetectInAct

=======
from ..exceptions import ActNotExist, StorageFileNotExist, NoEntitiesDetected
>>>>>>> actualizacion de llamadas  de la excepcion
from apps.data.helpers import extraer_datos
import logging
import numbers
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
            if (span.start >= s.start and span.start < s.end) or (s.start >= span.start and s.end <= span.end):
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
        logger.error(e)
        logger.error(f"Nueva ocurrencia erronea {ocurrency}")
        raise BadRequestAPI()


# TODO: Migrar a Json Schema o Serializer
def check_tag(tag, list_ent_name):
    return tag in list_ent_name


# TODO: Migrar a Json Schema o Serializer
# Se valida que sean numeros, que sea valido el intervalo
def check_start_end(start, end):
    return isinstance(start, numbers.Integral) and isinstance(end, numbers.Integral) and start < end and start > 0


def check_act_with_ocurrency(act, new_ocurrency_list):
    model_ocurrency = OcurrencyEntity.objects.filter(act=act)
    if model_ocurrency.exists() or (not model_ocurrency.exists() and new_ocurrency_list):
        return new_ocurrency_list
    else:
        raise NoEntitiesDetected()
