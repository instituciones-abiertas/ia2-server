from ..models import Entity, Act, OcurrencyEntity, ActStats
from ..utils.spacy import Nlp
from django.conf import settings
import uuid
import ast
import os
import logging
from time import time
from datetime import timedelta
from ..utils.oodocument import convert_document_to_format, extract_text_from_file, extract_header
from ..validator import is_docx_file
from ..exceptions import nameTooLong, ActFileNotFound
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
    if request_file is False:
        # Caso excepcional ya que no se lanza una excepcion de sistema primero
        logger.error("No se adjunto el archivo")
        raise ActFileNotFound()

    # Creo el acta base
    act = Act(file=request_file)

    try:
        act.full_clean()
    except ValidationError:
        logger.exception(settings.ERROR_TEXT_FILE_TYPE)
        raise UnsupportedMediaType(media_type=request_file.content_type, detail=settings.ERROR_TEXT_FILE_TYPE)
    except (nameTooLong) as e:
        logger.exception(e)
        raise nameTooLong()
    else:
        act.save()

    timeit_convert_to_txt = timeit_save_stats(act, "load_time")(convert_to_txt)
    act = timeit_convert_to_txt(act)

    act.save()

    return act


def detect_entities(act):
    nlp = Nlp()
    ents = nlp.get_all_entities(act.text)
    # Traigo todas las entidades para hacer busquedas mas rapida
    entities = Entity.objects.all()
    # Guardo las ocurrencias para no tener que hacer una llamada  a la base despues
    all_ocurrency = []

    for ent in ents:
        entity_name = ent.label_
        entity = entities.get(name=entity_name)
        should_be_anonymized = entity.should_anonimyzation
        # Falta definir el nombre exacto del campo en el frontend
        ocurrency = OcurrencyEntity.objects.create(
            act=act,
            startIndex=ent.start_char,
            endIndex=ent.end_char,
            entity=entity,
            should_anonymized=should_be_anonymized,
            human_marked_ocurrency=False,
            text=ent.text,
        )
        all_ocurrency.append(ocurrency)
    return all_ocurrency
