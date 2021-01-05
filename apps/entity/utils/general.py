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


# Obtener un set de las entidades que aparecen en un acta
def get_entities_to_act(act_check):
    list_ent = []
    ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
    for ocurrency in list(ocurrency_query):
        list_ent.append(ocurrency.entity)

    return set(list_ent)


def calculate_ents_anonimyzed(arrayEnts, act):
    result_list = []
    type_of_ents = get_entities_to_act(act)

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


def calculate_sucess_percent_for_entity(arrayEnts, act):
    result_list = []
    type_of_ents = get_entities_to_act(act)
    percent_total = 0

    for ent in type_of_ents:
        percent_ent = calculate_percent_entity(ent, arrayEnts)
        result_list.append({"name": "Porcentaje de acierto " + ent.name, "value": " Es {} %".format(percent_ent)})
        percent_total = percent_total + percent_ent

    result_list.append(calculate_sum_total_percent(percent_total, len(type_of_ents)))
    return result_list


# Calcula la cantidad total de ocurrencias de una entidad
def list_total_ocurrency_for_ent(ent, arrayEnts):
    return list(filter(lambda x: x.entity_id == ent.id, arrayEnts))


# Calcula la cantidad total de ocurrencias marcadas por humanos de una entidad
def list_human_ocurrency_for_ent(ent, arrayEnts):
    return list(filter(lambda x: x.entity_id == ent.id and x.human_marked_ocurrency, arrayEnts))


# Calcular porcentaje de acierto en una entididad
def calculate_percent_entity(ent, arrayEnts):
    if len(list_total_ocurrency_for_ent(ent, arrayEnts)) > 0:
        value_expectated = len(list_human_ocurrency_for_ent(ent, arrayEnts)) / len(
            list_total_ocurrency_for_ent(ent, arrayEnts)
        )
    else:
        value_expectated = 0
    # revisar esta forma de imprimir el porcentaje
    return round((1 - value_expectated) * 100, 2)


# Calcular cantidades de entidades dependiendo de su tipo
def number_of_entities(arrayEnts):
    all_entities = len(arrayEnts)
    human_mark_entities = len(list(filter(lambda x: x.human_marked_ocurrency, arrayEnts)))
    return [
        {"name": "Cantidad de Entidades totales detectadas ", "value": all_entities},
        {"name": "Cantidad de Entidades detectatados por humanxs", "value": human_mark_entities},
        {"name": "Cantidad de Entidades detectatados por modelo", "value": all_entities - human_mark_entities},
    ]


# Calcular porcentaje de acierto general realizando una suma de todos los promedios
def calculate_sum_total_percent(total_percent, total_ents):
    return {"name": "Porcentaje de acierto general ", "value": " Es {} %".format(round(total_percent / total_ents, 2))}


# Calculo de porcentaje de acierto en base a cantidades detectadas por el modelo
def calculate_global_average(arrayEnts):
    not_human_mark_entities = len(list(filter(lambda x: not (x.human_marked_ocurrency), arrayEnts)))
    return {
        "name": "Cantidad de acierto de modelo ",
        "value": "Es {} %".format(round((not_human_mark_entities / len(arrayEnts)) * 100, 2)),
    }
