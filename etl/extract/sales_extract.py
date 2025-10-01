from etl.utils import *
from etl.utils.config.config import Settings
from etl.utils.logger import Logger

def Extract_sale(source_folder):
    
    logger = Logger('etl.extract.Extract_sale').get_logger()
    logger.info("Inicio la extracción de SALE")
    file_name = 'transacciones.xlsx'
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

    logger.info("Fin la extracción de SALE")

    return {
        'error': error,
        'error_message': error_message,
        'sale_data': df
    }