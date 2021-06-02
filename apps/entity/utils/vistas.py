from ..models import Entity, Act, OcurrencyEntity, ActStats
from ..utils.spacy import Nlp, filter_spans
from django.conf import settings
import uuid
import ast
import os
import logging
import collections
import re
from re import finditer
from time import time
from datetime import timedelta
from django.utils import timezone

from ..utils.oodocument import convert_document_to_format, extract_text_from_file, extract_header
from ..validator import is_docx_file
from ..exceptions import CreateActFileIsMissingException, CreateActFileNameIsTooLongException
from django.core.exceptions import ValidationError
from rest_framework.exceptions import UnsupportedMediaType

# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")


def timeit_save_stats(act, key):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    """

    def Inner(func):
        def wrapper(*args, **kwargs):
            start = time()
            r = func(*args, **kwargs)
            end = time()
            stats = {key: end - start}
            save_act_stats(act, stats)
            return r

        return wrapper

    return Inner


def save_act_stats(act, stats):
    if act:
        if not hasattr(act, "actstats"):
            s = ActStats(act=act)
        else:
            s = act.actstats
        for key, value in stats.items():
            setattr(s, key, timedelta(seconds=value))
        s.save()


def convert_to_txt(act):
    output_path = settings.MEDIA_ROOT_TEMP_FILES + "output.txt" + str(uuid.uuid4())
    # Transformo el archivo de entrada a txt para procesarlo
    convert_document_to_format(act.file.path, output_path, "txt")
    # Variable de entorno para activar
    act.text = extract_text_from_file(output_path)

    # Chequeo la variable definida, si es True y si ademas es una extension valida de docx
    if (
        settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION
        and ast.literal_eval(settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION)
        and is_docx_file(act.file.path)
    ):
        header_text = extract_header(act.file.path)
        # Agregado encabezado al texto y calculo de tamaño
        act.offset_header = len(header_text)
        act.text = header_text + "\n" + act.text

    os.remove(output_path)
    return act


def create_act(request_file):
    # Checks the file from the request is missing
    if request_file is False:
        raise CreateActFileIsMissingException()

    act = Act(file=request_file)

    try:
        act.full_clean()
    except ValidationError:
        logger.exception(settings.ERROR_TEXT_FILE_TYPE)
        raise UnsupportedMediaType(media_type=request_file.content_type, detail=settings.ERROR_TEXT_FILE_TYPE)
    except (CreateActFileNameIsTooLongException) as e:
        logger.exception(e)
        raise CreateActFileNameIsTooLongException()
    else:
        act.save()

    timeit_convert_to_txt = timeit_save_stats(act, "load_time")(convert_to_txt)
    act = timeit_convert_to_txt(act)

    act.save()

    return act


def format_span(span):
    new_ordered_dict = collections.OrderedDict()
    new_ordered_dict["start"] = span.start_char
    new_ordered_dict["end"] = span.end_char
    new_ordered_dict["tag"] = span.label_
    return new_ordered_dict


def format_spans(span_list):
    # retorna una lista de OrderedDict
    return list(map(format_span, span_list))


def find_ent_ocurrencies_in_upper_text(text, ents):
    found_texts = []
    upper_pattern= ['[A-ZÀ-ÿ][A-ZÀ-ÿ]+']
    for pattern in upper_pattern:
        match = re.findall(pattern, text)
        ex_cap_text = ' '.join(x.lower() for x in match)
        filtered_ents = list(filter(lambda ent: ent.text.lower() in ex_cap_text, ents))
        for ent in filtered_ents:
            found_texts.append({"text": ent.text, "entity_name": ent.label_})
    return found_texts


def get_entities_in_uppercase_text(doc, text, ents):
    result = []
    found_texts = find_ent_ocurrencies_in_upper_text(text, ents)
    for element in found_texts:
        found_text, entity_name = element.values()
        for match in finditer(found_text, text):
            new_span = doc.char_span(match.span()[0], match.span()[1], entity_name)
            if new_span and not overlap_ocurrency_list(new_span.start, new_span.end, ents, False):
                result.append(new_span)

    return result


def detect_entities(act):
    nlp = Nlp()
    ents = nlp.get_all_entities(act.text)
    ents_in_upper = get_entities_in_uppercase_text(nlp.doc, act.text, ents)
    if ents_in_upper:
        ents.extend(filter_spans(ents_in_upper))
    return format_spans(ents)


def overlap_ocurrency(ent_start, ent_end, ocurrency, use_index):
    ocurrency_start = ocurrency.startIndex if use_index else ocurrency.start
    ocurrency_end = ocurrency.endIndex if use_index else ocurrency.end
    return (
        (ent_start >= ocurrency_start and ent_end <= ocurrency_end)
        or (ent_start <= ocurrency_end and ent_end >= ocurrency_end)
        or (ent_start >= ocurrency_start)
        and (ent_end <= ocurrency_end)
    )


def overlap_ocurrency_list(ent_start, ent_end, original_ocurrency_list, use_index=True):
    return any(overlap_ocurrency(ent_start, ent_end, ocurrency, use_index) for ocurrency in original_ocurrency_list)


def find_all_spans_of_ocurrency(text, ent, original_ent_list):
    nlp = Nlp()
    doc = nlp.generate_doc(text)
    ent_text = doc.char_span(ent.startIndex, ent.endIndex).text
    # en el doc busco las nuevas entidades que matcheen con el texto ent_text
    # filtrando aquellas que overlapeen con las entidades originales
    result = []
    for match in finditer(ent_text, text):
        if not overlap_ocurrency_list(match.span()[0], match.span()[1], original_ent_list, True):
            new_span = doc.char_span(match.span()[0], match.span()[1], ent.entity.name)
            result.append(new_span)
    return result


def find_all_ocurrencies(text, original_ocurrencies, tag_list):
    # Filtro las ocurrencias cuyo nombre de tag coincide con los de las entidades sobre las que aplicar la funcionalidad de múltiple selección
    filtered_ocurrencies = list(filter(lambda x: (x.entity.id in tag_list), original_ocurrencies))
    new_ocurrencies = list(
        map(lambda ocurrency: find_all_spans_of_ocurrency(text, ocurrency, original_ocurrencies), filtered_ocurrencies)
    )
    result = filter_spans([ent for ent_list in new_ocurrencies for ent in ent_list])
    return format_spans(result)


def set_initial_review_time(act):
    s = act.actstats
    s.begin_review_time = timezone.now()
    s.save()


def calculate_and_set_elapsed_review_time(act):
    s = act.actstats
    s.review_time = timezone.now() - s.begin_review_time
    s.save()
