from etl.utils import *
from etl.utils.logger import Logger

def Transform_customer(df_customer):
    logger = Logger('etl.transform.Transform_customer').get_logger()
    logger.info("Inicio la transformacion de CUSTOMER")
    error = False
    error_message = ''

    try:
        #Cambiar nombre de las columnas a minusculas
        df_customer.columns = df_customer.columns.str.lower()
        
        #drop column innecesarias
        df_customer.drop(columns=['persona legal', 'dirección', 'indicativo', 'fecha de nacimiento'], axis=1, inplace=True)

        #ÖLimpiar el numero de telefono
        df_customer['celular'] = df_customer['celular'].str.strip()
        df_customer['celular'] = df_customer['celular'].str.replace(' ', '')
        df_customer.loc[df_customer['celular'].str.startswith('+57'), 'celular'] = (df_customer['celular'].str[3:])

        #Columnas object convertir a mayusculas
        for col in df_customer.columns:
            if df_customer[col].dtype in ['object']:
                df_customer[col] = df_customer[col].str.upper()
                df_customer[col] = df_customer[col].str.strip()

        df_customer['cliente'] = df_customer["nombre"] + df_customer["apellido"].fillna("").radd(" ")
        df_customer['cliente'] = df_customer['cliente'].str.strip()

        df_customer = df_customer.drop(columns=['nombre', 'apellido'])
        
        df_customer = df_customer.rename(columns={"fecha de creación": "creation_date", "correo electrónico": "email", "celular": "idCustomer", "¿como nos conociste?": "referral_source", "cliente": "customer_name"})
        df_customer = df_customer.drop_duplicates()
    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error: {error_message}')
    
    logger.info("Fin la transformacion de CUSTOMER")

    return {
        'error': error,
        'error_message': error_message,
        'customer_data': df_customer
    }