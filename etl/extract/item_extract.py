from etl.utils import *
from etl.utils.config.config import Settings
from etl.utils.logger import Logger
from etl.utils.helpers import extraer_subtabla

def Extract_items(source_folder):
    
    logger = Logger('etl.extract.Extract_items').get_logger()
    logger.info("Inicio la extracción de Items")
    file_name = 'reporte_general_Agosto.xlsx'
    df = pd.DataFrame()
    servicios_df = pd.DataFrame()
    productos_df = pd.DataFrame()
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

        # Read excel file based on the bytes. Skip first 5 rows only
        df = pd.read_excel(io.BytesIO(response), skiprows=5)
        df = df.reset_index(drop=True)

        logger.info("Se extraen los servicvios")
        # Extraer servicio
        servicios_df = extraer_subtabla(df, 'SERVICIO VENDIDOS', 'PRODUCTOS VENDIDOS')
        servicios_df.columns = ['item_name', 'precio_unitario', 'cantidad', 'total']

        logger.info("Se extraen los productos")
        # Extraer productos
        productos_df = extraer_subtabla(df, 'PRODUCTOS VENDIDOS', 'RESUMEN DE GASTOS')
        productos_df.columns = ['item_name', 'precio_unitario', 'cantidad', 'total', 'ganancias']

    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')

    logger.info("Fin la extracción de Items")

    return {
        'error': error,
        'error_message': error_message,
        'servicio_data': servicios_df,
        'producto_data': productos_df
    }