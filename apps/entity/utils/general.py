from ..models import Entity, Act, OcurrencyEntity, LearningModel
from ..exceptions import ActNotExist, StorageFileNotExist
from apps.data.helpers import extraer_datos


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


def buscar_entidad(ocurrencias, entidad):
    return next((o.text for o in ocurrencias if o.entity == entidad), None)


def extraer_datos_de_ocurrencias(ocurrencias):
    # Consideracion: solo se queda con la 1er ocurrencia de estas entiedades
    lugar = buscar_entidad(ocurrencias, "LUGAR_HECHO")
    fecha = buscar_entidad(ocurrencias, "FECHA_HECHO")
    contexto_violencia = buscar_entidad(ocurrencias, "CONTEXTO_VIOLENCIA")
    contexto_violencia_de_genero = buscar_entidad(ocurrencias, "CONTEXTO_VIOLENCIA_DE_GENERO")
    if lugar or fecha or contexto_violencia or contexto_violencia_de_genero:
        extraer_datos(contexto_violencia, contexto_violencia_de_genero, lugar, fecha)
