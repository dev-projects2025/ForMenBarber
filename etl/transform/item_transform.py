from etl.utils import *
from etl.utils.logger import Logger

def Transform_item(servicios_df, productos_df):
    logger = Logger('etl.transform.Transform_customer').get_logger()
    logger.info("Inicio la transformacion de CUSTOMER")
    error = False
    error_message = ''
    df_items = pd.DataFrame()

    try:
        logger.info("Se transforman los servicios")
        servicios_df['item_type'] = 'SERVICIO'
        servicios_df = servicios_df.drop(columns=['cantidad', 'total'])
        
        logger.info("Se transforman los productos")
        productos_df['item_type'] = 'PRODUCTO'
        productos_df = productos_df.drop(columns=['cantidad', 'total', 'ganancias'])

        df_items = pd.concat([servicios_df, productos_df], ignore_index=True)

        logger.info("Se unifican servicios y productos")
        df_items = df_items[~df_items["item_name"].str.strip().str.upper().isin(['TOTAL', np.nan])]
        df_items['item_name'] = df_items['item_name'].str.upper()

        # Se resetea el indice
        df_items = df_items.reset_index(drop=True)

        df_items = df_items.rename(columns={"precio_unitario": "price"})
        df_items = df_items.drop_duplicates()

    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')
    
    logger.info("Fin la transformacion de CUSTOMER")

    return {
        'error': error,
        'error_message': error_message,
        'item_data': df_items
    }