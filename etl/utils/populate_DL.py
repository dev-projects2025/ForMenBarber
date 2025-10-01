"""
Este módulo configura un logger seguro que registra mensajes en consola y en archivo,
con rotación automática para evitar que el archivo crezca demasiado.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from minio import Minio
from minio.error import S3Error
from etl.utils.config.config import Settings
from etl.utils.constants import constants
from etl.utils.logger import Logger

def populate_dl(source_folder):
    logger = Logger('etl.transform.Transform_collaborator').get_logger()
    logger.info("Inicio la transformacion de COLLABORATOR")

    # Datos de conexión a MinIO
    MINIO_ENDPOINT = "localhost:9000"
    MINIO_ACCESS_KEY = Settings.MINIO_PWD
    MINIO_SECRET_KEY = Settings.MINIO_PWD
    BUCKET_NAME = constants.BUCKET

    # Ruta al folder
    BASE_PATH = constants.FILES_PATH
    logger.info("Base path %s", BASE_PATH)

    folder_path = os.path.join(BASE_PATH, source_folder).replace("\\", "/")
    logger.info("Folder to find %s", folder_path)

    # Validar existencia de la carpeta
    if os.path.isdir(folder_path):
        logger.info("Folder exists: %s", folder_path)

        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        # Cliente MinIO
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )

        # Crear bucket si no existe
        if not client.bucket_exists(BUCKET_NAME):
            client.make_bucket(BUCKET_NAME) 
            logger.info("Bucket '%s' creado", BUCKET_NAME)
        else:
            logger.info("Bucket '%s' ya existe", BUCKET_NAME)

        # Subir archivos si existen
        if files:
            for file_name in files:
                local_path = os.path.join(folder_path, file_name)
                object_name = file_name
                try:
                    client.fput_object(BUCKET_NAME, f'{source_folder}/{object_name}', local_path)
                    logger.info("Uploaded: %s → %s/%s", local_path, folder_path, object_name)
                except S3Error as e:
                    logger.error("Error subiendo %s: %s", file_name, e)
        else:
            logger.warning("Folder %s is empty.", folder_path)
    else:
        logger.warning("Folder does not exist: %s", folder_path)
