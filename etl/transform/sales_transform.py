from etl.utils import *
from etl.utils.logger import Logger
from etl.utils.config.config import Settings
from etl.utils.postgres_connection import PostgresDB

def procesar_pagos(texto):
    if pd.isna(texto):
        return pd.Series([None, 0.0])
    
    tipos = []
    total = 0.0
    
    # separar por salto de línea
    for linea in texto.split("\n"):
        if ":" not in linea:
            continue
        tipo, monto = linea.split(":", 1)
        tipos.append(tipo.strip())
        
        # limpiar el monto → quitar símbolos, puntos de miles y usar punto decimal
        monto_clean = (
            monto.replace("$", "")
                 .replace(".", "")
                 .replace(",", ".")
                 .strip()
        )
        try:
            total += float(monto_clean)
        except:
            pass
    
    return pd.Series([", ".join(tipos), total])

def transaccions_productos(logger, db, remaining, products, gift = False):
    start_posi = 0
    products_transactions = pd.DataFrame()
    transactions = []

    if gift:
        start_posi = 1

    if start_posi == 1:
        try:
            product_id = db.obtener_campo(constants.ITEM_TBL, 'item_name', products[0], 'idItem')
            product_price = 0

        except Exception as e:
            logger.error(f'[Product details]No se pudo conectar a la base de datos. {e}')

        transactions.append({
            'idItem': product_id,
            'idCustomer': np.nan,
            'idCollaborator': np.nan,
            'payment_type': np.nan,
            'sale_date': np.nan,
            'quantity': 1,
            'total_amount': product_price,
        })

    
    for product in products[start_posi:]:
        try:
            product_id = db.obtener_campo(constants.ITEM_TBL, 'item_name', product, 'idItem')
            product_price = db.obtener_campo(constants.ITEM_TBL, 'idItem', product_id, 'price')
            number_of_products_paid = remaining // product_price
            remaining = remaining - (number_of_products_paid * product_price)

            transactions.append({
                'idItem': product_id,
                'idCustomer': np.nan,
                'idCollaborator': np.nan,
                'payment_type': np.nan,
                'sale_date': np.nan,
                'quantity': number_of_products_paid,
                'total_amount': (number_of_products_paid * product_price),
            })
            
            if remaining == 0:
                break

        except Exception as e:
            logger.error(f'[Product details]No se pudo conectar a la base de datos. {e}')

    
    products_transactions = pd.DataFrame(transactions)

    return products_transactions

