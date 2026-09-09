-- =====================================================================
-- DDL: Modelo Dimensional (Esquema Estrella) - Data Warehouse
-- Asignatura: Ingeniería de Datos
-- =====================================================================

-- Eliminar tablas existentes si se requiere reiniciar el esquema (orden inverso por FKs)
DROP TABLE IF EXISTS fact_applications CASCADE;
DROP TABLE IF EXISTS dim_candidates CASCADE;
DROP TABLE IF EXISTS dim_dates CASCADE;
DROP TABLE IF EXISTS dim_seniorities CASCADE;
DROP TABLE IF EXISTS dim_technologies CASCADE;
DROP TABLE IF EXISTS dim_countries CASCADE;

-- 1. Dimensión de Países
CREATE TABLE dim_countries (
    id_country SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);

-- 2. Dimensión de Tecnologías
CREATE TABLE dim_technologies (
    id_technology SERIAL PRIMARY KEY,
    technology_name VARCHAR(100) NOT NULL
);

-- 3. Dimensión de Nivel de Experiencia (Seniority)
CREATE TABLE dim_seniorities (
    id_seniority SERIAL PRIMARY KEY,
    seniority_level VARCHAR(50) NOT NULL
);

-- 4. Dimensión de Tiempo (Fecha)
CREATE TABLE dim_dates (
    id_date INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);

-- 5. Dimensión de Candidatos
CREATE TABLE dim_candidates (
    id_candidate SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150)
);

-- 6. Tabla de Hechos (Fact Applications)
CREATE TABLE fact_applications (
    id_fact SERIAL PRIMARY KEY,
    id_candidate INT REFERENCES dim_candidates(id_candidate),
    id_country INT REFERENCES dim_countries(id_country),
    id_technology INT REFERENCES dim_technologies(id_technology),
    id_seniority INT REFERENCES dim_seniorities(id_seniority),
    id_date INT REFERENCES dim_dates(id_date),
    yoe NUMERIC(4, 1),
    code_challenge_score NUMERIC(4, 2),
    technical_interview NUMERIC(4, 2),
    is_hired INT CHECK (is_hired IN (0, 1))
);
