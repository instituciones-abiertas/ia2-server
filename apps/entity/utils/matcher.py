from spacy.tokens import Span

patterns = {
            "NUM": [{"LIKE_NUM": True}],
        }

def add_matchers(matcher):
    # El mactch_id debe ser igual a el NOMBRE de la entidad
    for match_id, pattern in patterns.items():
        matcher.add(match_id, None, pattern)

def filterEntsByRightNeightbor(ents_list, ent_name, word_list, neightbourPosition):
    # Filtra las entidades que a la izquierda no tienen una palabra que pertenezca a la lista dada.
    return [ent for ent in ents_list if ent.label_ == ent_name and ent[0].nbor(neightbourPosition).text not in word_list]

def filterEntsByLeftNeightbor(ents_list, ent_name, word_list, neightbourPosition):
    # Filtra las entidades que a la izquierda no tienen una palabra que pertenezca a la lista dada.
    return [ent for ent in ents_list if ent.label_ == ent_name and ent[0].nbor(neightbourPosition).text not in word_list]

def use_matchers(nlp, matcher, doc):
        if not doc:
            return None

        matches = matcher(doc)
        spans = []
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            spans.append(Span(doc, start, end, label))
        spans = filterEntsByLeftNeightbor(spans, "NUM", ["página", "pag", "p", "p.", "pág", "pág.", "fs", "art","art.", "arts", "arts.", "inciso", "artículo", "artículos", "inc"], -1)
        spans = filterEntsByLeftNeightbor(spans, "NUM", ["página", "pag", "p", "pág", "fs", "art", "arts", "inciso", "artículo", "artículos", "inc"], -2)
        spans = filterEntsByRightNeightbor(spans, "NUM", ["inc", "hs", "horas", "metros", "m", "gr", "grs", "gramos", "km", "kg", "cm"], 1)
        return spans