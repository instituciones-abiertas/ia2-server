import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_UNDERLINE


def ActFileFixture(_file, file_name):
    return InMemoryUploadedFile(_file.buffer, "file", file_name, None, None, _file.buffer.tell(), None)
