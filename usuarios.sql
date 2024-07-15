-- Creamos usuarios para alumnos
DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..58 LOOP
        EXECUTE format('CREATE USER alumno%s WITH PASSWORD ''password%s'';', i, i);
        EXECUTE format('GRANT alumno TO alumno%s;', i);
    END LOOP;
END $$;

-- Asegurarse de que tienes una columna 'login' en tu tabla 'alumnos'
ALTER TABLE alumnos ADD COLUMN IF NOT EXISTS login VARCHAR(255);

-- Actualizar los registros de alumnos para incluir el login
DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..58 LOOP
        EXECUTE format('UPDATE alumnos SET login = ''alumno%s'' WHERE id = %s;', i, i);
    END LOOP;
END $$;

-- Crear usuarios para profesores
DO $$
DECLARE
    name_list TEXT[] := ARRAY['Mar', 'Flor', 'Nayara', 'Marifé', 'Álvaro', 'Nieves', 'Sofía'];
    name TEXT;
BEGIN
    FOREACH name IN ARRAY name_list
    LOOP
        -- Crear el usuario con el rol de profesor
        EXECUTE format('CREATE USER %I WITH PASSWORD %L;', name || 'profesor', name || 'armonia');
        -- Asignar el rol de profesor al usuario creado
        EXECUTE format('GRANT profesor TO %I;', name || 'profesor');
    END LOOP;
END $$;

ALTER TABLE profesores ADD COLUMN IF NOT EXISTS login VARCHAR(255);

--Actualizar la columna 'login' en la tabla 'profesores'
DO $$
DECLARE
    name_list TEXT[] := ARRAY['Mar', 'Flor', 'Nayara', 'Marifé', 'Álvaro', 'Nieves', 'Sofía'];
    name TEXT;
BEGIN
    FOREACH name IN ARRAY name_list
    LOOP
        -- Actualizar la columna 'login' en la tabla 'profesores'
        EXECUTE format('UPDATE profesores SET login = %L WHERE nombre = %L;', name || 'profesor', name);
    END LOOP;
END $$;

-- Crear usuario para admin
CREATE USER armoniaadmin WITH PASSWORD '56789spain';
GRANT admin TO armoniaadmin;
