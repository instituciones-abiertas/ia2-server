from .general import filter_spans
from .matcher import use_matchers
from .custom_rules import use_rules


def add_rules_sistem(nlp, doc, list_ents, matcher):
    if matcher:
        # Usamos los matchers creados y obtengo ocurrencias
        matcher_ents = use_matchers(nlp, matcher, doc)
        # Filtramos ocurrencias encontradas mirando si ya estan reconocidas como entidades
        filtered_matcher_ents = filter_spans(matcher_ents, list_ents)
        # Agrego a la lista de entidades las ocurrencias resultantes
        list_ents = list_ents + (filtered_matcher_ents)

    # Usamos las reglas creadas y obtengo ocurrencias
    ents_by_rules = use_rules(doc, list_ents)
    # Filtramos ocurrencias encontradas mirando si ya estan reconocidas como entidades
    filter_ents = filter_spans(list_ents, ents_by_rules)
    list_ents = ents_by_rules + filter_ents
    return list_ents
