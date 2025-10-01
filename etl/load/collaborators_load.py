from etl.utils import *
from etl.utils.postgres_connection import PostgresDB
from etl.utils.constants import constants
from etl.utils.logger import Logger
from etl.utils.config.config import Settings

def Load_collaborator(df):
    logger = Logger('etl.load.Load_collaborator').get_logger()
    logger.info("Inicio la carga de COLLABORATOR")

    # Crear conexión
    db = PostgresDB(
        host=Settings.DB_ENDPOINT,
        dbname=Settings.DB_NAME,
        user=Settings.DB_USER,
        password=Settings.DB_PWD,
        port=5432
    )

    try:
        db.conectar()
        logger.info("Conexion establecida")

        df_new_items = pd.DataFrame()

        # Eliminar los registros existentes
        for idx, fila in df.iterrows():
            query = f'SELECT COUNT(*) FROM {constants.COLLABORATOR_TBL} WHERE idCollaborator = %s'
            if not db.existe_registro(query, (fila['idCollaborator'],)):
                df_new_items = pd.concat([df_new_items, pd.DataFrame([fila])], ignore_index=True)

        if len(df_new_items) > 0:
            db.insertar_dataframe(df_new_items, constants.COLLABORATOR_TBL)
            logger.info("Datos insertados")
        else:
            logger.info("No hay datos a insertar")
            
    except Exception as e:
        logger.error(f'No se pudo conectar a la base de datos. {e}')

    finally:
        db.cerrar()

    logger.info("Fin la carga de COLLABORATOR")