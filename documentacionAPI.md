# Documentación de la API de la Escuela de Música Armonía

## Descripción General

Esta es la API para la gestión de la Escuela de Música Armonía. Permite la gestión de alumnos, profesores, clases, inscripciones y descuentos, así como la autenticación de usuarios y la descarga de datos en formato CSV.# Documentación de la API de la Escuela de Música Armonía

## Descripción General

Esta es la API para la gestión de la Escuela de Música Armonía. Permite la gestión de alumnos, profesores, clases, inscripciones y descuentos, así como la autenticación de usuarios y la descarga de datos en formato CSV.

## Endpoints

### Inicio

#### `GET /`

Renderiza la página de inicio.

### Autenticación

#### `GET /login`

Renderiza la página de inicio de sesión.

#### `POST /login`

Verifica las credenciales del usuario y, si son correctas, inicia una sesión y redirige al dashboard.

- **Parámetros del cuerpo**:
  - `username` (string): El nombre de usuario.
  - `password` (string): La contraseña del usuario.

- **Respuestas**:
  - `200 OK`: Credenciales correctas, redirige al dashboard.
  - `401 Unauthorized`: Credenciales incorrectas.

#### `GET /logout`

Cierra la sesión del usuario y redirige a la página de inicio.

### Dashboard

#### `GET /dashboard`

Renderiza el dashboard con información de la escuela.

- **Respuestas**:
  - `200 OK`: Renderiza la página del dashboard.
  - `500 Internal Server Error`: Error al cargar el dashboard.

### Gestión de Alumnos

#### `GET /admin/alumnos`

Renderiza la página de gestión de alumnos. Disponible para administradores y profesores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de alumnos.
  - `500 Internal Server Error`: Error al obtener los datos de alumnos.

### Gestión de Profesores

#### `GET /admin/profesores`

Renderiza la página de gestión de profesores. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de profesores.
  - `500 Internal Server Error`: Error al obtener los datos de profesores.

### Gestión de Clases

#### `GET /admin/clases`

Renderiza la página de gestión de clases. Disponible para administradores y profesores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de clases.
  - `500 Internal Server Error`: Error al obtener los datos de clases.

#### `GET /admin/clases/nueva`

Renderiza el formulario para añadir una nueva clase. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza el formulario de nueva clase.

#### `POST /admin/clases/nueva`

Añade una nueva clase a la base de datos. Disponible solo para administradores.

- **Parámetros del cuerpo**:
  - `nombre` (string): El nombre de la clase.
  - `profesor_id` (int): El ID del profesor.
  - `precio_base` (float): El precio base de la clase.
  - `tipo_pack` (string): El tipo de pack de la clase.

- **Respuestas**:
  - `200 OK`: Clase añadida correctamente.
  - `500 Internal Server Error`: Error al añadir la clase.

#### `GET /admin/clases/<int:clase_id>/editar`

Renderiza el formulario para editar una clase existente. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza el formulario de edición de clase.

#### `POST /admin/clases/<int:clase_id>/editar`

Actualiza los datos de una clase existente en la base de datos. Disponible solo para administradores.

- **Parámetros del cuerpo**:
  - `nombre` (string): El nombre de la clase.
  - `profesor_id` (int): El ID del profesor.
  - `precio_base` (float): El precio base de la clase.
  - `tipo_pack` (string): El tipo de pack de la clase.

- **Respuestas**:
  - `200 OK`: Clase actualizada correctamente.
  - `500 Internal Server Error`: Error al actualizar la clase.

#### `POST /admin/clases/<int:clase_id>/eliminar`

Elimina una clase existente de la base de datos. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Clase eliminada correctamente.
  - `500 Internal Server Error`: Error al eliminar la clase.

### Gestión de Inscripciones

#### `GET /admin/inscripciones`

Renderiza la página de gestión de inscripciones. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de inscripciones.
  - `500 Internal Server Error`: Error al obtener los datos de inscripciones.

### Gestión de Descuentos

#### `GET /admin/descuentos`

Renderiza la página de gestión de descuentos. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de descuentos.
  - `500 Internal Server Error`: Error al obtener los datos de descuentos.

### Descarga de Datos

#### `GET /descargar_alumnos_csv`

Descarga los datos de la tabla `alumnos` en formato CSV. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: CSV descargado correctamente.
  - `500 Internal Server Error`: Error al exportar los datos.

## Seguridad

La API utiliza autenticación basada en sesiones y proporciona decoradores para proteger las rutas según los roles de los usuarios (`admin`, `profesor`).

## Variables de Entorno

