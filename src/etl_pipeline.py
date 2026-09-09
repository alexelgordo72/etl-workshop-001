import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
import os
from dotenv import load_dotenv

def extract_data(file_path):
    print("-> Leyendo el archivo CSV de candidatos...")
    # Usamos pandas para cargar el archivo plano
    dataframe = pd.read_csv(file_path, sep=',')
    return dataframe

def transform_data(df):
    print("-> Empezando la limpieza y transformación de los datos...")
    data = df.copy()

    # Renombramos las columnas a minúsculas y sin espacios para trabajar mejor en SQL
    data.rename(columns={
        'First Name': 'first_name', 
        'Last Name': 'last_name', 
        'Email': 'email',
        'Country': 'country', 
        'Application Date': 'application_date', 
        'Yoe': 'yoe',
        'Seniority': 'seniority', 
        'Technology': 'technology',
        'Code Challenge Score': 'code_challenge_score', 
        'Technical Interview': 'technical_interview'
    }, inplace=True)

    # Rellenamos valores nulos básicos para evitar errores en las consultas
    data['email'] = data['email'].fillna('sin_correo@dominio.com')
    data['seniority'] = data['seniority'].fillna('Not Specified')
    data['technical_interview'] = data['technical_interview'].fillna(0.0)
    
    # Ajuste por si hay notas de código en escala de 100 en lugar de 10
    data.loc[data['code_challenge_score'] == 100, 'code_challenge_score'] = 10

    # Limpieza de años de experiencia (Yoe): filtramos valores raros menores a 0 o mayores a 50
    datos_logicos = data[(data['yoe'] >= 0) & (data['yoe'] <= 50)]
    mediana_yoe = datos_logicos['yoe'].median()
    data.loc[data['yoe'] < 0, 'yoe'] = 0
    data.loc[data['yoe'] > 50, 'yoe'] = mediana_yoe
    data['yoe'] = data['yoe'].fillna(mediana_yoe)

    # Regla de negocio del taller: se contrata si ambos puntajes son mayores o iguales a 7
    def verificar_contratacion(fila):
        if fila['code_challenge_score'] >= 7 and fila['technical_interview'] >= 7:
            return 1
        return 0
            
    data['is_hired'] = data.apply(verificar_contratacion, axis=1)

    # Preparamos las fechas para la dimensión de tiempo
    data['application_date'] = pd.to_datetime(data['application_date'])
    data['id_date'] = data['application_date'].dt.strftime('%Y%m%d').astype(int)

    # Armamos las dimensiones del modelo estrella
    paises_unicos = data['country'].dropna().unique()
    dim_countries = pd.DataFrame({'id_country': range(1, len(paises_unicos) + 1), 'country_name': paises_unicos})

    tech_unicas = data['technology'].dropna().unique()
    dim_technologies = pd.DataFrame({'id_technology': range(1, len(tech_unicas) + 1), 'technology_name': tech_unicas})

    seniority_unicos = data['seniority'].dropna().unique()
    dim_seniorities = pd.DataFrame({'id_seniority': range(1, len(seniority_unicos) + 1), 'seniority_level': seniority_unicos})

    fechas_unicas = data[['application_date', 'id_date']].drop_duplicates()
    dim_dates = pd.DataFrame({
        'id_date': fechas_unicas['id_date'], 
        'full_date': fechas_unicas['application_date'].dt.date,
        'year': fechas_unicas['application_date'].dt.year, 
        'month': fechas_unicas['application_date'].dt.month,
        'day': fechas_unicas['application_date'].dt.day, 
        'quarter': fechas_unicas['application_date'].dt.quarter
    })

    dim_candidates = data[['first_name', 'last_name', 'email']].copy()
    dim_candidates['id_candidate'] = range(1, len(dim_candidates) + 1)

    # Cruzamos los datos para armar la tabla de hechos (fact table)
    fact = pd.merge(data, dim_countries, left_on='country', right_on='country_name', how='left')
    fact = pd.merge(fact, dim_technologies, left_on='technology', right_on='technology_name', how='left')
    fact = pd.merge(fact, dim_seniorities, left_on='seniority', right_on='seniority_level', how='left')
    fact['id_candidate'] = dim_candidates['id_candidate']

    fact_applications = fact[[
        'id_candidate', 'id_country', 'id_technology', 'id_seniority', 'id_date',
        'yoe', 'code_challenge_score', 'technical_interview', 'is_hired'
    ]]

    return {
        "dim_countries": dim_countries, 
        "dim_technologies": dim_technologies,
        "dim_seniorities": dim_seniorities, 
        "dim_dates": dim_dates,
        "dim_candidates": dim_candidates, 
        "fact_applications": fact_applications
    }

def load_to_postgres(diccionario_tablas):
    print("-> Conectando a la base de datos y cargando las tablas...")
    load_dotenv()
    
    usuario = os.getenv("DB_USER")
    password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    puerto = os.getenv("DB_PORT")
    bd = os.getenv("DB_NAME")

    # Armamos la cadena de conexión con SQLAlchemy
    url_conexion = f"postgresql://{usuario}:{password}@{host}:{puerto}/{bd}"
    motor = create_engine(url_conexion)

    lista_dimensiones = ["dim_countries", "dim_technologies", "dim_seniorities", "dim_dates", "dim_candidates"]
    
    # Guardamos todo en PostgreSQL usando pandas to_sql
    with motor.begin() as conexion:
        for tabla in lista_dimensiones:
            print(f"Subiendo tabla dimensión: {tabla}...")
            diccionario_tablas[tabla].to_sql(tabla, conexion, if_exists='replace', index=False)
        
        print("Subiendo tabla de hechos: fact_applications...")
        diccionario_tablas["fact_applications"].to_sql("fact_applications", conexion, if_exists='replace', index=False)
        
    print("-> ¡ETL completado con éxito!")

if __name__ == "__main__":
    # Obtenemos la ruta relativa para encontrar el archivo de datos sin líos de directorios
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(directorio_actual, "../data/raw/candidates.csv")
    
    # Ejecutamos las tres fases del ETL
    datos_crudos = extract_data(ruta_csv) 
    datos_transformados = transform_data(datos_crudos)
    load_to_postgres(datos_transformados)
