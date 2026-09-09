# Workshop 001 - Data Engineering

## Descripcion General
Desarrollo del taller práctico de ingeniería de datos enfocado en la implementación de un proceso ETL (Extracción, Transformación y Carga) y el modelado dimensional en esquema estrella utilizando Python, Pandas y PostgreSQL.

## Estructura del Repositorio
- data/raw/: Contiene el archivo CSV de datos originales.
- docs/: Documentación y entregables del taller.
- src/etl_pipeline.py: Script principal del proceso ETL.
- sql/kpi_queries.sql: Vistas y consultas SQL analíticas.
- .env: Credenciales y parámetros de conexión.
- requirements.txt: Dependencias de Python.
- sql/star_schema.sql: DDL con la creación de tablas del esquema estrella.
- sql/kpi_queries.sql: Vistas y consultas SQL analíticas.


## Despliegue e Infraestructura
El entorno de base de datos se encuentra desplegado bajo una arquitectura en la nube y conectividad segura:
- **Infraestructura:** Servidor virtual (VM) alojado en Google Cloud Platform (GCP).
- **Contenedorización:** Motor PostgreSQL (versión 16) ejecutándose en un contenedor Docker aislado (`db_etl_workshop`) en el puerto `5433`.
- **Conectividad de Red:** Conexión segura punto a punto establecida mediante una red virtual privada ZeroTier, permitiendo la comunicación directa sin exponer puertos públicos innecesarios hacia el exterior.

## Ejecucion del Proyecto

1. Instalar dependencias:
   python3 -m pip install -r requirements.txt

2. Ejecutar el pipeline ETL desde la máquina local:
   python3 src/etl_pipeline.py
