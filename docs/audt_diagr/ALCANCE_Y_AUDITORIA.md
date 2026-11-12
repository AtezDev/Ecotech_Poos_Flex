# EcoTech — Auditoría de alcance y compatibilidad

Fecha de revisión: 10 de noviembre de 2026.

## Fuentes contrastadas

- Repositorio público `AtezDev/Ecotech_Poos_Flex`, rama `main`, commit `d99a44315f0e2c6e2fb5f38b7afe8879f1efdadf` (último estado comprobado).
- UML final `Diagrama_Final.drawio` de tres vistas.
- Unidad 2, Clase 1: del UML a Python.
- Unidad 2, Clase 2: relaciones, encapsulamiento y listas de objetos.
- Material «Del objeto al primer registro»: `conexion.py`, SQLite/MySQL, DAO, INSERT, `lastrowid`.
- Flex U2–U3, Clase 3 «Empleado válido y lectura de datos»: reglas nombre/correo, `@property`, setters, `listar()`, `buscar_por_id()`, `fetchall()`, `fetchone()`, `None` y `try/except ValueError` puntual en `main.py`.

## Clases y atributos del UML

| Clase | Atributos | Estado |
|---|---|---|
| Empleado | `idEmpleado`, `nombre`, `direccion`, `telefono`, `correoElectronico`, `fechaInicioContrato`, `salario` | Presentes. `id` es la representación técnica del ID generado. |
| Departamento | `nombre`, `gerente` | Presentes, más lista interna de empleados. |
| Proyecto | `nombre`, `descripcion`, `fechaInicio` | Presentes. |
| RegistroTiempo | `fecha`, `horasTrabajadas`, `descripcionTarea` | Presentes, más referencias a empleado y proyecto. |
| Informe | Sin atributos propios; cuatro métodos de generación | Conceptual en UML; aún no implementado en Python. |
| CuentaUsuario | Nombre, hash, sal y rol | UML final; Unidad 3 pendiente. |
| ControlAcceso | `usuarioAutenticado` | UML final; Unidad 3 pendiente. |

## Material enseñado y adaptaciones

**Directamente enseñado:** clases, `__init__`, `self`, relaciones simples, listas, `@property`, getters/setters, validación de nombre y correo, `ValueError`, `try/except ValueError` en `main.py`, `INSERT` parametrizado con `lastrowid`, `SELECT` para `listar()` y `buscar_por_id()`.

**Adaptaciones necesarias al UML:** campos completos de Empleado, fecha de Proyecto, referencias de RegistroTiempo, tres DAO sencillos de inserción, y una tabla puente `empleado_proyecto` con el DAO mínimo `asignar()`. La tabla puente representa la relación muchos a muchos sin inventar una subclase `EmpleadoProyecto`.

**No introducido aún:** CRUD completo, menú, API externa, autenticación, roles, emisión de informes y control general de errores de DAO. Las operaciones conceptuales de `crearDepartamento`, `eliminarDepartamento`, `crearProyecto`, `eliminarProyecto` y otras de gestión completa del UML quedan pendientes: no deben presentarse como CRUD terminado. Los métodos de cambio de atributos sí están disponibles en las entidades.

**Reglas añadidas por coherencia:** fechas `date`, salario numérico no negativo, horas positivas y descripción no vacía. El UML requiere validar salario y horas, pero los límites exactos deben confirmarse con el docente. El ejemplo de nombre/correo de la Clase 3 se implementó como se enseñó.

## Estructura SQL y multiplicidad

Tablas: `departamento`, `proyecto`, `empleado`, `empleado_proyecto`, `registro_tiempo`.

- Un departamento puede tener varios empleados (`empleado.departamento_id`).
- Empleado y Proyecto tienen una relación N:M; la tabla puente tiene clave primaria `(empleado_id, proyecto_id)`.
- RegistroTiempo se asocia a una pareja existente de empleado y proyecto. La clave foránea compuesta y la comprobación previa de `RegistroTiempoDAO` impiden guardar horas para una asignación ausente.
- `EmpleadoProyectoDAO.asignar()` consulta primero con `fetchone()` y devuelve `False` ante un duplicado, además de la restricción de unicidad de la base.

## Compatibilidad con SQLite y MySQL

`conexion.py` selecciona motor mediante `DB_ENGINE`; `creacion_bd.py` utiliza los tipos y autoincrementos correspondientes; los DAO seleccionan `?` o `%s` y pasan datos como parámetros. SQLite activa `PRAGMA foreign_keys=ON`. MySQL crea tablas `ENGINE=InnoDB` para soportar las claves foráneas.

**Importante:** MySQL/WampServer **no fue ejecutado en este entorno**. Debe probarse en el computador del estudiante con WAMP activo y una base `ecotech_practica` nueva y vacía.

La base MySQL original `ecotech` contiene una tabla `empleado(id,nombre,correo)`. Este programa no la migra, no la borra ni la sobrescribe. `crear_tablas()` hace una comprobación previa y lanza un mensaje si faltan columnas, antes de comenzar a crear otras tablas. La base antigua debe respaldarse y migrarse por separado cuando lo indique el docente.

## Pruebas realizadas en SQLite

- Creación de cinco tablas, incluidas las dos relaciones.
- Inserciones e ID autoincremental.
- Lectura de empleados mediante `listar()` y `buscar_por_id()`; `[]` y `None` en ausencia.
- `strip()`, validación de nombre/correo y rechazo sin sobrescribir un valor válido.
- Límite de 80 caracteres, apóstrofes, fecha de contrato y salario.
- Inserción de asociación N:M; rechazo de duplicados.
- Rechazo de RegistroTiempo sin asociación; inserción correcta con asociación.
- Verificación de clave foránea compuesta en SQLite.
- Detección de una tabla antigua de tres columnas sin borrar su registro.

Resultado: 17 pruebas automáticas aprobadas en SQLite, más ejecución completa de `main.py` desde otro directorio.

## Copia de archivos al repositorio real

1. Respaldar la carpeta original y el `.env` local antes de reemplazar.
2. Copiar `src/`, `Readme.md`, `requirements.txt`, `requeriments.txt`, `.env.example` y `.gitignore` desde esta guía a la **raíz del repositorio**. Copiar `docs/Diagrama_Final.drawio` y este documento sin eliminar los documentos previos.
3. **No sobrescribir el `.env` con credenciales personales.** Dejar `DB_ENGINE=sqlite` en la primera prueba, o usar otra base MySQL de pruebas.
4. Ejecutar en Git Bash desde la raíz: `source .venv/Scripts/activate` si el entorno ya existe; `python -m pip install -r requirements.txt`; `python src/main.py`.
5. Verificar `git status`, que `.env`/`.venv`/`.db` estén ignorados, y recién entonces ejecutar `git add .`, `git commit -m "Avance EcoTech: validaciones, consultas y relaciones UML"`, `git push`.
6. Mantener las capturas previas de la tabla original y de los IDs 1, 2 y 3 en MySQL; la base nueva generará otros IDs.

## Observaciones honestas

- Los archivos son una **versión de referencia de reemplazo**, no una edición directa de GitHub.
- No se asegura integración con una base antigua cuyo esquema no coincide con el nuevo UML.
- `main.py` es una demostración de clase e inserta filas nuevas en cada ejecución.
- El código de dominio y los DAO se mantienen cortos y sin comentarios explicativos excesivos; las justificaciones están en README y aquí.
- El cierre de conexiones ante errores de SQL, el CRUD completo y el menú seguirán ampliándose conforme al material de la asignatura.
