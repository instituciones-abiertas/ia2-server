import spacy
import os
import plac
import random
import warnings
import time
import logging

from django.conf import settings
from pathlib import Path
from spacy.util import minibatch, compounding
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from re import match

logger = logging.getLogger("django.server")
if settings.IA2_MODEL_FILE is None or not settings.IA2_MODEL_FILE:
    logger.error("[Spacy] No model available. Please check the IA2_MODEL_FILE variable in your environment.")
    quit()
model_name = os.path.basename(settings.IA2_MODEL_FILE).split("-")[0]


class Nlp:
    def __init__(self):
        self.nlp = spacy.load(model_name)
        self.doc = None

    def generate_doc(self, text):
        return self.nlp(text)

    def get_all_entities(self, text):
        self.doc = self.generate_doc(text)
        list_ents = list(self.doc.ents)
        return [ent for ent in list_ents if ent.label_ not in settings.DISABLED_ENTITIES]


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