def Transform_sale(df_sale):
    logger = Logger('etl.transform.Transform_sale').get_logger()
    logger.info("Inicio la transformacion de SALE")
    error = False
    error_message = ''
    df_items = pd.DataFrame()
    sales = pd.DataFrame()

    try:
        # Crear conexión
        db = PostgresDB(
            host="localhost",
            dbname=Settings.DB_NAME,
            user=Settings.DB_USER,
            password=Settings.DB_PWD,
            port=5432
        )

        df_sale.columns = df_sale.columns.str.lower()
        df_sale.columns = df_sale.columns.str.strip()

        #Filtrar Dataframe
        df_sale = df_sale[df_sale['estado'] != 'ANULADA']

        df_sale[['servicio', 'barbero']] = df_sale["servicios"].str.split('-', n=1, expand=True)

        #Normalizar producto. Quitar excesos
        '''df_sale['productos'] = (
            df_sale["productos"]
            .str.split("\n")                       # separar por saltos de línea
            .apply(lambda lista: [x.split("-")[0].strip() for x in lista])  # quedarnos con lo antes del "-"
            .str.join(',')                        # unir con coma
        )'''
        df_sale['productos'] = (
            df_sale["productos"]
            .fillna('')  # reemplazar NaN por cadena vacía
            .astype(str) # asegurar que todo sea string
            .str.split("\n")  
            .apply(lambda lista: [x.split("-")[0].strip() for x in lista if x.strip()])  
            .str.join(',')  
        )
        df_sale['productos'] = df_sale['productos'].str.strip()

        #print(df_sale)

        #Llenar nulos con un valor por defecto
        df_sale['productos'] = df_sale['productos'].fillna('NO PRODUCT')
        df_sale['barbero'] = df_sale['barbero'].fillna('NO COLLABORATOR')
        df_sale['servicio'] = df_sale['servicio'].fillna('NO SERVICE')

        #Normalizar medios de pago
        df_sale[["tipos_pago", "total_pago"]] = df_sale["medios de pago"].apply(procesar_pagos)

        #Eliminar columnas innecesarias
        df_sale = df_sale.drop(columns=['tipo de cortesía', 'servicios', 'medios de pago'])

        #Columnas object convertir a mayusculas
        for col in df_sale.columns:
            if df_sale[col].dtype in ['object']:
                df_sale[col] = df_sale[col].str.upper()
                df_sale[col] = df_sale[col].str.strip()

        try:
            # Establec conexion
            db.conectar()
            logger.info("Conexion establecida")
            
            # Normalizar cliente, producto, servicio, medio de pago y barbero
            for index, fila in df_sale.iterrows():

                #Normalizar el cliente
                try:
                    customerid = db.obtener_campo(constants.CUSTOMER_TBL, 'customer_name', fila["cliente"], 'idCustomer')
                    df_sale.at[index, "cliente"] = customerid
                        
                except Exception as e:
                    logger.error(f'No se pudo conectar a la base de datos. {e}')

                #Normalizar el barbero
                if str(fila['barbero']).strip() != 'NO COLLABORATOR':
                    try:
                        idCollaborator = db.obtener_campo(constants.COLLABORATOR_TBL, 'name', fila["barbero"], 'idCollaborator')
                        df_sale.at[index, "barbero"] = idCollaborator   
                            
                    except Exception as e:
                        logger.error(f'No se pudo conectar a la base de datos. {e}')

                #Normalizar el producto
                if str(fila['productos']).strip() == 'NO PRODUCT':
                    try:
                        idItem = db.obtener_campo(constants.ITEM_TBL, 'item_name', fila["productos"], 'idItem')
                        df_sale.at[index, "productos"] = idItem 
                            
                    except Exception as e:
                        logger.error(f'No se pudo conectar a la base de datos. {e}')

                #Normalizar el servicio
                if str(fila['servicio']).strip() != 'NO SERVICE':
                    try:
                        idItem = db.obtener_campo(constants.ITEM_TBL, 'item_name', fila["servicio"], 'idItem')
                        df_sale.at[index, "servicio"] = idItem    
                            
                    except Exception as e:
                        logger.error(f'No se pudo conectar a la base de datos. {e}')

            logger.info('Clientes, colaboradores y items normalizados')
        except Exception as e:
            logger.error(f'Error normalizacion: {e}')
        finally:
            db.cerrar()
            

        #Si el cliente no existe, no se considera la venta. Decision de Negocio
        df_sale = df_sale[df_sale['cliente'].notna()]

        #Separar las ventas de items (Productos y servicios)
        df_transactions = pd.DataFrame()

        try:
            # Establec conexion
            db.conectar()
            logger.info("Conexion establecida")
            
            # Normalizar cliente, producto, servicio, medio de pago y barbero
            for index, fila in df_sale.iterrows():
                number_of_services_paid = 0
                remaining = 0
                product_sales = np.nan
                service_sales = pd.DataFrame()

                #print(df_sale)
                
                if fila['servicio'] != 'NO SERVICE':
                    # Obtener el valor del servicio
                    try:
                        service_price = db.obtener_campo(constants.ITEM_TBL, 'idItem', fila['servicio'], 'price')
                        number_of_services_paid = fila['total_pago'] // service_price
                        remaining = fila['total_pago'] - (number_of_services_paid * service_price)

                        service = [{
                                    'idItem': fila['servicio'],
                                    'idCustomer': fila['cliente'],
                                    'idCollaborator': fila['barbero'],
                                    'payment_type': "MIXTO" if len(str(fila['tipos_pago']).split(',')) > 1 else fila['tipos_pago'],
                                    'sale_date': fila['fecha'],
                                    'quantity': number_of_services_paid,
                                    'total_amount': (number_of_services_paid * service_price),
                                }]
                        
                        service_sales = pd.DataFrame(service)
                        
                        products = str(fila['productos']).split(',')
                        product_sales = transaccions_productos(logger, db, remaining, products, gift = True)
                    except Exception as e:
                        logger.error(f'No se pudo conectar a la base de datos. {e}')

                elif fila['productos'] != 'NO PRODUCT':
                    products = str(fila['productos']).split(',')
                    product_sales = transaccions_productos(logger, db, fila['total_pago'], products, gift = False)
                    product_sales['idCollaborator'] = '0'

                product_sales['idCustomer'] = fila['cliente']
                product_sales['idCollaborator'] = fila['barbero']
                product_sales['payment_type'] = "MIXTO" if len(str(fila['tipos_pago']).split(',')) > 1 else fila['tipos_pago']
                product_sales['sale_date'] = fila['fecha']

                sales = pd.concat([sales, service_sales], ignore_index=True)

                if not product_sales.empty:
                    sales = pd.concat([sales, product_sales], ignore_index=True)           

            sales['idCollaborator'] = sales['idCollaborator'].fillna('0')
            sales['payment_type'] = sales['payment_type'].fillna('EFECTIVO')
            sales.loc[sales['idCollaborator'] == 'NO COLLABORATOR', 'idCollaborator'] = '0'

            sales = sales.dropna(subset=["idItem"])

            logger.info('Clientes, colaboradores y items normalizados')
        except Exception as e:
            logger.error(f'Error_1: {e}')
        finally:
            db.cerrar()

    except Exception as e:
        error = True
        error_message = e
        logger.error(f'Error_2: {error_message}')
    
    logger.info("Fin la transformacion de SALE")

    return {
        'error': error,
        'error_message': error_message,
        'sale_data': sales
    }