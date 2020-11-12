from django.conf import settings
from oodocument.oodocument import oodocument
from django.core.exceptions import ImproperlyConfigured
from .exceptions import ServiceOddDocumentUnavailable
from string import Template

def anonimyzed_text(path_document,path_output,data_to_replace,format_output):
    try:
        oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
        oo.replace_with(data_to_replace,path_output, format_output)
    except:
        raise ServiceOddDocumentUnavailable()
    else:
        oo.dispose()

def generate_data_for_anonymization(ocurrency_for_anonimyzation, text, replace_tpl):
    data = {}
    s = Template(replace_tpl)
    for ent in ocurrency_for_anonimyzation:
            if(ent.should_anonymized):
               data[text[ent.startIndex:ent.endIndex]] = s.substitute(name=ent.entity.name)
    return data

def convert_document_to_format(path_document,output_path,output_format):
    try:
        oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
    except:
        raise ServiceOddDocumentUnavailable()
    else:
        oo.convert_to(output_path, output_format)
        oo.dispose()

def extract_text_from_file(file_path):
    read_file = open(file_path,"r")
    read_result = read_file.read()
    return(read_result)
