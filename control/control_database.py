# database.py

import logging
from app import get_db_connection
import psycopg2

# Configurar el logger
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def execute_sql_script(script_file):
    """ Ejecuta un script SQL en la base de datos. """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            try:
                with open(script_file, 'r') as f:
                    sql_script = f.read()
                cursor.execute(sql_script)
                conn.commit()
                logger.info(f"Script {script_file} executed successfully.")
            except Exception as e:
                conn.rollback()
                logger.error(f"Error executing script {script_file}: {e}")

if __name__ == '__main__':
    script_file = 'database.sql'
    execute_sql_script(script_file)
