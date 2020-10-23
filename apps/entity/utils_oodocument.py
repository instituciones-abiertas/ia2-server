from django.conf import settings
from oodocument.oodocument import oodocument


def anonimyzed_text(path_document,path_output,data_to_replace,format_output):
    oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
    oo.replace_with(data_to_replace,path_output, format_output)
    oo.dispose()

def generate_data_for_anonymization(ocurrency_for_anonimyzation,text,mask_text):
    data = {}
    print(ocurrency_for_anonimyzation)
    for ent in ocurrency_for_anonimyzation:
            if(ent.should_anonymized):         
               data[text[ent.startIndex:ent.endIndex]] = mask_text
    return data

def convert_document_to_format(path_document,output_path,output_format):
    oo = oodocument(path_document, host=settings.LIBREOFFICE_HOST, port=settings.LIBREOFFICE_PORT)
    oo.convert_to(output_path, output_format)
    oo.dispose()

def extract_text_from_file(file_path):
    read_file = open(file_path,"r")
    read_result = read_file.read()
    return(read_result)