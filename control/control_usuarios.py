import logging
from logs import db, log_info, log_error  # Importamos la base de datos y las funciones de logging
from datetime import datetime

# Configuración básica de logging específica para control_usuarios.py
logging.basicConfig(
    filename='control_usuarios.log',  # Nombre del archivo de logs
    level=logging.INFO,  # Nivel de los mensajes de logging
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Obtener el logger configurado en este módulo
logger = logging.getLogger(__name__)

# Función para simular una operación de creación de usuario
def crear_usuario(nombre):
    try:
        # Aquí iría la lógica para crear un usuario en la base de datos o hacer cualquier operación
        # Vamos a simular un mensaje de información y un error para probar los logs
        log_info(f"Usuario '{nombre}' creado correctamente.")
        # Simular un error al intentar algo
        1 / 0  # Esto generará una excepción ZeroDivisionError
    except Exception as e:
        log_error(f"Error al crear usuario '{nombre}': {e}")
        # Aquí podrías manejar la excepción de manera apropiada

# Función principal que ejecuta algunas operaciones de usuario
def main():
    logger.info("Inicio del script control_usuarios.py")
    crear_usuario("Usuario1")
    logger.info("Fin del script control_usuarios.py")

if __name__ == '__main__':
    main()
