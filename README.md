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

## Ejecucion del Proyecto

1. Instalar dependencias:
   python3 -m pip install -r requirements.txt

2. Ejecutar el pipeline:
   python3 src/etl_pipeline.py
