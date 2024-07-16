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