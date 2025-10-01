import psycopg2
import pandas as pd
from etl.utils.logger import Logger

class PostgresDB:
    def __init__(self, host, dbname, user, password, port=5432):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.conn = None
        self.logger = Logger('etl.load.PostgresDB').get_logger()

    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.logger.info('Conexión exitosa a PostgreSQL')
        except Exception as e:
            self.logger.error(f'Error de conexión: {e}')

    def existe_registro(self, query, params=None):
        """Ejecuta un SELECT y devuelve True si existe al menos un registro"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                resultado = cur.fetchone()
                if resultado and resultado[0] > 0:
                    return True
                return False
        except Exception as e:
            self.logger.error(f"Error verificando existencia: {e}")
            self.conn.rollback()
            return False

    def leer_query(self, query, params=None):
        """Lee resultados en un DataFrame de pandas"""
        try:
            return pd.read_sql(query, self.conn, params=params)
        except Exception as e:
            self.logger.error(f'Error leyendo datos: {e}')
            return pd.DataFrame()
        
    def obtener_campo(self, tabla, campo_busqueda, valor_busqueda, campo_retorno):
        """
        Valida si un registro existe en la tabla y devuelve el valor de un campo definido.
        :param tabla: nombre de la tabla
        :param campo_busqueda: columna por la cual buscar (ej. 'email')
        :param valor_busqueda: valor a buscar (ej. 'usuario@mail.com')
        :param campo_retorno: columna que quieres devolver (ej. 'id_cliente')
        :return: valor encontrado o None si no existe
        """
        try:
            with self.conn.cursor() as cur:
                query = f"SELECT {campo_retorno} FROM {tabla} WHERE {campo_busqueda} = %s LIMIT 1"
                cur.execute(query, (valor_busqueda,))
                resultado = cur.fetchone()
                
                if resultado:
                    return resultado[0]   # Devuelve el valor de la columna
                else:
                    return None
        except Exception as e:
            self.logger.error(f"Error consultando {tabla}: {e}")
            self.conn.rollback()
            return None
        
    def insertar_dataframe(self, df, tabla):
        """
        Inserta un DataFrame en una tabla de PostgreSQL.
        Los nombres de columnas del DataFrame deben coincidir con los de la tabla.
        """
        try:
            cols = ",".join(df.columns)  # columnas de la tabla
            valores = ",".join(["%s"] * len(df.columns))  # placeholders
            query = f"INSERT INTO {tabla} ({cols}) VALUES ({valores})"
            
            with self.conn.cursor() as cur:
                for _, fila in df.iterrows():
                    try:
                        cur.execute(query, tuple(fila))
                        self.conn.commit()
                    except Exception as e:
                        self.logger.warning(f'ERROR {e}')
                        self.conn.rollback()
        except Exception as e:
            self.logger.error(f'Error insertando DataFrame: {e}')
            self.conn.rollback()

    def cerrar(self):
        if self.conn:
            self.conn.close()
            self.logger.info(f'Conexión cerrada')
