from ..models import Entity, Act, OcurrencyEntity, LearningModel
from ..exceptions import ActNotExist, StorageFileNotExist
from apps.data.helpers import extraer_datos

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
        raise ActNotExist()


def open_file(path):
    try:
        output = open(path, "rb")
    except OSError:
        raise StorageFileNotExist()
    else:
        return output


def calculate_ents_anonimyzed(arrayEnts):
    result_list = []
    type_of_ents = list(Entity.objects.all())

    for ent in type_of_ents:
        result_list.append(
            {
                "name": "Datos " + ent.name,
                "value": len(list(filter(lambda x: x.entity_id == ent.id, arrayEnts))),
            }
        )

    return result_list


def extraer_datos_de_ocurrencias(ocurrencias):
    # Consideracion: solo se queda con la 1er ocurrencia de estas entiedades

    def buscar(entidad):
        return next((o.text for o in ocurrencias if o.entity == entidad), None)

    entidades = ["CONTEXTO_VIOLENCIA", "CONTEXTO_VIOLENCIA_DE_GENERO", "LUGAR_HECHO", "FECHA_HECHO"]
    contexto_violencia, contexto_violencia_de_genero, lugar, fecha = list(map(buscar, entidades))

    if contexto_violencia or contexto_violencia_de_genero or lugar or fecha:
        try:
            extraer_datos(contexto_violencia, contexto_violencia_de_genero, lugar, fecha)
        except Exception as error:
            capture_exception(error)
