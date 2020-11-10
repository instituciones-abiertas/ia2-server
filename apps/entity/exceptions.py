from rest_framework.exceptions import APIException
from django.conf import settings

class ServiceOddDocumentUnavailable(APIException):
    status_code = 503
    default_detail = settings.ERROR_OODOCUMENT_NOT_WORKING
    default_code = 'service_odddocument_unavailable'

class nameTooLong(APIException):
    status_code = 400
    default_detail = settings.ERROR_NAME_TOO_LONG
    default_code = 'service_document'

class ActFileNotFound(APIException):
    status_code = 404
    default_detail = settings.ERROR_ACT_FILE_NOT_FOUND
    default_code = 'act_file_not_found'

class DropboxExpireCredentials(APIException):
    status_code = 401
    default_detail = settings.ERROR_DROPBOX_CREDENTIALS
    default_code = 'dropbox_credentials'