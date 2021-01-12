import traceback
import sys
import mimetypes
import uuid
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from .exceptions import nameTooLong
import magic

ALLOW_DOCX_MIMETYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml": "docx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
    "application/zip": "docx",
}

ALLOW_MIMETYPES = {
    "application/msword": "doc",
    "application/vnd.oasis.opendocument.text": "odt",
}
ALLOW_MIMETYPES.update(ALLOW_DOCX_MIMETYPES)

ALLOW_EXTENSION = {"odt", "doc", "docx"}


def get_file_extension(fileField):
    unique_filename = "/tmp/" + str(uuid.uuid4())
    f = open(unique_filename, "wb")
    f.write(fileField._file.file.getvalue())
    filetype = magic.from_file(unique_filename, mime="True")
    f.close()
    os.remove(unique_filename)
    if filetype in ALLOW_MIMETYPES:
        return fileField
    else:
        traceback.print_exc(file=sys.stdout)
        raise ValidationError(settings.ERROR_TEXT_FILE_TYPE)


def name_length(fileField):
    if len(fileField.name) < 150:
        return fileField
    else:
        traceback.print_exc(file=sys.stdout)
        raise nameTooLong()


def is_docx_file(file):
    filetype = magic.from_file(file, mime="True")
    return filetype in ALLOW_DOCX_MIMETYPES
