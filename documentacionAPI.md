# Documentación de la API

## Autenticación y Autorización

### Decoradores

- `@login_required`: Requiere que el usuario esté autenticado.
- `@admin_required`: Requiere que el usuario tenga el rol de administrador.
- `@profesor_required`: Requiere que el usuario tenga el rol de profesor.

---

## Rutas

### Inicio

#### `GET /`
- **Descripción**: Muestra la página de inicio.
- **Respuesta**: Renderiza `index.html`.

---

### Inicio de Sesión

#### `GET /login`
- **Descripción**: Muestra el formulario de inicio de sesión.
- **Respuesta**: Renderiza `login.html`.

#### `POST /login`
- **Descripción**: Procesa las credenciales de inicio de sesión.
- **Parámetros**:
  - `username`: Nombre de usuario.
  - `password`: Contraseña.
- **Respuesta**:
  - `200 OK`: Redirige al dashboard si las credenciales son correctas.
  - `401 Unauthorized`: Devuelve un mensaje de error si las credenciales son incorrectas.

---

### Dashboard

#### `GET /dashboard`
- **Descripción**: Muestra el panel de control.
- **Autenticación**: Requiere que el usuario esté autenticado.
- **Respuesta**: Renderiza `dashboard.html` con datos de ejemplo.

---

### Gestión de Alumnos

#### `GET /admin/alumnos`
- **Descripción**: Muestra la lista de alumnos.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `alumnos.html` con la lista de alumnos.
- **Errores**:
  - `500 Internal Server Error`: Error al obtener alumnos de la base de datos.

---

### Gestión de Profesores

#### `GET /admin/profesores`
- **Descripción**: Muestra la lista de profesores.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `profesores.html` con la lista de profesores.
- **Errores**:
  - `500 Internal Server Error`: Error al obtener profesores de la base de datos.

---

### Gestión de Clases

#### `GET /admin/clases`
- **Descripción**: Muestra la lista de clases.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `clases.html` con la lista de clases.
- **Errores**:
  - `500 Internal Server Error`: Error al obtener clases de la base de datos.

#### `GET /admin/clases/nueva`
- **Descripción**: Muestra el formulario para añadir una nueva clase.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `nueva_clase.html` con la lista de profesores.

#### `POST /admin/clases/nueva`
- **Descripción**: Procesa la creación de una nueva clase.
- **Parámetros**:
  - `nombre`: Nombre de la clase.
  - `profesor_id`: ID del profesor.
  - `precio_base`: Precio base de la clase.
  - `tipo_pack`: Tipo de pack de la clase.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**:
  - `200 OK`: Redirige a la lista de clases si la creación es exitosa.
  - `500 Internal Server Error`: Error al añadir clase a la base de datos.

#### `GET /admin/clases/<int:clase_id>/editar`
- **Descripción**: Muestra el formulario para editar una clase existente.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `editar_clase.html` con la información de la clase y la lista de profesores.

#### `POST /admin/clases/<int:clase_id>/editar`
- **Descripción**: Procesa la edición de una clase existente.
- **Parámetros**:
  - `nombre`: Nombre de la clase.
  - `profesor_id`: ID del profesor.
  - `precio_base`: Precio base de la clase.
  - `tipo_pack`: Tipo de pack de la clase.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**:
  - `200 OK`: Redirige a la lista de clases si la edición es exitosa.
  - `500 Internal Server Error`: Error al editar clase en la base de datos.

#### `POST /admin/clases/<int:clase_id>/eliminar`
- **Descripción**: Procesa la eliminación de una clase existente.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**:
  - `200 OK`: Redirige a la lista de clases si la eliminación es exitosa.
  - `500 Internal Server Error`: Error al eliminar clase de la base de datos.

---

### Gestión de Inscripciones

#### `GET /admin/inscripciones`
- **Descripción**: Muestra la lista de inscripciones.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `inscripciones.html` con la lista de inscripciones.
- **Errores**:
  - `500 Internal Server Error`: Error al obtener inscripciones de la base de datos.

---

### Gestión de Descuentos

#### `GET /admin/descuentos`
- **Descripción**: Muestra la lista de descuentos.
- **Autenticación**: Requiere que el usuario tenga el rol de administrador.
- **Respuesta**: Renderiza `descuentos.html` con la lista de descuentos.
- **Errores**:
  - `500 Internal Server Error`: Error al obtener descuentos de la base de datos.

---

## Ejecución de la Aplicación

Para ejecutar la aplicación, usa el siguiente comando:

```bash
python app.py