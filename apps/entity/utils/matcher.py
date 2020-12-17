from spacy.tokens import Span

patterns = {
            "CORREO_ELECTRÓNICO": [{"LIKE_EMAIL": True}],
            "NUM": [{"LIKE_NUM": True}],
        }

def add_matchers(matcher):
    # El mactch_id debe ser igual a el NOMBRE de la entidad
    for match_id, pattern in patterns.items():
        matcher.add(match_id, None, pattern)

def use_matchers(nlp, matcher, doc):
        if not doc:
            return None

        matches = matcher(doc)
        spans = []
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            spans.append(Span(doc, start, end, label))
        return spans