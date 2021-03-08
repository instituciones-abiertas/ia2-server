from rest_framework.exceptions import APIException
from django.conf import settings


class ServiceOddDocumentUnavailable(APIException):
    status_code = 503
    default_detail = settings.ERROR_OODOCUMENT_NOT_WORKING
    default_code = "service_odddocument_unavailable"


class nameTooLong(APIException):
    status_code = 400
    default_detail = settings.ERROR_NAME_TOO_LONG
    default_code = "service_document"


class ActFileNotFound(APIException):
    status_code = 404
    default_detail = settings.ERROR_ACT_FILE_NOT_FOUND
    default_code = "act_file_not_found"


class ActNotExist(APIException):
    status_code = 404
    default_detail = settings.ERROR_ACT_NOT_EXIST
    default_code = "act_not_exist"


class StorageFileNotExist(APIException):
    status_code = 404
    default_detail = settings.ERROR_STORAGE_FILE_NOT_EXIST
    default_code = "storage_file_not_exist"


class DropboxExpireCredentials(APIException):
    status_code = 403
    default_detail = settings.ERROR_DROPBOX_CREDENTIALS
    default_code = "dropbox_credentials"


class DriveExpireCredentials(APIException):
    status_code = 403
    default_detail = settings.ERROR_DRIVE_CREDENTIALS
    default_code = "drive_credentials"


class DriveNotFoundCredentials(APIException):
    status_code = 404
    default_detail = settings.ERROR_DRIVE_CREDENTIALS_NOT_FOUND
    default_code = "drive_not_found_credentials"


class StorageCloudFolderNotExist(APIException):
    status_code = 404
    default_detail = settings.ERROR_STORAGE_CLOUD_FOLDER_NOT_EXIST
    default_code = "storage_cloud_folder_not_exist"
