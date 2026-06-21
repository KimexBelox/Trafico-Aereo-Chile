PROJECT_NAME = "Sistema BI Tráfico Aéreo Chile"

# ==========================================
# FUENTE DE DATOS
# ==========================================

CSV_URL = "https://datos.gob.cl/dataset/934b4b83-4fd4-476f-b8b4-ec5aa7e9157f/resource/23a54a1b-6234-4bfb-b45b-84fa147dc2ec/download/trafico.csv"

# ==========================================
# CARPETAS
# ==========================================

RAW_FOLDER = "Datos/Datos Crudos"

PROCESSED_FOLDER = "Datos/Procesados"

DOCUMENTATION_FOLDER = "Documentación"

SQL_FOLDER = "SQL"

LOG_FOLDER = "Logs"

# ==========================================
# ARCHIVOS
# ==========================================

RAW_FILE_NAME = "trafico_aereo.csv"

TRANSFORMED_FILE_NAME = "trafico_aereo_transformado.csv"

PROFILE_FILE_NAME = "Perfil_Inicial_Dataset.docx"

SQL_SCRIPT_NAME = "create_stg_trafico_aereo.sql"

# ==========================================
# SQL SERVER
# ==========================================

SQL_SERVER = "NELSONDIAZ"

DATABASE_NAME = "Portafolio_BI"

STAGING_SCHEMA = "stg"

STAGING_TABLE = "Trafico_Aereo"