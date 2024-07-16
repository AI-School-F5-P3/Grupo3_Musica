'''
def calcular_precio(cursor, alumno_id, clases):
    cursor.execute("SELECT COUNT(*) FROM alumnos WHERE familiar_id = %s", (alumno_id,))
    num_familiares = cursor.fetchone()[0]

    # Descuento por familiar
    descuento_familiar = 0.1 if num_familiares > 0 else 0.0

    total_precio = 0
    clases_ordenadas = sorted(clases, key=lambda x: x['precio_base'])

    for i, clase in enumerate(clases_ordenadas):
        precio = clase['precio_base']
        if i == 0:
            total_precio += precio
        elif i == 1:
            total_precio += precio * 0.5
        else:
            total_precio += precio * 0.25

    # Aplicar descuento familiar
    total_precio -= total_precio * descuento_familiar

    return total_precio
'''

# Aplicar un descuento del 10% en la variable precio si el atributo familiar_id de
# un alumno no está vacío en la base de datos:

def aplicar_descuento_familiar(cursor, alumno_id, precio):
    # Verificar si el alumno tiene un familiar_id asociado
    cursor.execute("SELECT familiar_id FROM alumnos WHERE id = %s", (alumno_id,))
    resultado = cursor.fetchone()
    
    # Si el alumno tiene un familiar_id, aplicar un descuento del 10%
    if resultado and resultado[0] is not None:
        precio_con_descuento = precio * 0.9  # Aplicar un 10% de descuento
        return precio_con_descuento
    else:
        return precio