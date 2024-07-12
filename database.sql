-- Crear la tabla de profesores
CREATE TABLE IF NOT EXISTS profesores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Crear la tabla de alumnos con una referencia a la misma tabla para el campo familiar_id
CREATE TABLE IF NOT EXISTS alumnos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    familiar_id INT,
    CONSTRAINT fk_familiar
      FOREIGN KEY(familiar_id) 
	  REFERENCES alumnos(id)
);

-- Eliminar las columnas de teléfono y correo de la tabla alumnos si existen
ALTER TABLE alumnos 
DROP COLUMN IF EXISTS correo,
DROP COLUMN IF EXISTS telefono;

-- Crear la tabla de datos sensibles para almacenar el correo y el teléfono del alumno
CREATE TABLE IF NOT EXISTS datos_sensibles (
    alumno_id INT PRIMARY KEY,
    email VARCHAR(100),
    telefono VARCHAR(20),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
);

-- Crear o reemplazar la función para insertar un alumno junto con sus datos sensibles
CREATE OR REPLACE FUNCTION insert_alumno_with_sensitive_data(
    p_nombre VARCHAR(50),
    p_apellidos VARCHAR(50),
    p_edad INT,
    p_email VARCHAR(100),
    p_telefono VARCHAR(20),
    p_familiar_id INT DEFAULT NULL
) RETURNS INT AS $$
DECLARE
    new_alumno_id INT;
BEGIN
    -- Insertar en la tabla alumnos
    INSERT INTO alumnos (nombre, apellidos, edad, familiar_id)
    VALUES (p_nombre, p_apellidos, p_edad, p_familiar_id)
    RETURNING id INTO new_alumno_id;

    -- Insertar en la tabla datos_sensibles
    INSERT INTO datos_sensibles (alumno_id, email, telefono)
    VALUES (new_alumno_id, p_email, p_telefono);

    RETURN new_alumno_id;
END;
$$ LANGUAGE plpgsql;


-- Crear la tabla de clases
CREATE TABLE IF NOT EXISTS clases (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    profesor_id INT NOT NULL,
    precio_base DECIMAL(5,2) NOT NULL,
    tipo_pack VARCHAR(20) NOT NULL, -- pack1 para clases de 35€, pack2 para clases de 40€
    CONSTRAINT fk_profesor
      FOREIGN KEY(profesor_id) 
	  REFERENCES profesores(id)
);

-- Crear la tabla de niveles
CREATE TABLE IF NOT EXISTS niveles (
    id SERIAL PRIMARY KEY,
    clase_id INT NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    CONSTRAINT fk_clase
      FOREIGN KEY(clase_id) 
	  REFERENCES clases(id)
);

-- Crear la tabla de relación entre clases y profesores
CREATE TABLE IF NOT EXISTS clase_profesor (
    clase_id INT REFERENCES clases(id) ON DELETE CASCADE,
    profesor_id INT REFERENCES profesores(id) ON DELETE CASCADE,
    PRIMARY KEY (clase_id, profesor_id)
);


-- Crear la tabla de relación entre alumnos y clases
CREATE TABLE IF NOT EXISTS alumnos_clases (
    id SERIAL PRIMARY KEY,
    alumno_id INT NOT NULL,
    clase_id INT NOT NULL,
    nivel_id INT NOT NULL,
    CONSTRAINT fk_alumno
      FOREIGN KEY(alumno_id) 
	  REFERENCES alumnos(id),
    CONSTRAINT fk_clase
      FOREIGN KEY(clase_id) 
	  REFERENCES clases(id),
    CONSTRAINT fk_nivel
      FOREIGN KEY(nivel_id) 
	  REFERENCES niveles(id)
);

-- Crear la tabla de precios y descuentos
CREATE TABLE IF NOT EXISTS precios (
    id SERIAL PRIMARY KEY,
    tipo_pack VARCHAR(20) NOT NULL,
    precio_base DECIMAL(5,2) NOT NULL,
    descuento_segunda DECIMAL(5,2) NOT NULL,
    descuento_tercera DECIMAL(5,2) NOT NULL
);