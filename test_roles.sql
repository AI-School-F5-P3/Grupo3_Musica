SET ROLE armoniaadmin;
--tiene todos los derechos de ver y modificar datos

SET ROLE Marprofesor;
SELECT * FROM datos_sensibles_enmascarados_profesores;
--tiene derechos de (solo)ver datos de alumnos, profesores y clases y datos sensibles enmascarados de alumnos

SET ROLE alumno15;
SELECT * FROM datos_sensibles_enmascarados_alumnos;
-- tiene que devolver solo sus propios datos
RESET ROLE;

-- Lista de roles
SELECT rolname FROM pg_roles WHERE rolname LIKE 'alumno%' OR rolname LIKE '%profesor' OR rolname = 'armoniaadmin';

-- Lista de permisos
SELECT grantee, table_name, privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name IN ('datos_sensibles', 'datos_sensibles_enmascarados_alumnos', 'datos_sensibles_enmascarados_profesores');



