import psycopg2
import logging

# Configuración básica de logging
logging.basicConfig(
    filename='control_gestion_de_permisos.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Obtener el logger configurado en este módulo
logger = logging.getLogger(__name__)

# Función para ejecutar el script SQL desde un archivo
def execute_sql_script(script_file):
    try:
        with open(script_file, 'r') as f:
            sql_script = f.read()
        
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            conn.commit()
            logger.info(f"Script {script_file} executed successfully.")
    except Exception as e:
        logger.error(f"Error executing script {script_file}: {e}")
    finally:
        conn.close()

# Script principal para ejecutar todas las operaciones
def main():
    sql_file = 'gestion_de_permisos.sql'
    execute_sql_script(sql_file)

if __name__ == '__main__':
    main()
