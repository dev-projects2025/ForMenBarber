import pandas as pd
import numpy as np
import re

def cargar_datos(archivo_excel):
    """Cargar datos desde archivo Excel"""
    try:
        # Cargar el archivo Excel
        df = pd.read_excel(archivo_excel, sheet_name='Transacciones')
        print(f"Datos cargados exitosamente: {len(df)} registros encontrados")
        return df
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {archivo_excel}")
        return None
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def entender_dataset(df):
    """
    Comprender el dataset: tamaño, primeros registros, tipos de datos y valores nulos.
    """
    print(f"\nTamaño del dataset: {df.shape[0]} filas, {df.shape[1]} columnas.\n")
    print("\nPrimeras filas del dataset:\n", df.head())
    print("\nInformacion del dataset:\n")
    print(df.info())
    print("\nValores nulos por columna:\n", df.isnull().sum())

def transformar_datos(df):
    """Aplicar todas las transformaciones solicitadas"""
    print("Aplicando transformaciones a los datos...")
    
    # Crear una copia para no modificar el original
    df_transformado = df.copy()
    
    # CONVERSIÓN EXPLÍCITA DE TIPOS DE VARIABLES
    
    # 1. Convertir Fecha a datetime y luego extraer solo la fecha
    print("1. Convirtiendo Fecha a tipo fecha...")
    df_transformado['Fecha'] = pd.to_datetime(df_transformado['Fecha'], errors='coerce').dt.date
    
    # 2. Convertir Valor Total a numérico
    print("2. Convirtiendo Valor Total a numérico...")
    df_transformado['Valor Total'] = (
        df_transformado['Valor Total']
        .astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .str.replace(' ', '', regex=False)
        .replace('', '0')
        .replace('nan', '0')
        .astype(float)
    )
    
    # 3. Convertir SOLO columnas categóricas apropiadas (NO Cliente)
    print("3. Convirtiendo columnas categóricas...")
    # Solo Estado debe ser categórica de las columnas originales
    if 'Estado' in df_transformado.columns:
        df_transformado['Estado'] = df_transformado['Estado'].astype('category')
    
    # 4. Separar columna Servicios en "servicio" y "barbero"
    print("4. Separando columna Servicios...")
    def separar_servicio_barbero(servicio):
        if pd.isna(servicio) or servicio == '':
            return pd.Series(['Sin servicio', 'Sin barbero'])
        
        # Buscar el patrón "servicio - barbero"
        match = re.search(r'(.+?)\s*-\s*([^-]+)$', str(servicio))
        if match:
            servicio_texto = match.group(1).strip()
            barbero_texto = match.group(2).strip()
            return pd.Series([servicio_texto, barbero_texto])
        else:
            # Si no encuentra el patrón, asumir que es solo servicio
            return pd.Series([str(servicio).strip(), 'Sin barbero'])
    
    # Aplicar la separación
    df_transformado[['Servicio', 'Barbero']] = df_transformado['Servicios'].apply(separar_servicio_barbero)
    
    # Convertir nuevas columnas categóricas (SÍ son apropiadas)
    df_transformado['Servicio'] = df_transformado['Servicio'].astype('category')
    df_transformado['Barbero'] = df_transformado['Barbero'].astype('category')
    
    # 5. Limpiar columna Productos (solo el nombre del producto, sin barbero)
    print("5. Limpiando columna Productos...")
    def limpiar_producto(producto):
        if pd.isna(producto) or producto == '':
            return 'Sin producto'
        
        producto_str = str(producto)
        
        # Manejar productos múltiples (separados por \n)
        if '\n' in producto_str:
            # Tomar solo el primer producto
            primer_producto = producto_str.split('\n')[0]
            # Limpiar el primer producto
            producto_limpio = re.sub(r'\s*-\s*[^-]+$', '', primer_producto.strip())
            return producto_limpio if producto_limpio else 'Sin producto'
        else:
            # Producto individual
            producto_limpio = re.sub(r'\s*-\s*[^-]+$', '', producto_str.strip())
            return producto_limpio if producto_limpio else 'Sin producto'
    
    df_transformado['Producto'] = df_transformado['Productos'].apply(limpiar_producto)
    df_transformado['Producto'] = df_transformado['Producto'].astype('category')  # SÍ es apropiado
    
    # 6. Eliminar columna "Tipo de Cortesía"
    print("6. Eliminando columnas innecesarias...")
    columnas_cortesia = ['Tipo de Cortesía', 'Tipo de Cortes�a']
    for columna in columnas_cortesia:
        if columna in df_transformado.columns:
            df_transformado = df_transformado.drop(columna, axis=1)
            print(f"   Columna {columna} eliminada")
    
    # 7. Transformar columna "Medios de Pago" a categórica
    print("7. Transformando Medios de Pago...")
    def categorizar_medio_pago(medio_pago):
        if pd.isna(medio_pago) or medio_pago == '':
            return 'No especificado'
        
        medio_pago_str = str(medio_pago).lower()
        
        if 'transferencia' in medio_pago_str:
            return 'Transferencia'
        elif 'efectivo' in medio_pago_str:
            return 'Efectivo'
        else:
            return 'Otro'
    
    df_transformado['Medio de Pago'] = df_transformado['Medios de Pago'].apply(categorizar_medio_pago)
    df_transformado['Medio de Pago'] = df_transformado['Medio de Pago'].astype('category')  # SÍ es apropiado
    
    # 8. Eliminar valor "Anulada" en columna "Estado"
    print("8. Filtrando transacciones...")
    registros_inicial = len(df_transformado)
    df_transformado = df_transformado[df_transformado['Estado'] != 'Anulada']
    registros_final = len(df_transformado)
    eliminados = registros_inicial - registros_final
    print(f"   Se eliminaron {eliminados} registros con estado 'Anulada'")
    
    # 9. Eliminar columnas originales que ya no necesitamos
    columnas_a_eliminar = ['Servicios', 'Productos', 'Medios de Pago']
    for columna in columnas_a_eliminar:
        if columna in df_transformado.columns:
            df_transformado = df_transformado.drop(columna, axis=1)
    
    # VERIFICACIÓN FINAL DE TIPOS DE DATOS
    print("\n=== VERIFICACIÓN DE TIPOS DE DATOS ===")
    print(df_transformado.dtypes)
    
    print("\nTransformaciones completadas exitosamente")
    return df_transformado
    