Asegúrate de que el archivo `.env` contenga las siguientes variables de entorno para la conexión a la base de datos:

```plaintext
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=your_db_port


## Endpoints

### Inicio

#### `GET /`

Renderiza la página de inicio.

### Autenticación

#### `GET /login`

Renderiza la página de inicio de sesión.

#### `POST /login`

Verifica las credenciales del usuario y, si son correctas, inicia una sesión y redirige al dashboard.

- **Parámetros del cuerpo**:
  - `username` (string): El nombre de usuario.
  - `password` (string): La contraseña del usuario.

- **Respuestas**:
  - `200 OK`: Credenciales correctas, redirige al dashboard.
  - `401 Unauthorized`: Credenciales incorrectas.

#### `GET /logout`

Cierra la sesión del usuario y redirige a la página de inicio.

### Dashboard

#### `GET /dashboard`

Renderiza el dashboard con información de la escuela.

- **Respuestas**:
  - `200 OK`: Renderiza la página del dashboard.
  - `500 Internal Server Error`: Error al cargar el dashboard.

### Gestión de Alumnos

#### `GET /admin/alumnos`

Renderiza la página de gestión de alumnos. Disponible para administradores y profesores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de alumnos.
  - `500 Internal Server Error`: Error al obtener los datos de alumnos.

### Gestión de Profesores

#### `GET /admin/profesores`

Renderiza la página de gestión de profesores. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de profesores.
  - `500 Internal Server Error`: Error al obtener los datos de profesores.

### Gestión de Clases

#### `GET /admin/clases`

Renderiza la página de gestión de clases. Disponible para administradores y profesores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de clases.
  - `500 Internal Server Error`: Error al obtener los datos de clases.

#### `GET /admin/clases/nueva`

Renderiza el formulario para añadir una nueva clase. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza el formulario de nueva clase.

#### `POST /admin/clases/nueva`

Añade una nueva clase a la base de datos. Disponible solo para administradores.

- **Parámetros del cuerpo**:
  - `nombre` (string): El nombre de la clase.
  - `profesor_id` (int): El ID del profesor.
  - `precio_base` (float): El precio base de la clase.
  - `tipo_pack` (string): El tipo de pack de la clase.

- **Respuestas**:
  - `200 OK`: Clase añadida correctamente.
  - `500 Internal Server Error`: Error al añadir la clase.

#### `GET /admin/clases/<int:clase_id>/editar`

Renderiza el formulario para editar una clase existente. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza el formulario de edición de clase.

#### `POST /admin/clases/<int:clase_id>/editar`

Actualiza los datos de una clase existente en la base de datos. Disponible solo para administradores.

- **Parámetros del cuerpo**:
  - `nombre` (string): El nombre de la clase.
  - `profesor_id` (int): El ID del profesor.
  - `precio_base` (float): El precio base de la clase.
  - `tipo_pack` (string): El tipo de pack de la clase.

- **Respuestas**:
  - `200 OK`: Clase actualizada correctamente.
  - `500 Internal Server Error`: Error al actualizar la clase.

#### `POST /admin/clases/<int:clase_id>/eliminar`

Elimina una clase existente de la base de datos. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Clase eliminada correctamente.
  - `500 Internal Server Error`: Error al eliminar la clase.

### Gestión de Inscripciones

#### `GET /admin/inscripciones`

Renderiza la página de gestión de inscripciones. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de inscripciones.
  - `500 Internal Server Error`: Error al obtener los datos de inscripciones.

### Gestión de Descuentos

#### `GET /admin/descuentos`

Renderiza la página de gestión de descuentos. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: Renderiza la página de descuentos.
  - `500 Internal Server Error`: Error al obtener los datos de descuentos.

### Descarga de Datos

#### `GET /descargar_alumnos_csv`

Descarga los datos de la tabla `alumnos` en formato CSV. Disponible solo para administradores.

- **Respuestas**:
  - `200 OK`: CSV descargado correctamente.
  - `500 Internal Server Error`: Error al exportar los datos.

## Seguridad

La API utiliza autenticación basada en sesiones y proporciona decoradores para proteger las rutas según los roles de los usuarios (`admin`, `profesor`).

## Variables de Entorno

Asegúrate de que el archivo `.env` contenga las siguientes variables de entorno para la conexión a la base de datos:

```plaintext
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=usuario_de_tu_base_de_datos
DB_PASSWORD=contraseña_de_tu_base_de_datos
DB_HOST=host_de_tu_base_de_datos
DB_PORT=puerto_de_tu_base_de_datos
```