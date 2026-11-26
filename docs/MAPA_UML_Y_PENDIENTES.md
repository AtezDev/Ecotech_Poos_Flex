# Auditoría del alcance UML — las tres vistas son el contrato

El objetivo de esta carpeta es aprender **sin eliminar nada del UML**. Los ejemplos del profesor muestran dos campos del Empleado, pero este proyecto conserva los seis datos de entrada, el ID y todas las relaciones que se han implementado.

| Clase del UML | Estado de la implementación actual |
|---|---|
| Empleado | Siete atributos del UML (el ID es generado por BD y se protege después); getters, cambios, validadores y `registrarEmpleado`, `asignarAProyecto`, `desasignarDeProyecto` |
| Departamento | Nombre/gerente, lista de empleados, asignación y reasignación, getters/setters. CRUD SQL completo en `DepartamentoDAO` y `menu_departamento.py`. **Pendientes UML:** `crearDepartamento`, `modificarDepartamento`, `buscarDepartamento`, `eliminarDepartamento` como **métodos de la clase** |
| Proyecto | Nombre/descripcion/fecha, cambios y getters. CRUD SQL completo en `ProyectoDAO` y `menu_proyecto.py`. **Pendientes UML:** `crearProyecto`, `modificarProyecto`, `eliminarProyecto` como **métodos de la clase** |
| RegistroTiempo | Fecha/horas/descripcion, getters/cambios, asociación a Empleado–Proyecto, registro en BD y CRUD SQL completo (`menu_registro_tiempo.py`) |
| Informe | **Pendiente de futuras clases**: los cuatro métodos de generación y la dependencia de `ControlAcceso` |
| CuentaUsuario | **Implementada**: nombre de usuario, hash bcrypt, rol y verificación (la sal va dentro del hash de bcrypt) |
| ControlAcceso | **Parcial**: autenticar y autorizar (`servicios/permisos.py`) están; falta cerrar sesión como clase propia |

**Importante:** el UML contiene siete clases, pero el alcance de las diapositivas revisadas todavía no enseña el sistema de autenticación e informes. No hay implementaciones ficticias de seguridad ni se presenta esta carpeta como el sistema final completo.

## Relación N:M conservada (sin rediseñar)

- En Python `Empleado._proyectos` representa una colección de `Proyecto`.
- En SQL `empleado_proyecto(empleado_id, proyecto_id)` guarda las parejas.
- `empleado_proyecto` tiene clave primaria compuesta y dos foreign keys.
- `registro_tiempo` depende de una pareja previamente registrada (FK compuesta).
- No hay borrado en cascada: un DELETE de Empleado con proyectos relacionados debe ser rechazado.

## CRUD (Clase 4 y ampliación del 17-nov-2026)

- `EmpleadoDAO.insertar`: CREATE.
- `EmpleadoDAO.listar` y `buscar_por_id`: READ.
- `EmpleadoDAO.actualizar`: UPDATE de nombre, dirección, teléfono, correo y salario (en la Clase 4 del profesor solo se mostró el correo).
- `EmpleadoDAO.eliminar`: DELETE por ID con confirmación en el menú.

- `DepartamentoDAO`, `ProyectoDAO` y `RegistroTiempoDAO`: listar, buscar por ID, actualizar y eliminar.
- `EmpleadoProyectoDAO.desasignar` y `DepartamentoDAO.asignar_empleado/quitar_empleado`: cambiar de proyecto y de departamento.

**Pendiente:** fecha de contrato del empleado (el UML no define su cambio) y estado «terminado» de un proyecto (el UML no lo define). El resto del proyecto está conservado.

## Material original y seguridad

Esta carpeta no incluye `.env`, `.venv`, bases de datos locales ni contraseñas. Mantén los documentos históricos que ya tienes en tu repositorio GitHub; no los elimines al incorporar los archivos remodelados.