def realizar_EDA(df):    
    print("\n=== ANALISIS EXPLORATORIO DE DATOS ===\n")
    
    total_registros = len(df)
    
    # 1. Información general
    print("1. RESUMEN GENERAL:")
    print("\nEstado del dataset:")
    for columna in df.columns:
        no_nulos = df[columna].notna().sum()
        porcentaje = (no_nulos / total_registros) * 100
        print(f"  - {columna}: {no_nulos}/{total_registros} ({porcentaje:.1f}%)")
    
    # === VISUALIZACIONES ===
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # -------- 1. Histograma de Valor Total --------
    plt.figure(figsize=(8,5))
    sns.histplot(df['Valor Total'], bins=20, kde=True, color="skyblue")
    plt.title("Distribución del Valor Total de las Transacciones")
    plt.xlabel("Valor Total ($)")
    plt.ylabel("Frecuencia")
    plt.show()
    
    # -------- Ventas por día de la semana --------
    # Aseguramos que Fecha sea datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Crear columna con el nombre del día en español
    df['Día Semana'] = df['Fecha'].dt.day_name(locale='es_ES') \
                  if hasattr(df['Fecha'].dt, 'day_name') else df['Fecha'].dt.day_name()

    # Diccionario para traducir manualmente si tu sistema no soporta locale
    traducir_dias = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    df['Día Semana'] = df['Día Semana'].replace(traducir_dias)

    # Orden lógico de los días
    orden_dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    ventas_semana = df.groupby('Día Semana')['Valor Total'].sum().reindex(orden_dias)

    # Gráfica
    plt.figure(figsize=(8,5))
    sns.barplot(x=ventas_semana.index, y=ventas_semana.values, palette="viridis")
    plt.title("Ventas Totales por Día de la Semana")
    plt.xlabel("Día de la Semana")
    plt.ylabel("Valor Total ($)")
    plt.xticks(rotation=45)
    plt.show()

    # -------- 3. Clientes frecuentes --------
    clientes_top = df['Cliente'].value_counts().head(10)
    
    plt.figure(figsize=(8,5))
    sns.barplot(x=clientes_top.values, y=clientes_top.index, palette="magma")
    plt.title("Top 10 Clientes Frecuentes")
    plt.xlabel("Número de Transacciones")
    plt.ylabel("Cliente")
    plt.show()
    
    # -------- 4. Servicios más solicitados --------
    servicios_top = df['Servicio'].value_counts().head(10)
    
    plt.figure(figsize=(8,5))
    sns.barplot(x=servicios_top.values, y=servicios_top.index, palette="coolwarm")
    plt.title("Top Servicios más Solicitados")
    plt.xlabel("Número de Solicitudes")
    plt.ylabel("Servicio")
    plt.show()
    
    # -------- 5. Ingresos por barbero y cantidad de servicios ---
    ingreso_barbero = df.groupby('Barbero')['Valor Total'].sum().sort_values(ascending=False)
    conteo_barbero = df['Barbero'].value_counts()

    fig, ax1 = plt.subplots(figsize=(8,5))

    # Barras de ingresos
    sns.barplot(x=ingreso_barbero.index, y=ingreso_barbero.values, ax=ax1, color="steelblue")
    ax1.set_ylabel("Ingresos ($)", color="steelblue")
    ax1.set_xlabel("Barbero")
    ax1.set_title("Ingresos y Número de Servicios por Barbero")
    ax1.tick_params(axis='y', labelcolor="steelblue")

    # Línea de número de servicios
    ax2 = ax1.twinx()
    ax2.plot(conteo_barbero.index, conteo_barbero.values, color="darkred", marker="o", linewidth=2)
    ax2.set_ylabel("Número de Servicios", color="darkred")
    ax2.tick_params(axis='y', labelcolor="darkred")

    plt.show()

