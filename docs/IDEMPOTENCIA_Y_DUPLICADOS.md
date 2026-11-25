# Idempotencia: que reingresar el programa no multiplique datos

Regla de la guía (sección 12): sembrar dos veces debe conservar los registros objetivo sin duplicarlos. Antes de insertar, se busca por un criterio estable; si existe, se reutiliza.

## Qué se duplicaba antes de este cambio

| Acción | Resultado antes | Resultado ahora |
|---|---|---|
| Opción 3 de semillas, repetida | Sin duplicados (ya comprobado) | Sin duplicados |
| `python src/main.py --demo`, cada vez | Un empleado, un departamento "Desarrollo" y un proyecto "EcoTech" más en cada ejecución | Se carga una vez; las siguientes responden que no se duplicó nada |
| Registrar empleado con un correo ya existente (menú) | Se creaba el duplicado | Se rechaza con mensaje |
| Actualizar correo a uno de otro empleado (menú) | Se permitía | Se rechaza con mensaje |
| Crear departamento o proyecto con nombre repetido (menú) | Se creaba el duplicado | Se rechaza con mensaje |
| Crear cuenta para un empleado que ya tiene cuenta | Rechazado por UNIQUE en `usuario.empleado_id` | Sin cambio |
| Crear cuentas con el mismo nombre de usuario | Rechazado por UNIQUE en `usuario.nombre_usuario` | Sin cambio |

## Cambios

- `EmpleadoDAO.buscar_id_por_correo`, `DepartamentoDAO.buscar_id_por_nombre`, `ProyectoDAO.buscar_id_por_nombre`: devuelven el ID o `None`. Mismo patrón que `buscar_id_empleado` de semillas.
- `menu_empleado.crear_empleado` y `actualizar_empleado`, `menu_departamento.crear_departamento`, `menu_proyecto.crear_proyecto`: buscan antes de insertar.
- `main.demostrar_relaciones`: si el empleado de la demo ya existe, no inserta nada. Si el departamento "Desarrollo" o el proyecto "EcoTech" ya existen, los reutiliza. El empleado de la demo mantiene el nombre "Ana Torres" y usa el correo `ana.demo@ecotech.cl`, porque el correo es la clave y el de las semillas ya es `ana.torres@ecotech.cl`.

## Qué no se cambió, y por qué

- No se agregaron restricciones UNIQUE nuevas a `empleado.correo`, `departamento.nombre` ni `proyecto.nombre`. `crear_tablas()` compara columnas, no restricciones: una base ya existente no recibiría la restricción, y si ya tiene duplicados la creación fallaría. Antes de añadirla hay que limpiar los datos y confirmarla con el profesor (el README lo deja como pendiente).
- La clave de `admin` ya no está en el código: se lee de `ADMIN_PASSWORD` en el `.env`. Si falta, no se crea la cuenta y se informa.
- La cuenta `admin` se vuelve a crear solo si no existe ninguna cuenta con ese nombre. Si el administrador la renombra o la elimina y luego se ejecuta la opción 3, se crea una nueva para el primer empleado sin cuenta. Es un comportamiento de la semilla, no una duplicación, pero conviene saberlo.

## Cómo se verificó

- `unittest discover`: 161 OK (130 anteriores + 14 de `tests/test_idempotencia.py` + 17 de `tests/test_cuentas_crud.py`).
- `pytest`: 161 passed.
- Escenarios repetidos en SQLite y MariaDB 10.11: conteos estables tras 3 cargas de semillas y 2 de `--demo`; rechazos de correo, departamento y proyecto repetidos.

## Preguntas para el profesor

1. ¿El correo de empleado, el nombre de departamento y el nombre de proyecto son reglas del modelo? Si sí, ¿se agrega UNIQUE con una migración?
2. ¿La cuenta inicial `admin` debe poder recrearse con la opción 3 cuando falta?
