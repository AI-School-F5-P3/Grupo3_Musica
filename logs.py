# logs.py

import logging
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar SQLAlchemy para el modelo Log
db = SQLAlchemy()

# Definir el modelo Log
class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    level = db.Column(db.String(10))
    message = db.Column(db.Text)

    def __init__(self, level, message):
        self.level = level
        self.message = message

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

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

# Funciones de logging
def log_to_database(level, message):
    new_log = Log(level=level, message=message)
    new_log.save_to_db()

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