def guardar_datos_transformados(df, nombre_archivo):
    """Guardar los datos transformados a un nuevo archivo Excel"""
    try:
        df.to_excel(nombre_archivo, index=False)
        print(f"\nDatos transformados guardados en: {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar archivo: {e}")

# Función principal
def ejecutar_analisis_completo(ruta_archivo):
    
    # 1. Cargar datos
    df_original = cargar_datos(ruta_archivo)
    if df_original is None:
        return
    
    # 2. Entender dataset
    entender_dataset(df_original)
    
    # 3. Aplicar transformaciones
    df_transformado = transformar_datos(df_original)
    
    # 4. Mostrar estructura de datos transformados
    print("\n=== ESTRUCTURA DE DATOS TRANSFORMADOS ===")
    print(f"Columnas finales: {list(df_transformado.columns)}")
    print(f"Primeras 5 filas:")
    print(df_transformado.head())
        
    # 5. EDA
    realizar_EDA(df_transformado)
    
    # 6. Guardar datos transformados
    archivo_salida = "transacciones_transformadas.xlsx"
    guardar_datos_transformados(df_transformado, archivo_salida)
    
    print("ANALISIS COMPLETADO EXITOSAMENTE")
    
    return {
        'dataframe_original': df_original,
        'dataframe_transformado': df_transformado
    }

# EJECUTAR EL ANÁLISIS
if __name__ == "__main__":
    # Especifica la ruta de tu archivo Excel
    ruta_archivo = "transacciones.xlsx"
    
    # Ejecutar análisis completo
    resultados = ejecutar_analisis_completo(ruta_archivo)