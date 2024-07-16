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
