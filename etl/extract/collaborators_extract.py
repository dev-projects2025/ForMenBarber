from etl.utils import *
from etl.utils.config.config import Settings
from etl.utils.logger import Logger

def Extract_collaborator(source_folder):
    
    logger = Logger('etl.extract.Extract_collaborator').get_logger()
    logger.info("Inicio la extracción de COLLABORATOR")
    file_name = 'Reporte_Colaboradores.xlsx'
    df = pd.DataFrame()
    error = False
    error_message = ''

    try:
        # Set connection to Data Lake
        minio_client = MinioClient(
            endpoint=Settings.MINIO_ENDPOINT,
            access_key=Settings.MINIO_USER,
            secret_key=Settings.MINIO_PWD,
            secure=False
        )
        logger.info("Conexión establecida a MinIO")

        # Create bucket if not exists
        bucket = constants.BUCKET

        # Descargar objeto en memoria
        object_name = f'{source_folder}/{file_name}'
        response = minio_client.get_object(bucket, object_name)

        # Read excel file based on the bytes. Skip first 5 rows only
        df = pd.read_excel(io.BytesIO(response))

    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')

    logger.info("Fin la extracción de COLLABORATOR")

    return {
        'error': error,
        'error_message': error_message,
        'collaborator_data': df
    }