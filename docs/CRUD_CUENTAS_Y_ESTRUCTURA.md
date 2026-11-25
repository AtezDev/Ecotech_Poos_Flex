# CRUD de cuentas frente a los CRUD de las demás entidades

Comparación con la estructura que ya usan Empleados, Departamentos y Proyectos: un DAO con `insertar`, `listar`, `buscar_por_id`, `actualizar` y `eliminar`, y un menú con Registrar, Listar, Buscar, Actualizar y Eliminar.

| Operación | Empleado / Departamento / Proyecto | Usuario (cuenta) |
|---|---|---|
| Crear | Menú «Registrar» | Acceso (opción 2) y admin (opción 1) |
| Listar | `listar_todo` + `mostrar_datos()` | `listar_todo` + `Usuario.mostrar_datos()` (sin hash) |
| Buscar | `buscar_uno` por ID | Por ID y por nombre (`buscar_cuenta`) |
| Actualizar | Un submenú o una opción por campo | Modificar (admin) y Mi cuenta (usuario) |
| Eliminar | `eliminar_con_confirmacion` | Admin (`eliminar_cuenta`) y Mi cuenta (`eliminar_mi_cuenta`) |
| Verificación | Validaciones del dominio | Nombre normalizado, largo y caracteres; clave mínima de 15; 72 bytes; clave actual para cambios propios |
| Integridad | UNIQUE y FK en la BD | UNIQUE en nombre y en empleado; FK a `empleado` |

## Reglas nuevas en esta versión

- El nombre `admin` está reservado: ninguna cuenta nueva ni renombrada puede tomarlo, porque el acceso de administrador se decide por ese nombre.
- La cuenta `admin` no puede cambiar su nombre ni eliminarse desde Mi cuenta.
- Los cambios propios (nombre, clave, eliminar) exigen la clave actual.
- La clave nueva no puede ser igual a la actual.

## Pendiente

- Estructura: `buscar_cuenta` y `eliminar_cuenta` todavía tienen código propio en lugar de usar `buscar_uno` y `eliminar_con_confirmacion` de `menu_comun`. El comportamiento es el mismo; falta igualar la forma.
- Roles formales (quién administra) para la próxima clase. Hoy se decide por el nombre `admin`.
- Protección contra tiempo de respuesta: si el usuario no existe, la respuesta tarda menos que con una clave incorrecta (ver la revisión de la Clase 6).
