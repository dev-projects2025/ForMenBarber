# 💈FOR MEN BARBERSHOP💈  
## ✅ Universidad Autonoma del Occidente. Mi primera Chamba: Gestión y almacenamiento de Datos!

![LogoUni](https://www.uao.edu.co/wp-content/uploads/2021/03/reingreso.jpg)
<div align="justify">
Nuestro proyecto esta enfocado en implementar un flujo de ETL para consolidar y analizar datos transaccionales de la empresa 🔥Formen Barber Shop!🔥Los datos provienen de archivos XLSX, que contienen los movimientos de ventas y servicios. El Objetivo del proyecto es transformar la información a métricas visuales para la toma de decisiones del negocio usando herramientas tegnologicas como: MinIO, PostgreSQL, Docker, Github, PgAdmin, Drive, Power Bi y Visual Estudio Code (Python).👽
</div>

---

## 🌍 Información de la Empresa

- 💇‍♂️**Nombre de la Barbería:** For men Barber Shop
- 🛍️**Ubicación:** Centro comercial Cañaveralejo
- 🕺**Ciudad:** Cali
- 💼**Años de Antigüedad:** 2
- 🪖**Empleados actuales:** 2

---

## 📂 Estructura del Proyecto

```plaintext
ETL_FormenBarbershop/
├── etl/ # Módulo principal ETL
│ ├── extract/ # Scripts de extracción de datos
│ │ ├── collaborators_extract.py
│ │ ├── customers_extract.py
│ │ ├── item_extract.py
│ │ └── sales_extract.py
│ │
│ ├── load/ # Scripts de carga de datos
│ │ ├── collaborators_load.py
│ │ ├── customers_load.py
│ │ ├── item_load.py
│ │ └── sales_load.py
│ │
│ ├── transform/ # Scripts de transformación de datos
│ │ ├── collaborators_transform.py
│ │ ├── customers_transform.py
│ │ ├── item_transform.py
│ │ └── sales_transform.py
│ │
│ └── utils/ # Utilidades y configuración
│ ├── config/ # Configuración general
│ │ ├── config.py
│ │ └── init.py
│ │
│ ├── constants.py # Constantes globales
│ ├── helpers.py # Funciones auxiliares
│ ├── logger.py # Configuración de logs
│ ├── minio_connection.py # Conexión a MinIO
│ ├── populate_DL.py # Poblar Data Lake
│ ├── postgres_connection.py# Conexión a PostgreSQL
│ └── init.py
│
├── logs/ # Archivos de logs de ejecución
│
├── Scripts/ # Scripts auxiliares
│ └── Script.sql # Script SQL para base de datos
│
├── .env # Variables de entorno
├── .gitignore # Reglas de exclusión para Git
├── docker-compose.yaml # Orquestación de contenedores
├── main.py # Script principal de ejecución
└── requirements.txt # Dependencias del proyecto
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
- 📦 **MinIO** – Almacenamiento tipo S3 para el Data Lake (Se levanta en contenedor Docker).
- 🛢️ **PostgreSQL** – Base de datos relacional para la carga final (Se levanta en contenedor Docker).
- 🤝 **PgAdmin** - Para administrar la base de datos (Se levanta en contenedor Docker).
- 💾 **Google Drive (modo escritorio)** – Para acceder a los archivos xlsx sincronizados localmente.
- 📊 **Power BI** – Para visualización de los datos cargados.
- ⌨️ **Visual Estudio Code** - Para usar como editor de código.
   
- Crear el archivo .env en la raiz del proyecto y definir las siguientes variables:
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

## 🐳 Levantar los contenedores: MinIO, Postgres y Pgadmin

Definir las variables de entorno en el archivo .env:

🔐 **Variables de entorno MinIO:** Definir las variables de entorno MINIO_USER, MINIO_PWD, MINIO_VOL_CONFIG, MINIO_VOL_OBJECTS, MINIO_ENDPOINT

🔐 **Variables de entorno Postgres:** Definir las variables de entorno DB_NAME, DB_USER, DB_PWD, DB_VOL, DB_ENDPOINT

🔐 **Variables de entorno Postgres:** Definir las variables de entorno PGADMIN_USER, PGADMIN_PWD, PGADMIN_VOL

🔐 **Variables de entorno Generales:** Definir la variable de entorno FILES_PATH (Ruta donde se tomaran los archivos que se subiran al DataLake)


En la raíz del proyecto, ejecutar:

```bash
docker-compose up -d
```

---
## 📗 Configurar el Google Drive Desktop

Descargar Google Drive desktop desde el siguiente enlace:

```bash
https://support.google.com/a/users/answer/13022292?hl=es
```
---

## 🗄️ Ubicar los archivos dentro de una unidad compartida del drive

Los archivos a cargar son los siguientes:

1. **Clientes:** clientes_FMB.xlsx
2. **Colaboradores:** Reporte_Colaboradores.xlsx
3. **Productos y servicios:** reporte_general_Agosto.xlsx
4. **Ventas:** transacciones.xlsx

Los archivos deben de estar localizados en una carpeta nombrada de la siguiente manera DDMMYYYY. El proceso de ETL buscará únicamente los archivos dentro de la carpeta del día actual.

Se debe de setear en la variable de ambiente FILES_PATH el path anterior.

```plaintext
Carpeta con los archivos/
├── 01102025/ # Carpeta de archivos del día formato DDMMYYYY
│ ├── clientes_FMB.xlsx
│ ├── Reporte_Colaboradores.xlsx
│ ├── reporte_general.xlsx
│ ├── transacciones.xlsx
```

Ejemplo:

<img width="1077" height="228" alt="Files" src="https://github.com/user-attachments/assets/5062389e-4020-4af5-a141-8a539b22e361" />

Para este caso, **FILES_PATH**=C:\Gestion y almacenamiento\ETL\ManBarberShop

---

## 🗄️ Crear el modelo de DWH en la base de datos

Usando pgadmin, ejecutar el script /Scripts/Script.sql. Esto creará el modelo que soportará el DHW.

## 📊 Modelo de Datos

### **Customer**
- `idCustomer` (PK)
- `creation_date`
- `customer_name`
- `email`
- `referral_source`

### **Item**
- `idItem` (PK)
- `item_name`
- `item_type`
- `price`

### **Collaborator**
- `idCollaborator` (PK)
- `name`

### **Sales**
- `idSale` (PK)
- `idItem` (FK) → Item.idItem
- `idCustomer` (FK) → Customer.idCustomer
- `idCollaborator` (FK) → Collaborator.idCollaborator
- `payment_type`
- `sale_date`
- `quantity`
- `total_amount`
  

<img width="557" height="585" alt="ERD_Barbershop" src="https://github.com/user-attachments/assets/98808afd-3911-48f6-95ae-fb9550ce9da2" />

---

## 📈 Resultados esperados

<img width="975" height="731" alt="ForMenBarberShop" src="https://github.com/user-attachments/assets/4e9ed340-d3df-4d4a-9242-a9279c8d5b79" />

---


| OKR | KPI | Conclusión |
|:----------|:--------:|---------:|
| Incrementar la ocupación en días de baja demanda| Frecuencia de servicios por Barbero =(Número de servicios realizados)/(Número de barberos x Número de días de servicio)| Permite medir el nivel de ocupación que tiene cada barbero en promedio por cada día laborado. De esta manera, el propietario puede planificar cuantos turnos puede asignar máximos en un día y contemplar la capacidad operativa, exceso de personal o ineficiencia operativa|
| Mejorar el desempeño individual de cada barbero   | Promedio de atención de servicios Fórmula:(Número de servicios realizados /Número de servicios programados) | Esta formula brinda un panorama del cumplimiento de los servicios realizados vs los planificados. Por lo tanto, si encontramos un valor por encima de 1, se puede concluir como negativo, por qué no se está cumpliendo con la meta esperada por alguna de estas razones: ausencias, citas canceladas o incapacidad operativa. De lo contrario, si encontramos un valor inferior a 1, se percibe que durante la operación, existen servicios que se están realizando sin contar con una programación o cita previa |


<img width="961" height="537" alt="Main_View" src="https://github.com/user-attachments/assets/ff51cff3-7785-48cb-b7a6-31a3a15fa93a" />


<img width="947" height="534" alt="Barberos_clientes_View" src="https://github.com/user-attachments/assets/95dd0c32-d895-4d5f-89d8-540809d655c6" />


<img width="944" height="535" alt="Items_Medios_pago_View" src="https://github.com/user-attachments/assets/5e81ea69-0807-452e-9e62-7880b69d8640" />


---

## 🛡️ Control de Cambios

- Verificación de columnas requeridas (`Producto`, `Servicio`, `Clientes`, `Fecha`, `Valor Total`,`Medios de Pago`,`Estado`)  
- Control de errores por campos faltantes  
- Registro de errores en `logs/error.log`
- Backup del dataset.

---

## 👤 Autores

**Clarificador(es):** Andres Felipe Hernandez

**Ideador(es):** Brayan Steven Mayor

**Implementador(es):** Anderson Gallego - Victor Buitrago

**Desarrollador(es):** Juan Camilo Caicedo

**CEO Asociación de Brayans de Colombia**

#Apasionados por la estadística aplicada, visualización efectiva y automatización de procesos analíticos.

---
