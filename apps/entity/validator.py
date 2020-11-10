import mimetypes,uuid,os
from django.conf import settings
from django.core.exceptions import ValidationError
from .exceptions import nameTooLong
import magic

ALLOW_MYMETYPES = {
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml': 'docx',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'application/zip': 'docx',
            'application/msword': 'doc',
            'application/vnd.oasis.opendocument.text': 'odt',
}
ALLOW_EXTENSION = { 'odt', 'doc', 'docx'}

def get_file_extension(fileField):
        unique_filename = '/tmp/'+str(uuid.uuid4())
        f = open(unique_filename, 'wb')
        f.write(fileField._file.file.getvalue())
        filetype = magic.from_file(unique_filename, mime='True')
        f.close()
        os.remove(unique_filename)
        if   filetype in ALLOW_MYMETYPES : 
           return fileField 
        else: 
            raise ValidationError(settings.ERROR_TEXT_FILE_TYPE)

def name_length(fileField):
    if   len(fileField.name) < 150 :
           return fileField
    else:
            raise nameTooLong()