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