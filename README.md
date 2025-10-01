# 💈FOR MEN BARBERSHOP💈  
## ✅ Universidad Autonoma del Occidente. Mi primera Chamba: Gestión y almacenamiento de Datos!

![LogoUni](https://www.uao.edu.co/wp-content/uploads/2021/03/reingreso.jpg)
<div align="justify">
Nuestro proyecto esta enfocado en implementar un flujo de ETL para consolidar y analizar datos transaccionales de la empresa 🔥Formen Barber Shop!🔥Los datos provienen de archivos XLSX, que contienen los movimientos de ventas y servicios. El Objetivo del proyecto es transformar la información a métricas visuales para la toma de decisiones del negocio usando herramientas tegnologicas como: MinIO, PostgreSQL, Docker, Github, PgAdmin, Drive, Power Bi y Visual Estudio Code (Python).👽
</div>

---

## 🌍 CONTEXTO DE LA EMPRESA

- 💇‍♂️**Nombre de la Barbería:** For men Barber Shop
- 🛍️**Ubicación:** Centro comercial Cañaveralejo
- 🕺**Ciudad:** Cali
- 💼**Años de Antigüedad:** 2
- 🪖**Empleados actuales:** 2

---

## 📂 Estructura del Proyecto

```plaintext
ETL_FormenBarbershop/
├── etl/           # Código Python por etapa
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── config/            # Parámetros de conexión y rutas
├── logs/              # Registro de ejecución
└── README.md          # Documentación del proyecto
```

---

## 🚀 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes herramientas:

- 🐍 **Python v3.13.2+** - Como lenguaje de programación. Recuerda instalar las librerías, que se encuentran definidas en el archivo Requeriments.txt 🌈:
  - minio==7.2.17
  - numpy==2.3.3
  - pandas==2.3.3
  - psycopg2==2.9.10
  - psycopg2_binary==2.9.10
  - python-dotenv==1.1.1
     
- 🐳 **Docker** – Para levantar contenedores de servicios en PostgreSQL, PgAdmin y MinIO.
- 📦 **MinIO** – Almacenamiento tipo S3 para el Data Lake.
- 🛢️ **PostgreSQL** – Base de datos relacional para la carga final.
- 💾 **Google Drive (modo escritorio)** – Para acceder a los archivos xlsx sincronizados localmente.
- 📊 **Power BI** – Para visualización de los datos cargados.
- 🤝 **PgAdmin** - Para administrar la base de datos.
- ⌨️ **Visual Estudio Code** - Para usar como editor de código.
   
- Crear el archivo .env y definir las siguientes variables:
  - DB_NAME
  - DB_USER
  - DB_PWD
  - DB_VOL
  - PGADMIN_USER
  - PGADMIN_PWD
  - PGADMIN_VOL
  - MINIO_USER
  - MINIO_PWD
  - MINIO_VOL_CONFIG
  - MINIO_VOL_OBJECTS
---

## 🐳 Levantar el Contenedor de Base de Datos

En la raíz del proyecto, ejecutar:

```bash
docker-compose up -d
```

🌐 Esto iniciará un contenedor con PostgreSQL en el puerto `5432`.

🔐 **Credenciales de conexión:**

- Host: `localhost`  
- Port: `5432`  
- Database: `bd`  
- User: `arq`  
- Password: `password`

---
## 📗 Configurar el Google Drive Desktop

En la raíz del pc, ejecutar el instalador del Drive:

```bash
https://support.google.com/a/users/answer/13022292?hl=es
```
---

## 🗄️ Proceso de Insert

En la unidad compartida del Drive se encuentran los archivos en formato CSV.  
Por medio de Python se aplicó la conexión con MinIO para insertar los datos en un Data Lake.  
El nombre del folder es **Raw**, donde diariamente se depositará el dataset.

---

## 🔥 Proceso de ETL

### 1. Extracción (`extract.py`)
- Fuente: Drive local (CSV o Excel)
- Herramienta: `pandas`
- Salida: `data/raw_data.csv`

```python
import pandas as pd
ruta = r"G:\Unidades compartidas\ManBarberShop\29092025\Reporte_Colaboradores.xlsx"
df = pd.read_excel(ruta)
df.to_csv("data/raw_data.csv", index=False)
```

---

### 2. Transformación (`transform.py`)
- Limpieza de filas vacías y totales
- Normalización de nombres de columnas
- Conversión de tipos

```python
df = pd.read_csv("data/raw_data.csv")
df = df[~df["Producto"].str.upper().isin(["TOTAL", ""])]
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.to_csv("data/clean_data.csv", index=False)
```

---

### 3. Carga (`load.py`)
- Destino: PostgreSQL
- Herramienta: `sqlalchemy` + `psycopg2`

```python
from sqlalchemy import create_engine
df = pd.read_csv("data/clean_data.csv")
engine = create_engine("postgresql+psycopg2://arq:password@localhost:5432/bd")
df.to_sql("stg1_principal", engine, if_exists="replace", index=False)
```

---

## 📈 Resultados esperados

- Power BI conectado a PostgreSQL  
- Dashboards con métricas de:

---


| OKR | KPI | Conclusión |
|:----------|:--------:|---------:|
| Incrementar la ocupación en días de baja demanda| Frecuencia de servicios por Barbero =(Número de servicios realizados)/(Número de barberos x Número de días de servicio)| Permite medir el nivel de ocupación que tiene cada barbero en promedio por cada día laborado. De esta manera, el propietario puede planificar cuantos turnos puede asignar máximos en un día y contemplar la capacidad operativa, exceso de personal o ineficiencia operativa|
| Mejorar el desempeño individual de cada barbero   | Promedio de atención de servicios Fórmula:(Número de servicios realizados /Número de servicios programados) | Esta formula brinda un panorama del cumplimiento de los servicios realizados vs los planificados. Por lo tanto, si encontramos un valor por encima de 1, se puede concluir como negativo, por qué no se está cumpliendo con la meta esperada por alguna de estas razones: ausencias, citas canceladas o incapacidad operativa. De lo contrario, si encontramos un valor inferior a 1, se percibe que durante la operación, existen servicios que se están realizando sin contar con una programación o cita previa |

- Meter una imagen del BI
---

## 🛡️ Control de Cambios

- Verificación de columnas requeridas (`Producto`, `Servicio`, `Clientes`, `Fecha`, `Valor Total`,`Medios de Pago`,`Estado`)  
- Control de errores por campos faltantes  
- Registro de errores en `logs/error.log`
- Backup del dataset.

---

## 👤 Autores

**BRAYAN STEVEN MAYOR**
**VICTOR JAVIER BUITRAGO VELASCO**
**CEO Asociación de Brayans de Colombia**
#Apasionados por la estadística aplicada, visualización efectiva y automatización de procesos analíticos.

---
