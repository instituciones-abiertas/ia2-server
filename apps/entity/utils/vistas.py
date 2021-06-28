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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from ..utils.oodocument import convert_document_to_format, extract_text_from_file, extract_header
from ..validator import is_docx_file
from ..exceptions import CreateActFileIsMissingException, CreateActFileNameIsTooLongException
from django.core.exceptions import ValidationError
from rest_framework.exceptions import UnsupportedMediaType
from .general import check_exist_act
from ..tasks import train_model, extraer_datos_de_ocurrencias, reemplazo_asincronico_en_texto

# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")


def timeit_save_stats(func, *args, act_id=None, key=None):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    """

    def wrapper(*args, **kwargs):
        key = kwargs["key"]
        act_id = kwargs["act_id"]
        start = time()
        re = func(*args)
        end = time()
        stats = {key: end - start}
        print(stats)
        save_act_stats(act_id, stats)
        return re

    return wrapper


def save_act_stats(act_id, stats):
    if act_id:
        act = check_exist_act(act_id)
        if not hasattr(act, "actstats"):
            s = ActStats(act=act)
        else:
            s = act.actstats
        for key, value in stats.items():
            setattr(s, key, timedelta(seconds=value))
        s.save()


def create_proto_act(request_file):

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

    path = default_storage.save("tmp" + act.file.name, ContentFile(request_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    output_path = settings.MEDIA_ROOT_TEMP_FILES + "output.txt" + str(uuid.uuid4())
    # Transformo el archivo de entrada a txt para procesarlo
    convert_document_to_format(tmp_file, output_path, "txt")
    # Variable de entorno para activar
    act.text = extract_text_from_file(output_path)

    # Chequeo la variable definida, si es True y si ademas es una extension valida de docx
    if (
        settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION
        and ast.literal_eval(settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION)
        and is_docx_file(tmp_file)
    ):
        header_text = extract_header(tmp_file)
        # Agregado encabezado al texto y calculo de tamaño
        act.offset_header = len(header_text)
        act.text = header_text + "\n" + act.text
    # Borra archivos
    os.remove(tmp_file)
    os.remove(output_path)
    return act


@timeit_save_stats
def convert_to_txt(act):
    path_file = act.file.path.replace(" ", "_")  # TODO Mejorar la forma de obtner la url
    output_path = settings.MEDIA_ROOT_TEMP_FILES + "output.txt" + str(uuid.uuid4())
    # Transformo el archivo de entrada a txt para procesarlo
    convert_document_to_format(path_file, output_path, "txt")
    # Variable de entorno para activar
    act.text = extract_text_from_file(output_path)

    # Chequeo la variable definida, si es True y si ademas es una extension valida de docx
    if (
        settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION
        and ast.literal_eval(settings.IA2_ENABLE_OODOCUMENT_HEADER_EXTRACTION)
        and is_docx_file(path_file)
    ):
        header_text = extract_header(path_file)
        # Agregado encabezado al texto y calculo de tamaño
        act.offset_header = len(header_text)
        act.text = header_text + "\n" + act.text

    os.remove(output_path)
    return act


def create_act(request_file, generate_hash, text):
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
        act.text = text
        act.hashText = generate_hash
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
    upper_pattern = ["[A-ZÀ-ÿ][A-ZÀ-ÿ]+"]
    for pattern in upper_pattern:
        match = re.findall(pattern, text)
        ex_cap_text = " ".join(x.lower() for x in match)
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


def detect_entities(act, doc, ents):
    # FIXME se podría dejar de usar get_entities_in_uppercase_text si se hace la búsqueda por selección múltiple. REVISAR!
    ents_in_upper = get_entities_in_uppercase_text(doc, act.text, ents)
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


def find_all_spans_of_ocurrency(text, doc, ent, original_ent_list):
    char_span = doc.char_span(ent.startIndex, ent.endIndex)
    if not char_span:
        return []

    ent_text = char_span.text
    # en el doc busco las nuevas entidades que matcheen con el texto ent_text
    # filtrando aquellas que overlapeen con las entidades originales
    result = []
    for match in finditer(ent_text, text, flags=re.IGNORECASE):
        if not overlap_ocurrency_list(match.span()[0], match.span()[1], original_ent_list, True):
            new_span = doc.char_span(match.span()[0], match.span()[1], ent.entity.name)
            if new_span:
                result.append(new_span)
    return result


def find_all_ocurrencies(text, doc, original_ocurrencies, tag_list):
    # Filtro las ocurrencias cuyo nombre de tag coincide con los de las entidades sobre las que aplicar la funcionalidad de múltiple selección
    filtered_ocurrencies = list(filter(lambda x: (x.entity.id in tag_list), original_ocurrencies))
    new_ocurrencies = list(
        map(
            lambda ocurrency: find_all_spans_of_ocurrency(text, doc, ocurrency, original_ocurrencies),
            filtered_ocurrencies,
        )
    )
    result = filter_spans([ent for ent_list in new_ocurrencies for ent in ent_list])
    return format_spans(result)


@timeit_save_stats
def add_entities_by_multiple_selection(entity_list, act_check, doc, entities, human_mark):
    # Busco todas las multiples apariciones de las ocurrencias filtradas por el listado de tags

    all_ocurrencies_query = OcurrencyEntity.objects.filter(human_deleted_ocurrency=False, act=act_check)
    new_occurencies = find_all_ocurrencies(act_check.text, doc, all_ocurrencies_query, entity_list)
    create_new_occurrencies(new_occurencies, act_check, human_mark, entities)


def create_new_occurrencies(ocurrencies, act, human_mark, entity_list=[]):
    ocurrencies_to_create = []
    act_ocurrencies = OcurrencyEntity.objects.filter(act=act)

    for ocurrency in ocurrencies:
        # Si existe una ocurrencia que coinciden los indices se modifica y no se crea nueva.
        find_ocurrency = act_ocurrencies.filter(startIndex=ocurrency["start"], endIndex=ocurrency["end"])
        if find_ocurrency.exists():
            find_ocurrency.update(entity=entity_list.get(name=ocurrency["tag"]), human_marked_ocurrency=False)
        else:
            entity = entity_list.get(name=ocurrency["tag"])
            ocurrencies_to_create.append(
                OcurrencyEntity(
                    act=act,
                    startIndex=ocurrency["start"],
                    endIndex=ocurrency["end"],
                    entity=entity,
                    should_anonymized=entity.should_anonimyzation,
                    human_marked_ocurrency=human_mark,
                    text=act.text[ocurrency["start"] : ocurrency["end"]],
                )
            )
    OcurrencyEntity.objects.bulk_create(ocurrencies_to_create)


@timeit_save_stats
def detect_and_create_ocurrencies(act, all_entities):
    nlp = Nlp()
    ents = nlp.get_all_entities(act.text)

    ocurrencies = detect_entities(act, nlp.doc, ents)
    # Se crean las nuevas ocurrencias identificadas por el modelo
    create_new_occurrencies(ocurrencies, act, False, all_entities)

    if settings.USE_MULTIPLE_SELECTION_FROM_BEGINNING:
        entity_list_to_search = [ent.id for ent in all_entities if ent.enable_multiple_selection]
        add_entities_by_multiple_selection(
            entity_list_to_search, act, nlp.doc, all_entities, False, act_id=act.id, key="find_all_ocurrencies"
        )


def delete_and_save(ocurrency):
    ocurrency.human_deleted_ocurrency = True
    ocurrency.save()


def delete_ocurrencies(ocurrencies, act_check):
    ocurrencies_ids = [ocur["id"] for ocur in ocurrencies]
    ocurrencies_to_delete = OcurrencyEntity.objects.filter(id__in=ocurrencies_ids, act_id=act_check.id)
    list(map(delete_and_save, ocurrencies_to_delete))


def set_initial_review_time(act):
    s = act.actstats
    s.begin_review_time = timezone.now()
    s.save()


def calculate_and_set_elapsed_review_time(act):
    s = act.actstats
    s.review_time = timezone.now() - s.begin_review_time
    s.save()


@timeit_save_stats
def extraccion_de_datos(act_id):
    # En este metodo deberia implementar el calculo asincronico de tiempo para almacenar
    return extraer_datos_de_ocurrencias.apply_async([act_id])


@timeit_save_stats
def anonimizacion_de_documentos(*args):
    return reemplazo_asincronico_en_texto.apply_async([*args])


def remove_anonymus_previous_file(act, url):
    if act.anonymous_file:
        os.remove(act.anonymous_file.path)
    act.anonymous_file = url
    act.save()
    return
