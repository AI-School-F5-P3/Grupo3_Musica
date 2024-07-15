# control/control_insertar_datos.py

from control.logs import log_info, log_error
from control.control_database import get_db_connection

def insertar_alumno(nombre, apellidos, edad, familiar_id=None):
    sql = f"INSERT INTO alumnos (nombre, apellidos, edad, familiar_id) VALUES ('{nombre}', '{apellidos}', {edad}, {familiar_id});"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha insertado un nuevo alumno: {nombre} {apellidos}")
    except Exception as e:
        log_error(f"Error al insertar alumno {nombre} {apellidos}: {e}")
    finally:
        conn.close()

def insertar_profesor(nombre):
    sql = f"INSERT INTO profesores (nombre) VALUES ('{nombre}');"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha insertado un nuevo profesor: {nombre}")
    except Exception as e:
        log_error(f"Error al insertar profesor {nombre}: {e}")
    finally:
        conn.close()

def insertar_familiar(nombre, apellidos, edad):
    sql = f"INSERT INTO familiares (nombre, apellidos, edad) VALUES ('{nombre}', '{apellidos}', {edad});"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha insertado un nuevo familiar: {nombre} {apellidos}")
    except Exception as e:
        log_error(f"Error al insertar familiar {nombre} {apellidos}: {e}")
    finally:
        conn.close()

def insertar_nivel(clase_id, nivel):
    sql = f"INSERT INTO niveles (clase_id, nivel) VALUES ({clase_id}, '{nivel}');"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha insertado un nuevo nivel para la clase {clase_id}: {nivel}")
    except Exception as e:
        log_error(f"Error al insertar nivel para la clase {clase_id}: {e}")
    finally:
        conn.close()

def insertar_clase(nombre, profesor_id, precio_base, tipo_pack):
    sql = f"INSERT INTO clases (nombre, profesor_id, precio_base, tipo_pack) VALUES ('{nombre}', {profesor_id}, {precio_base}, '{tipo_pack}');"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha insertado una nueva clase: {nombre} (Profesor ID: {profesor_id})")
    except Exception as e:
        log_error(f"Error al insertar clase {nombre}: {e}")
    finally:
        conn.close()

def insertar_alumno_clase(alumno_id, clase_id, nivel_id):
    sql = f"INSERT INTO alumnos_clases (alumno_id, clase_id, nivel_id) VALUES ({alumno_id}, {clase_id}, {nivel_id});"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha asignado la clase {clase_id} al alumno {alumno_id}")
    except Exception as e:
        log_error(f"Error al asignar clase {clase_id} al alumno {alumno_id}: {e}")
    finally:
        conn.close()

def insertar_clase_profesor(clase_id, profesor_id):
    sql = f"INSERT INTO clase_profesor (clase_id, profesor_id) VALUES ({clase_id}, {profesor_id});"
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            log_info(f"Se ha asignado el profesor {profesor_id} a la clase {clase_id}")
    except Exception as e:
        log_error(f"Error al asignar profesor {profesor_id} a la clase {clase_id}: {e}")
    finally:
        conn.close()
