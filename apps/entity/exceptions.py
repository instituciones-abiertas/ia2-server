from rest_framework.exceptions import APIException
from django.conf import settings

class ServiceOddDocumentUnavailable(APIException):
    status_code = 503
    default_detail = settings.ERROR_OODOCUMENT_NOT_WORKING
    default_code = 'service_odddocument_unavailable'