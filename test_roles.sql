SET SESSION AUTHORIZATION armoniaadmin;
select * from todos_los_datos;

SET SESSION AUTHORIZATION Marprofesor;
SELECT * FROM datos_alumnos;
--tiene derechos de (solo)ver datos de alumnos, profesores y clases y datos sensibles enmascarados de alumnos

SET SESSION AUTHORIZATION alumno15;
SELECT * FROM mis_datos;
-- tiene que devolver solo sus propios datos
RESET ROLE;

-- Lista de roles
SELECT rolname FROM pg_roles WHERE rolname LIKE 'alumno%' OR rolname LIKE '%profesor' OR rolname = 'armoniaadmin';

-- Lista de permisos
SELECT grantee, table_name, privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name IN ('datos_sensibles', 'datos_sensibles_enmascarados_alumnos', 'datos_sensibles_enmascarados_profesores');



