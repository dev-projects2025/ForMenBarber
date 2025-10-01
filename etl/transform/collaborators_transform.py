from etl.utils import *
from etl.utils.logger import Logger

def Transform_collaborator(df_collaborator):
    logger = Logger('etl.transform.Transform_collaborator').get_logger()
    logger.info("Inicio la transformacion de COLLABORATOR")
    error = False
    error_message = ''

    try:
        df_collaborator.columns = df_collaborator.columns.str.lower()
        df_collaborator = df_collaborator.rename(columns={'id_colaborador': "idCollaborator", 'nombre colaborador': 'name'})
        df_collaborator = df_collaborator.drop_duplicates()

        cols = ['idCollaborator', 'name']
        df_collaborator[cols] = df_collaborator[cols].astype(str)

        #Columnas object convertir a mayusculas
        for col in df_collaborator.columns:
            if df_collaborator[col].dtype in ['object']:
                df_collaborator[col] = df_collaborator[col].str.upper()
                df_collaborator[col] = df_collaborator[col].str.strip()

    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')
    
    logger.info("Fin la transformacion de COLLABORATOR")

    return {
        'error': error,
        'error_message': error_message,
        'collaborator_data': df_collaborator
    }