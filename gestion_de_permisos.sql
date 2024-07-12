CREATE ROLE admin WITH LOGIN SUPERUSER;
CREATE ROLE profesor WITH LOGIN;
CREATE ROLE alumno WITH LOGIN;

CREATE OR REPLACE FUNCTION get_user_role()
RETURNS VARCHAR AS $$
DECLARE
    user_role VARCHAR;
BEGIN
    IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = CURRENT_USER AND rolsuper) THEN
        user_role := 'admin';
    ELSIF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = CURRENT_USER AND rolname = 'profesor') THEN
        user_role := 'profesor';
    ELSIF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = CURRENT_USER AND rolname = 'alumno') THEN
        user_role := 'alumno';
    ELSE
        user_role := 'desconocido';
    END IF;

    RETURN user_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION enmascarar_telefono(telefono VARCHAR) RETURNS VARCHAR AS $$
BEGIN
    RETURN SUBSTRING(telefono, 1, 3) || '****' || SUBSTRING(telefono, LENGTH(telefono)-2);
END;
$$ LANGUAGE plpgsql;

-- Función para enmascarar el email
CREATE OR REPLACE FUNCTION enmascarar_email(email VARCHAR) RETURNS VARCHAR AS $$
DECLARE
    username VARCHAR;
    domain VARCHAR;
BEGIN
    username := SPLIT_PART(email, '@', 1);
    domain := SPLIT_PART(email, '@', 2);
    RETURN LEFT(username, 2) || '****' || RIGHT(username, 1) || '@' || domain;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW datos_sensibles_enmascarados AS
SELECT 
    alumno_id,
    CASE 
        WHEN get_user_role() = 'admin' THEN telefono
        ELSE enmascarar_telefono(telefono)
    END AS telefono,
    CASE 
        WHEN get_user_role() = 'admin' THEN email
        ELSE enmascarar_email(email)
    END AS email
FROM datos_sensibles;


CREATE OR REPLACE FUNCTION get_user_id()
RETURNS INT AS $$
DECLARE
    user_id INT;
BEGIN
    -- Verificar si el usuario es un alumno
    SELECT id INTO user_id
    FROM alumnos
    WHERE email = CURRENT_USER;

    IF user_id IS NOT NULL THEN
        RETURN user_id;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE POLICY datos_sensibles_policy ON datos_sensibles
FOR SELECT
TO PUBLIC
USING (
    CASE 
        WHEN get_user_role() = 'alumno' THEN alumno_id = get_user_id()
        ELSE TRUE
    END
);

ALTER TABLE datos_sensibles ENABLE ROW LEVEL SECURITY;

CREATE POLICY alumno_policy ON datos_sensibles
    FOR SELECT
    USING (alumno_id = get_current_alumno_id());

CREATE POLICY profesor_policy ON datos_sensibles
    FOR SELECT
    USING (TRUE);

CREATE POLICY admin_policy ON datos_sensibles
    FOR ALL
    USING (TRUE);

CREATE OR REPLACE VIEW datos_sensibles_enmascarados AS
SELECT 
    alumno_id,
    enmascarar_telefono(telefono) AS telefono,
    enmascarar_email(email) AS email
FROM datos_sensibles;

CREATE OR REPLACE VIEW datos_sensibles_enmascarados_profesores AS
SELECT 
    alumno_id,
    enmascarar_telefono(telefono) AS telefono,
    enmascarar_email(email) AS email
FROM datos_sensibles;

CREATE OR REPLACE VIEW datos_alumnos AS
SELECT 
    a.id AS alumno_id,
    a.nombre,
    a.apellidos,
    a.edad,
    enmascarar_telefono(ds.telefono) AS telefono,
    enmascarar_email(ds.email) AS email
FROM alumnos a
JOIN datos_sensibles ds ON a.id = ds.alumno_id;

CREATE OR REPLACE VIEW datos_sensibles_enmascarados_alumnos AS
SELECT 
    alumno_id,
    CASE 
        WHEN current_user ~ '^alumno\d+$' THEN enmascarar_telefono(telefono)
        ELSE 'Access Denied'
    END AS telefono,
    CASE 
        WHEN current_user ~ '^alumno\d+$' THEN enmascarar_email(email)
        ELSE 'Access Denied'
    END AS email,
    CASE 
        WHEN current_user = 'alumno1' THEN 1
        WHEN current_user ~ '^alumno\d+$' THEN (substring(current_user from 'alumno(\d+)'))::INT
        ELSE NULL
    END AS debug_alumno_id,
    current_user AS debug_current_user,
    session_user AS debug_session_user
FROM datos_sensibles
WHERE current_user ~ '^alumno\d+$' AND 
      alumno_id = CASE 
                    WHEN current_user = 'alumno1' THEN 1
                    ELSE (substring(current_user from 'alumno(\d+)'))::INT
                  END;

CREATE OR REPLACE FUNCTION get_current_alumno_id() RETURNS INT AS $$
BEGIN
    RETURN (SELECT id FROM alumnos WHERE login = current_user);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE VIEW mis_datos AS
SELECT 
    a.nombre,
    a.apellidos,
    a.edad,
    CASE 
        WHEN current_user ~ '^alumno\d+$' THEN enmascarar_telefono(ds.telefono)
        ELSE 'Acceso Denegado'
    END AS telefono,
    CASE 
        WHEN current_user ~ '^alumno\d+$' THEN enmascarar_email(ds.email)
        ELSE 'Acceso Denegado'
    END AS email
FROM alumnos a
JOIN datos_sensibles ds ON a.id = ds.alumno_id
WHERE current_user ~ '^alumno\d+$' AND 
      a.id = CASE 
                WHEN current_user = 'alumno1' THEN 1
                ELSE (substring(current_user from 'alumno(\d+)'))::INT
             END;
-- permisos alumnos
GRANT SELECT ON mis_datos TO alumno;

-- permisos profesores
GRANT SELECT ON datos_alumnos TO profesor;
GRANT USAGE ON SCHEMA public TO profesor;

DO $$
DECLARE
    table_rec RECORD;
BEGIN
    FOR table_rec IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'  
          AND table_type = 'BASE TABLE'
          AND table_name != 'datos_sensibles'
    LOOP
        EXECUTE format('GRANT SELECT ON TABLE public.%I TO profesor', table_rec.table_name);
    END LOOP;
END $$;


CREATE OR REPLACE VIEW todos_los_datos AS
SELECT 
    a.id AS alumno_id,
    a.nombre,
    a.apellidos,
    a.edad,
    ds.telefono,
    ds.email
FROM alumnos a
JOIN datos_sensibles ds ON a.id = ds.alumno_id;

-- permisos admin
GRANT SELECT ON todos_los_datos TO admin;

GRANT ALL ON datos_sensibles TO admin;
GRANT USAGE ON SCHEMA public TO admin;
DO $$
DECLARE
    table_rec RECORD;
BEGIN
    FOR table_rec IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'  
          AND table_type = 'BASE TABLE'
    LOOP
        EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.%I TO admin', table_rec.table_name);
    END LOOP;
END $$;

REVOKE ALL ON datos_sensibles FROM PUBLIC;
REVOKE ALL ON datos_sensibles FROM alumno;
REVOKE ALL ON datos_sensibles FROM profesor;