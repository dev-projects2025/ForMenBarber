from etl.utils import *
from etl.utils.config.config import Settings
from etl.utils.logger import Logger

def Extract_customer(source_folder):
    
    logger = Logger('etl.extract.Extract_customer').get_logger()
    logger.info("Inicio la extracción de CUSTOMER")
    file_name = 'clientes_FMB.xlsx'
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
        minio_client.create_bucket(bucket)

        # Descargar objeto en memoria
        object_name = f'{source_folder}/{file_name}'
        response = minio_client.get_object(bucket, object_name)
        #data_customer = response.read()

        # Read excel file based on the bytes. Skip first 5 rows only
        df = pd.read_excel(io.BytesIO(response), skiprows=5)
        df = df.reset_index(drop=True)

        # Drop first column
        df = df.drop('Unnamed: 0', axis=1)
    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')

    logger.info("Fin la extracción de CUSTOMER")

    return {
        'error': error,
        'error_message': error_message,
        'customer_data': df
    }