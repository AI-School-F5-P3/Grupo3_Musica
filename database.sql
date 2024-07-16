-- database.sql

-- Extensiones y creación de tablas
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(10) NOT NULL,
    message TEXT
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS profesores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS alumnos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    familiar_id INT,
    CONSTRAINT fk_familiar
      FOREIGN KEY(familiar_id) 
      REFERENCES alumnos(id)
);

ALTER TABLE alumnos 
DROP COLUMN IF EXISTS correo,
DROP COLUMN IF EXISTS telefono;

CREATE TABLE IF NOT EXISTS datos_sensibles (
    alumno_id INT PRIMARY KEY,
    email VARCHAR(100),
    telefono VARCHAR(20),
    FOREIGN KEY (alumno_id) REFERENCES alumnos(id)
);

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
    INSERT INTO alumnos (nombre, apellidos, edad, familiar_id)
    VALUES (p_nombre, p_apellidos, p_edad, p_familiar_id)
    RETURNING id INTO new_alumno_id;

    INSERT INTO datos_sensibles (alumno_id, email, telefono)
    VALUES (new_alumno_id, p_email, p_telefono);

    RETURN new_alumno_id;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS alumnos3 (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    edad INT NOT NULL,
    familiar_id INT,
    CONSTRAINT fk_familiar
      FOREIGN KEY(familiar_id) 
      REFERENCES alumnos(id)
);


CREATE TABLE IF NOT EXISTS clases (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    profesor_id INT NOT NULL,
    precio_base DECIMAL(5,2) NOT NULL,
    tipo_pack VARCHAR(20) NOT NULL,
    CONSTRAINT fk_profesor
      FOREIGN KEY(profesor_id) 
      REFERENCES profesores(id)
);

CREATE TABLE IF NOT EXISTS niveles (
    id SERIAL PRIMARY KEY,
    clase_id INT NOT NULL,
    nivel VARCHAR(20) NOT NULL,
    CONSTRAINT fk_clase
      FOREIGN KEY(clase_id) 
      REFERENCES clases(id)
);

CREATE TABLE IF NOT EXISTS clase_profesor (
    clase_id INT REFERENCES clases(id) ON DELETE CASCADE,
    profesor_id INT REFERENCES profesores(id) ON DELETE CASCADE,
    PRIMARY KEY (clase_id, profesor_id)
);

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

CREATE TABLE IF NOT EXISTS precios (
    id SERIAL PRIMARY KEY,
    tipo_pack VARCHAR(20) NOT NULL,
    precio_base DECIMAL(5,2) NOT NULL,
    descuento_segunda DECIMAL(5,2) NOT NULL,
    descuento_tercera DECIMAL(5,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS inscripciones (
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

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    login VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL
);

-- Añadir algunos usuarios
INSERT INTO usuarios (login, password, rol) VALUES
('armoniaadmin', crypt('56789spain', gen_salt('bf')), 'admin'),
('Marprofesor', crypt('Mararmonia', gen_salt('bf')), 'profesor'),
('Florprofesor', crypt('Florarmonia', gen_salt('bf')), 'profesor');