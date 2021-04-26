import spacy
import os
import plac
import random
import warnings
import time
import logging
import re

from django.conf import settings
from pathlib import Path
from spacy.util import minibatch, compounding, filter_spans
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from spacy.tokens import Span
from re import match, finditer
from functools import reduce

logger = logging.getLogger("django.server")
if settings.IA2_MODEL_FILE is None or not settings.IA2_MODEL_FILE:
    logger.error("No hay un modelo valido para utilizar")
    logger.error("Pone el nombre del paquete en la variable de ambiente IA2_MODEL_FILE")
    quit()
model_name = os.path.basename(settings.IA2_MODEL_FILE).split("-")[0]

DISABLE_ENTITIES = settings.IA2_DISABLED_ENTITIES


class Nlp:
    def __init__(self):
        self.nlp = spacy.load(model_name)
        self.doc = None

    def generate_doc(self, text):
        return self.nlp(text)

    def get_all_entities(self, text):
        self.doc = self.generate_doc(text)
        list_ents = list(self.doc.ents)
        return filter_entity(list_ents, DISABLE_ENTITIES)


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
    res = []
    if ents_filter:
        res = [ent for ent in ent_list if ent.label_ not in ents_filter]
    return res


def filter_ents(ent_list):
    res = filter_spans(ent_list)
    return res


def overlap_ocurrency(ent_start, ent_end, ocurrency):
    print(f"original ocurrency", {ocurrency.text})
    print(f"ocurrency.startIndex", {ocurrency.startIndex})
    print(f"ocurrency.endIndex", {ocurrency.endIndex})
    print(f"overlap?", {ocurrency.startIndex})
    print(f"ent_start", {ent_start})
    print(f"ent_end?", {ent_end})
    print(
        (ent_start >= ocurrency.startIndex and ent_end <= ocurrency.endIndex)
        or (ent_start <= ocurrency.endIndex and ent_end >= ocurrency.endIndex)
        or (ent_start >= ocurrency.startIndex)
        and (ent_end <= ocurrency.endIndex)
    )
    return (
        (ent_start >= ocurrency.startIndex and ent_end <= ocurrency.endIndex)
        or (ent_start <= ocurrency.endIndex and ent_end >= ocurrency.endIndex)
        or (ent_start >= ocurrency.startIndex)
        and (ent_end <= ocurrency.endIndex)
    )


def overlap_ocurrency_list(ent_start, ent_end, original_ocurrency_list):
    return any(overlap_ocurrency(ent_start, ent_end, ocurrency) for ocurrency in original_ocurrency_list)


def find_all_entities(text, ent, original_ent_list):
    nlp = Nlp()
    doc = nlp.generate_doc(text)
    # Encuentro el texto correspondiente a la entidad
    end_index = ent.endIndex
    start_index = ent.startIndex
    print(f"ent", {ent.startIndex})
    ent_text = doc.char_span(start_index, end_index)
    print(f"ent text", {ent_text})

    # en el doc busco las nuevas entidades que matcheen con el texto ent_text
    result = []
    for match in finditer(ent_text.text, doc.text):
        print(f"match", {match})
        if not overlap_ocurrency_list(match.span()[0], match.span()[1], original_ent_list):
            new_span = doc.char_span(match.span()[0], match.span()[1], ent.entity.name)
            result.append(new_span)
    print("result")
    print(result)
    return result
