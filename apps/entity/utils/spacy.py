import spacy
import os
import plac
import random
import warnings
import time

from django.conf import settings
from pathlib import Path
from spacy.util import minibatch, compounding

model_path = "./custom_models/modelo_poc"
DISABLE_ENTITIES = settings.LIBERAJUS_DISABLE_ENTITIES


class Spacy:
    nlp = spacy.load(model_path, disable=["tagger", "parser"])

    @classmethod
    def generate_doc(self, text):
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