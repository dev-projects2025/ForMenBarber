import os
from dotenv import load_dotenv

# Cargar archivo .env
load_dotenv()

class Settings:
    # Postgres configuration
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PWD = os.getenv('DB_PWD')
    DB_VOL = os.getenv('DB_VOL')
    DB_ENDPOINT = os.getenv('DB_ENDPOINT') #"localhost"

    # Pgadmin configuration
    PGADMIN_USER = os.getenv('PGADMIN_USER')
    PGADMIN_PWD = os.getenv('PGADMIN_PWD')
    PGADMIN_VOL = os.getenv('PGADMIN_VOL')

    # MinIO
    MINIO_USER = os.getenv('MINIO_USER')
    MINIO_PWD = os.getenv('MINIO_PWD')
    MINIO_VOL_CONFIG = os.getenv('MINIO_VOL_CONFIG')
    MINIO_VOL_OBJECTS = os.getenv('MINIO_VOL_OBJECTS')
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT') #"localhost:9000"

    FILES_PATH = os.getenv('FILES_PATH')