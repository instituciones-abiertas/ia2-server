from publicador import Publicador, GoogleDrive, DropboxApi
import os
import logging
from django.conf import settings
from ..exceptions import DropboxExpireCredentials, DriveNotFoundCredentials, StorageCloudFolderNotExist

path_credentials_drive = settings.PUBLICADOR_CREDENTIALS_DRIVE_PATH
dropbox_token = settings.PUBLICADOR_DROPBOX_TOKEN_APP
# Uso de logger server de django, agrega
logger = logging.getLogger("django.server")


def publish_in_drive(file_path, path_in_drive):
    # Revisar que tipo de credenciales se necesitan
    context = Publicador(file_path, GoogleDrive(path_credentials_drive, path_in_drive))
    try:
        context.publicar()
    except Exception:
        logger.exception(settings.ERROR_DRIVE_CREDENTIALS_NOT_FOUND)
        raise DriveNotFoundCredentials()
    except BaseException as be:
        logger.exception(be)
        raise StorageCloudFolderNotExist()


def publish_in_dropbox(file_path, dropbox_path):
    # Revisar donde se debe agregar esa barra para que queda mas prolija
    context = Publicador(file_path, DropboxApi(dropbox_token, "/" + dropbox_path))
    try:
        context.publicar()
    except Exception:
        logger.exception(settings.ERROR_DROPBOX_CREDENTIALS)
        raise DropboxExpireCredentials()


def publish_in_both(file_path, folder_path):

    context = Publicador(file_path, GoogleDrive(path_credentials_drive, folder_path))
    context.publicar()
    context.strategy = DropboxApi(dropbox_token, folder_path)
    context.publicar()


def publish_document(file_path, folder_path, case):

    if case == "drive":
        publish_in_drive(file_path, folder_path)
    elif case == "dropbox":
        publish_in_dropbox(file_path, folder_path)
    else:
        publish_in_both(file_path, folder_path)
