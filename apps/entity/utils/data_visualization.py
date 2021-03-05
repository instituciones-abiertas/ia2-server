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
    list_ent = set()
    ocurrency_query = OcurrencyEntity.objects.filter(act=act_check)
    for ocurrency in list(ocurrency_query):
        list_ent.add(ocurrency.entity)
    # Se convierte el set en lista para ordenar alfabeticamente
    return sorted(list(list_ent), key=lambda x: x.name)


# Calcular cantidad de ocurrencias por entidades han sido detectadas y anonimizada
def calculated_ents(ocurrenciesArray, type_of_ents_array):
    result_list = []

    for ent in type_of_ents_array:
        total_ocurrencies = len(list_total_ocurrency_for_ent(ent, ocurrenciesArray))
        wrong_model_ocurrencies = len(list_model_wrong_ocurrency_for_ent(ent, ocurrenciesArray))
        human_ocurrencies = len(list_human_ocurrency_for_ent(ent, ocurrenciesArray))
        result_list.append(
            {
                "ent": ent.name,
                "model_detect": total_ocurrencies - human_ocurrencies,
                "model_wrong_detect": wrong_model_ocurrencies,
                "human_detect": human_ocurrencies,
                "percent": calculated_percent_entity(total_ocurrencies, wrong_model_ocurrencies, human_ocurrencies),
            }
        )
    return result_list


# Calcula la cantidad total de ocurrencias de una entidad que son detectadas
def list_total_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id, ocurrenciesArray))


# Calcula la cantidad total de ocurrencias marcadas por modelo de una entidad
def list_model_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(
        filter(
            lambda x: x.entity_id == ent.id and not (x.human_marked_ocurrency),
            ocurrenciesArray,
        )
    )


# Calcula la cantidad  de ocurrencias erroneas marcadas por modelo de una entidad
def list_model_wrong_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(
        filter(
            lambda x: x.entity_id == ent.id and not (x.human_marked_ocurrency) and x.human_deleted_ocurrency,
            ocurrenciesArray,
        )
    )


# Calcula la cantidad total de ocurrencias marcadas por humanos de una entidad
def list_human_ocurrency_for_ent(ent, ocurrenciesArray):
    return list(filter(lambda x: x.entity_id == ent.id and x.human_marked_ocurrency, ocurrenciesArray))


# Calcular porcentaje de acierto en una entidad
def calculated_percent_entity(total_ocurrencies, wrong_model_ocurrencies, human_ocurrencies):
    if check_correct_ocurrency_high(total_ocurrencies, wrong_model_ocurrencies, human_ocurrencies):
        value_expectated = (human_ocurrencies + wrong_model_ocurrencies) / total_ocurrencies
    # Si hay mas ocurrencias por humanx que detectada por el modelo,es 0 el porcentaje
    elif human_ocurrencies >= total_ocurrencies - wrong_model_ocurrencies:
        value_expectated = 1
    # El caso que no hay ninguna ocurrencia detectada
    else:
        value_expectated = 0
    # revisar esta forma de imprimir el porcentaje
    return round((1 - value_expectated) * 100, 2)


# Calcular cantidades de entidades dependiendo de su tipo
def total_of_entities(ocurrenciesArray, type_of_ents_array):
    all_entities = len(ocurrenciesArray)
    human_mark_entities = len(list(filter(lambda x: x.human_marked_ocurrency, ocurrenciesArray)))
    model_wrong_entities = len(list(filter(lambda x: x.human_deleted_ocurrency, ocurrenciesArray)))
    model_total_ent = all_entities - human_mark_entities
    return {
        "model_total_ent": model_total_ent,
        "model_wrong_ent": model_wrong_entities,
        "human_total_ent": human_mark_entities,
        "percent_total": calculated_global_all_entities_average(
            model_total_ent, human_mark_entities, model_wrong_entities
        ),
    }


# Calculo de porcentaje con la sumatoria de acierto por entidad(deprecado)
# def calculated_global_average(ocurrenciesArray, type_of_ents_array):
# total_percent = 0
# for ent in type_of_ents_array:
# total_percent = total_percent + calculated_percent_entity(ent, ocurrenciesArray)

# return round(total_percent / len(type_of_ents_array), 2)


# Calculo de porcenteja sobre el total de las entidades detectadas por el modelo , sobre el total (modelo + humano)
def calculated_global_all_entities_average(model_ents, human_ents, model_wrong_ents):
    percent = (model_ents - model_wrong_ents) / (model_ents + human_ents)
    return round(percent * 100, 2)


# Chequeo de que se detectaron correctamente mas entidades que erroneamente
def check_correct_ocurrency_high(total_ocurrencies, wrong_model_ocurrencies, human_ocurrencies):
    return total_ocurrencies > 0 and (wrong_model_ocurrencies + human_ocurrencies) < total_ocurrencies
