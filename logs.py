import logging # Módulo estándar de Python para registrar eventos.
import psycopg2 # Librería para interactuar con bases de datos PostgreSQL.
import os # Módulo para interactuar con el sistema operativo.
from dotenv import load_dotenv
from datetime import datetime

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configuración básica de logging
logging.basicConfig(
    filename='app.log',  # Nombre del archivo de logs
    level=logging.INFO,  # Nivel de los mensajes de logging
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Configurar un logger para la aplicación Flask
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)

# Configurar un manejador para enviar logs a la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Conexión a la base de datos PostgreSQL con psycopg2
conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cursor = conn.cursor()

# Funciones de logging para insertar en la base de datos
def log_to_database(level, message):
    timestamp = datetime.now().isoformat()
    try:
        cursor.execute("""
            INSERT INTO logs (timestamp, level, message)
            VALUES (%s, %s, %s)
        """, (timestamp, level, message))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f'Error al guardar log en la base de datos: {str(e)}')

def log_debug(message):
    logger.debug(message)
    log_to_database('DEBUG', message)

def log_info(message):
    logger.info(message)
    log_to_database('INFO', message)

def log_warning(message):
    logger.warning(message)
    log_to_database('WARNING', message)

def log_error(message):
    logger.error(message)
    log_to_database('ERROR', message)

def log_critical(message):
    logger.critical(message)
    log_to_database('CRITICAL', message)
