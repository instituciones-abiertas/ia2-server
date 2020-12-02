import spacy
import os
import plac
import random
import warnings
import time

from django.conf import settings
from pathlib import Path
from spacy.util import minibatch, compounding
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from re import match

model_path = "./custom_models/modelo_poc"
DISABLE_ENTITIES = settings.LIBERAJUS_DISABLE_ENTITIES


class Nlp:
    def __init__(self):
        self.nlp = spacy.load(model_path)
        self.matcher = Matcher(self.nlp.vocab)
        self.add_matchers()
        self.ruler = EntityRuler(self.nlp, overwrite_ents=True)
        self.text = None
        self.doc = None
        
        self.patterns = [
            {"label": "LEY", "pattern": [{"LOWER": "ley"}, {"LIKE_NUM": True}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "d.ddd.ddd"}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "dd.ddd.ddd"}]},
            {"label": "NUM_DNI", "pattern": [{"SHAPE": "ddd.ddd.ddd"}]},
            {"label": "NUM_IP", "pattern": [{"SHAPE": "ddd.ddd.ddd.ddd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dd-dddd-dddd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dddd-dddd"}]},
            {"label": "NUM_TELÉFONO", "pattern": [{"SHAPE": "dddd-ddd-dddd"}]},
            {"label": "FECHA_NUMÉRICA", "pattern": [{"SHAPE": "dd/dd/dd"}]},
            {"label": "FECHA_NUMÉRICA", "pattern": [{"SHAPE": "dd/dd"}]},
            {"label": "FECHA", "pattern": [{"LIKE_NUM": True}, {"POS": "ADP"}, {"LOWER": {"IN": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "noviembre", "diciembre"]}}, {"POS": "ADP", "OP": "?"}, {"LIKE_NUM": True, "OP": "?"}]},
            {"label": "NACIONALIDAD", "pattern": [{"LEMMA": {"IN": ["argentino", "boliviano", "paraguayo", "colombiano", "chileno", "brasileño", "panameño", "italiano", "español", "mexicano", "ruso", "francés", "inglés", "venezolano", "estadounidense", "alemán", "chino", "indio", "cubano", "nigeriano", "polaco", "sueco", "turco", "japonés", "portugués", "iraní", "paquistaní", "costarricense", "canadiense", "marroquí", "griego", "egipcio", "coreano", "ecuatoriano", "peruano", "guatemalteco", "salvadoreño", "holandés", "dominicano"]}}]},
            {"label": "NUM_CUIT_CUIL", "pattern":  [{"TEXT": {"REGEX": "(20|23|27|30|33)([0-9]{9}|-[0-9]{8}-[0-9]{1})"}}]},
        ]
        
        self.ruler.add_patterns(self.patterns)
        self.nlp.add_pipe(self.ruler)

    def add_matchers(self):
        patterns = {
            "CORREO_ELECTRÓNICO": [{"LIKE_EMAIL": True}],
            "NUM": [{"LIKE_NUM": True}],
        }

        # El mactch_id debe ser igual a el NOMBRE de la entidad
        for match_id, pattern in patterns.items():
            self.matcher.add(match_id, None, pattern)

    def use_matchers(self):
        if not self.doc:
            return None

        matches = self.matcher(self.doc)
        spans = []
        for match_id, start, end in matches:
            label = self.nlp.vocab.strings[match_id]
            spans.append(Span(self.doc, start, end, label))
        return spans

    def is_age(self, token, right_token, token_sent):
        return token.like_num and right_token.text == 'años' and 'edad' in token_sent.text

    def is_caseNumber(self, token, first_left_token, second_left_token, token_sent):
        return token.like_num and first_left_token.lower_ == 'nº' and second_left_token.lower_ == 'causa' 

    def is_last(self, token_id):
        return token_id == len(self.doc) -1
    
    def is_from_first_tokens(self, token_id):
        return token_id <= 2

    def use_rules(self, ents):
        if not self.doc:
            return None
        new_ents = []
        for token in self.doc:
            if  not self.is_last(token.i) and self.is_age(token, token.nbor(1), token.sent):
                new_ents.append(Span(self.doc, token.i, token.i + 1, label="EDAD"))
            if  not self.is_from_first_tokens(token.i) and self.is_caseNumber(token, token.nbor(-1), token.nbor(-2), token.sent):
                new_ents.append(Span(self.doc, token.i, token.i + 1, label="NUM_CAUSA"))
        return new_ents

    def filter_spans(self, spans, ents):
        def between(start, ents):
            for e in ents:
                if start >= e.start and start < e.end:
                    return True
            return False

        return [s for s in spans if not between(s.start, ents)]

    def generate_doc(self, text):
        self.text = text
        return self.nlp(text)


def get_all_entity_ner(text):
    doc = Spacy.generate_doc(text)
    return filter_entity(doc.ents, DISABLE_ENTITIES)


def get_risk(number):
    # Implementacion fake para pantalla
    if number < 10:
        return "bajo"
    elif number >= 10 and number < 30:
        return "medio"
    else:
        return "alto"


def train_data(training_data, n_iter, model_path):

    nlp = spacy.load(model_path)
    # load existing spaCy model

    # Agrega todas las labels que no existan al modelo
    # ner = nlp.get_pipe("ner")
    # for _, annotations in training_data:
    # for ent in annotations.get("entities"):
    # ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module="spacy")

        for itn in range(n_iter):
            random.shuffle(training_data)  # Se randomiza
            losses = {}
            #
            batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # save model to output directory
    output_dir = Path(model_path)
    nlp.to_disk(output_dir)


def write_model_test_in_file(filepath):
    model_path = filepath

    model = None
    with open(model_path, "r") as reader:
        model = reader.readlines()

    line_to_change = int(model[2])
    model[line_to_change] = f"{line_to_change}." + f"Call number {line_to_change - 3} changed this line.\n "
    increased_line_to_change = line_to_change + 1
    model[2] = f"{str(increased_line_to_change)}\n"
    print("EDITED MODEL")
    print(model)

    with open(model_path, "w") as reader:
        model = reader.writelines(model)


def filter_entity(ent_list, ents_filter):
    ents = [ent for ent in ent_list if ent.label_ not in ents_filter]
    return ents