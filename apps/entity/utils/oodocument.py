import logging
from django.conf import settings
from oodocument import oodocument
import os
import uuid
from django.core.exceptions import ImproperlyConfigured
from ..exceptions import ServiceOddDocumentUnavailable
from string import Template
from .general import open_file
from docx import Document


# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")

# Funcion deprecada,solo anonimiza,se reemplazo por anonimyzed_convert_document
def anonimyzed_text(path_document, path_output, data_to_replace, format_output, color=None):
    try:
        oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
        if color and isinstance(color, list) and len(color) == 3:
            r, g, b = color
            oo.set_font_back_color(r, g, b)
        oo.replace_with(data_to_replace, path_output, format_output)
    except Exception as e:
        logger.exception(e)
        raise ServiceOddDocumentUnavailable()
    else:
        oo.dispose()


def generate_data_for_anonymization(ocurrency_for_anonimyzation, text, replace_tpl):
    data = {}
    s = Template(replace_tpl)
    for ent in ocurrency_for_anonimyzation:
        if ent.should_anonymized:
            data[text[ent.startIndex : ent.endIndex]] = s.substitute(name=ent.entity.name)
    return data


def convert_document_to_format(path_document, output_path, output_format):
    try:
        oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
        oo.convert_to(output_path, output_format)
    except Exception as e:
        logger.exception(e)
        raise ServiceOddDocumentUnavailable()
    else:
        oo.dispose()


def extract_text_from_file(file_path):
    read_file = open_file(file_path, "r")
    read_result = read_file.read()
    return read_result


def anonimyzed_convert_document(
    path_document,
    path_output,
    format_output,
    data_to_replace,
    path_convert_document,
    format_convert_document,
    color=None,
):
    try:
        oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
        if color and isinstance(color, list) and len(color) == 3:
            r, g, b = color
            oo.set_font_back_color(r, g, b)
        oo.replace_with(data_to_replace, path_output, format_output)
        oo.convert_to(path_convert_document, format_convert_document)
    except Exception as e:
        logger.exception(settings.ERROR_STORAGE_FILE_NOT_EXIST)
        raise ServiceOddDocumentUnavailable()
    finally:
        oo.dispose()


# Utilizamos la libreria https://pypi.org/project/python-docx/
def extract_header(path_document):
    new_text = ""
    document = Document(path_document)
    section = document.sections[0]
    header = section.first_page_header
    for paragraph in header.paragraphs:
        # Agrega solo las lineas con contenido
        if paragraph:
            # Agrega un salto de linea despues de cada nuevo linea del encabezado
            new_text = new_text + "\n" + paragraph.text
    return new_text


# Función para convertir a formato docx y extraer el header (no utilizada aun)
def convert_and_extract_header(path_document):
    # Definicion de ruta
    output_path = settings.MEDIA_ROOT_TEMP_FILES + str(uuid.uuid4()) + "header.docx"
    # Conversion a docx
    convert_document_to_format(path_document, output_path, "docx")
    header_text = extract_header(output_path)
    # Borrado archivo temporal
    # os.remove(output_path)
    return header_text