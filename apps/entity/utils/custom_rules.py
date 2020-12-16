def is_age(token, right_token, token_sent):
    return token.like_num and right_token.text == 'años' and 'edad' in token_sent.text

def is_caseNumber(token, first_left_token, second_left_token, token_sent):
    return token.like_num and ((first_left_token.lower_ == 'nº' and second_left_token.lower_ == 'causa') or first_left_token.lower_ == 'caso')

def is_last(token_id, doc):
    return token_id == len(doc) -1

def is_from_first_tokens(token_id):
    return token_id <= 2

def is_judge(ent):
    first_token = ent[0]
    # si juez esta en la entidad, entonces borrar la palabra juez
    return ent.label_ in ['PER', 'LOC'] and (first_token.nbor(-1).lemma_ in ['juez', 'Juez'] or first_token.nbor(-2).lemma_ in ['juez', 'Juez'] or first_token.nbor(-2).lemma_ in ['juez', 'Juez']) or 'Juez' in ent.text

def is_secretary(ent):
    first_token = ent[0]
    return ent.label_ in ['PER', 'LOC'] and (first_token.nbor(-1).lemma_ in ['secretario', 'Secretario'] or first_token.nbor(-2).lemma_ in ['secretario', 'Secretario'] or first_token.nbor(-2).lemma_ in ['secretario', 'Secretario'])

from spacy.tokens import Span

def is_prosecutor(ent):
    first_token = ent[0]
    return ent.label_ in ['PER', 'LOC'] and (first_token.nbor(-1).lemma_ in ['fiscal', 'Fiscal, Fiscalía, fiscalía'] or first_token.nbor(-2).lemma_ in ['fiscal', 'Fiscal, Fiscalía, fiscalía'] or first_token.nbor(-2).lemma_ in ['fiscal', 'Fiscal, Fiscalía, fiscalía'])

def use_rules(doc, ents):
        if not doc:
            return None
        new_ents = []
        for token in doc:
            if  not is_last(token.i, doc) and is_age(token, token.nbor(1), token.sent):
                new_ents.append(Span(doc, token.i, token.i + 1, label="EDAD"))
            if  not is_from_first_tokens(token.i) and is_caseNumber(token, token.nbor(-1), token.nbor(-2), token.sent):
                new_ents.append(Span(doc, token.i, token.i + 1, label="NUM_CAUSA"))
        for ent in ents:
            if  not is_from_first_tokens(ent.start) and is_judge(ent):
                new_ents.append(Span(doc, ent.start, ent.end, label="JUEZ"))
            if  not is_from_first_tokens(ent.start) and is_secretary(ent):
                new_ents.append(Span(doc, ent.start, ent.end, label="SECRETARIX"))
            if  not is_from_first_tokens(ent.start) and is_prosecutor(ent):
                new_ents.append(Span(doc, ent.start, ent.end, label="FISCAL"))
        return new_ents