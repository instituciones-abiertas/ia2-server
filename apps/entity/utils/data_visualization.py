from ..models import OcurrencyEntity


def generate_data_visualization(ocurrenciesArray, act):
    # Se obtiene todos las distintas entidades que hay en el acta,para no visualizar entidades que no existen
    type_of_ents_in_act_array = get_entities_to_act(act)
    return {
        "entitiesResult": calculated_ents(ocurrenciesArray, type_of_ents_in_act_array),
        "total": total_of_entities(ocurrenciesArray, type_of_ents_in_act_array),
    }


# Obtener un set de las entidades que aparecen en un acta
def get_entities_to_act(act_check):
    list_ent = []
    ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
    for ocurrency in list(ocurrency_query):
        list_ent.append(ocurrency.entity)

    return set(list_ent)


# Calcular cantidad de ocurrencias por entidades han sido detectadas y anonimizada
def calculated_ents(ocurrenciesArray, type_of_ents_array):
    result_list = []

    for ent in type_of_ents_array:
        percent_ent = calculated_percent_entity(ent, ocurrenciesArray)
        result_list.append(
            {
                "ent": ent.name,
                "model_detect": len(list_model_ocurrency_for_ent(ent, ocurrenciesArray)),
                "human_detect": len(list_human_ocurrency_for_ent(ent, ocurrenciesArray)),
                "percent": percent_ent,
            }
        )
    return result_list


# Calcula la cantidad total de ocurrencias de una entidad que son anonimizadas
def list_total_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id, ocurrenciesArray))


# Calcula la cantidad total de ocurrencias marcadas por humanos de una entidad
def list_model_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id and not (x.human_marked_ocurrency), ocurrenciesArray))


# Calcula la cantidad total de ocurrencias marcadas por humanos de una entidad
def list_human_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id and x.human_marked_ocurrency, ocurrenciesArray))


# Calcular porcentaje de acierto en una entididad
def calculated_percent_entity(ent, ocurrenciesArray):
    if len(list_total_ocurrency_for_ent(ent, ocurrenciesArray)) > 0:
        value_expectated = len(list_human_ocurrency_for_ent(ent, ocurrenciesArray)) / len(
            list_total_ocurrency_for_ent(ent, ocurrenciesArray)
        )
    else:
        value_expectated = 0
    # revisar esta forma de imprimir el porcentaje
    return round((1 - value_expectated) * 100, 2)


# Calcular cantidades de entidades dependiendo de su tipo
def total_of_entities(ocurrenciesArray, type_of_ents_array):
    all_entities = len(ocurrenciesArray)
    human_mark_entities = len(list(filter(lambda x: x.human_marked_ocurrency, ocurrenciesArray)))
    return {
        "model_total_ent": all_entities - human_mark_entities,
        "human_total_ent": human_mark_entities,
        "percent_total": calculated_global_average(ocurrenciesArray, type_of_ents_array),
    }


# Calcular porcentaje de acierto general realizando una suma de todos los promedios
# def calculated_sum_total_percent(total_percent, total_ents):
# return {"name": "Porcentaje de acierto general ", "value": " Es {} %".format(round(total_percent / total_ents, 2))}


# Calculo de porcentaje con la sumatoria de acierto
def calculated_global_average(ocurrenciesArray, type_of_ents_array):
    total_percent = 0
    for ent in type_of_ents_array:
        total_percent = total_percent + calculated_percent_entity(ent, ocurrenciesArray)

    return round(total_percent / len(type_of_ents_array), 2)