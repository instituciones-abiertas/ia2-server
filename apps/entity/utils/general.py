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
    # Pensar como filtrar para dar solo las que tiene alguna ocurrencia
    type_of_ents = list(Entity.objects.all())

    for ent in type_of_ents:
        result_list.append(
            {
                "name": "Datos " + ent.name,
                "value": len(list_total_ocurrency_for_ent(ent, arrayEnts)),
            }
        )

    return result_list


def extraer_datos_de_ocurrencias(ocurrencias):
    # Consideracion: solo se queda con la 1er ocurrencia de estas entiedades

    def buscar(entidad):
        return next((o.text for o in ocurrencias if o.entity.name == entidad), None)

    entidades = ["CONTEXTO_VIOLENCIA", "CONTEXTO_VIOLENCIA_DE_GÉNERO", "LUGAR_HECHO", "FECHA_HECHO"]
    contexto_violencia, contexto_violencia_de_genero, lugar, fecha = list(map(buscar, entidades))

    if contexto_violencia or contexto_violencia_de_genero or lugar or fecha:
        try:
            extraer_datos(contexto_violencia, contexto_violencia_de_genero, lugar, fecha)
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


def calculate_sucess_percent_for_entity(arrayEnts):
    result_list = []
    # Pensar como filtrar para dar solo las que tiene alguna ocurrencia

    type_of_ents = list(Entity.objects.all())

    for ent in type_of_ents:
        result_list.append(
            {"name": "Porcentaje de acierto " + ent.name, "value": calculate_percent_entity(ent, arrayEnts)}
        )

    return result_list


# Calcula la cantidad total de ocurrencias de una entidad
def list_total_ocurrency_for_ent(ent, arrayEnts):
    return list(filter(lambda x: x.entity_id == ent.id, arrayEnts))


# Calcula la cantidad total de ocurrencias marcadas por humanos de una entidad
def list_human_ocurrency_for_ent(ent, arrayEnts):
    return list(filter(lambda x: x.entity_id == ent.id and not (x.human_marked_ocurrency), arrayEnts))


# Calcular porcentaje de acierto en una entididad
def calculate_percent_entity(ent, arrayEnts):
    if len(list_total_ocurrency_for_ent(ent, arrayEnts)) > 0:
        value_expectated = len(list_human_ocurrency_for_ent(ent, arrayEnts)) / len(
            list_total_ocurrency_for_ent(ent, arrayEnts)
        )
    else:
        value_expectated = 0
    return " Es {} %".format((1 - value_expectated) * 100)
