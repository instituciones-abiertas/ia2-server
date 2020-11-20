import spacy
import os
import plac
import random
import warnings
import time
from pathlib import Path
from spacy.util import minibatch, compounding

model_path = "./custom_models/modelo_poc"


class Spacy:
    nlp = spacy.load(model_path, disable=["tagger", "parser"])

    @classmethod
    def generate_doc(self, text):
        return self.nlp(text)


def get_all_entity_ner(text):
    doc = Spacy.generate_doc(text)
    return doc.ents


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