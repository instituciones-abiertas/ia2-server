from ..models import OcurrencyEntity


def generate_data_visualization(ocurrenciesArray, act):
    # Se obtiene todos las distintas entidades que hay en el acta,para no visualizar entidades que no existen
    type_of_ents_in_act_array = get_entities_to_act(act)
    return {
        "anonimyzedEntitiesResult": calculated_anonimyzed_ents(ocurrenciesArray, type_of_ents_in_act_array),
        "notAnonimyzedEntitiesResult": calculated_not_anonimyzed_ents(ocurrenciesArray, type_of_ents_in_act_array),
        "entitiesPercentModel": calculated_sucess_percent_for_entity(ocurrenciesArray, type_of_ents_in_act_array),
        "total": number_of_entities(ocurrenciesArray),
        "efectivity_average": calculated_global_average(ocurrenciesArray),
    }


# Obtener un set de las entidades que aparecen en un acta
def get_entities_to_act(act_check):
    list_ent = []
    ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
    for ocurrency in list(ocurrency_query):
        list_ent.append(ocurrency.entity)

    return set(list_ent)


# Calcular cantidad de ocurrencias por entidades han sido detectadas y anonimizada
def calculated_anonimyzed_ents(ocurrenciesArray, type_of_ents_array):
    result_list = []

    for ent in type_of_ents_array:
        result_list.append(
            {
                "name": "Cantidad de ocurrencias de:  " + ent.name,
                "value": len(list_total_anonimyzed_ocurrency_for_ent(ent, ocurrenciesArray)),
            }
        )
    return result_list


# Calcular cantidad de ocurrencias por entidades han sido detectadas y no son anonimizada
def calculated_not_anonimyzed_ents(ocurrenciesArray, type_of_ents_array):
    result_list = []

    for ent in type_of_ents_array:
        result_list.append(
            {
                "name": "Cantidad de ocurrencias de:  " + ent.name,
                "value": len(list_total_not_anonimyzed_ocurrency_for_ent(ent, ocurrenciesArray)),
            }
        )
    return result_list


# Calcular los porcentajes de acierto por cada entidad
def calculated_sucess_percent_for_entity(ocurrenciesArray, type_of_ents_array):
    result_list = []
    percent_total = 0

    for ent in type_of_ents_array:
        percent_ent = calculated_percent_entity(ent, ocurrenciesArray)
        result_list.append({"name": "Porcentaje de acierto " + ent.name, "value": " Es {} %".format(percent_ent)})
        percent_total = percent_total + percent_ent

    # Agrega el porcentaje general,haciendo la sumatoria de las porcentajes,divido la cantidad
    result_list.append(calculated_sum_total_percent(percent_total, len(type_of_ents_array)))

    return result_list


# Calcula la cantidad total de ocurrencias de una entidad que son anonimizadas
def list_total_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id, ocurrenciesArray))


# Calcula la cantidad total de ocurrencias de una entidad que son anonimizadas
def list_total_anonimyzed_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id and x.should_anonymized, ocurrenciesArray))


# Calcula la cantidad total de ocurrencias de una entidad que no son anonimizadas
def list_total_not_anonimyzed_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id and not (x.should_anonymized), ocurrenciesArray))


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
def number_of_entities(ocurrenciesArray):
    all_entities = len(ocurrenciesArray)
    human_mark_entities = len(list(filter(lambda x: x.human_marked_ocurrency, ocurrenciesArray)))
    return [
        {"name": "Cantidad de Entidades totales detectadas ", "value": all_entities},
        {"name": "Cantidad de Entidades detectadas por humanxs", "value": human_mark_entities},
        {"name": "Cantidad de Entidades detectadas por modelo", "value": all_entities - human_mark_entities},
    ]


# Calcular porcentaje de acierto general realizando una suma de todos los promedios
def calculated_sum_total_percent(total_percent, total_ents):
    return {"name": "Porcentaje de acierto general ", "value": " Es {} %".format(round(total_percent / total_ents, 2))}


# Calculo de porcentaje de acierto en base a cantidades detectadas por el modelo
def calculated_global_average(ocurrenciesArray):
    not_human_mark_entities = len(list(filter(lambda x: not (x.human_marked_ocurrency), ocurrenciesArray)))
    return {
        "name": "Cantidad de acierto de modelo ",
        "value": "Es {} %".format(round((not_human_mark_entities / len(ocurrenciesArray)) * 100, 2)),
    }
