# Auditoría del alcance UML — las tres vistas son el contrato

El objetivo de esta carpeta es aprender **sin eliminar nada del UML**. Los ejemplos del profesor muestran dos campos del Empleado, pero este proyecto conserva los seis datos de entrada, el ID y todas las relaciones que se han implementado.

| Clase del UML | Estado de la implementación actual |
|---|---|
| Empleado | Siete atributos del UML (el ID es generado por BD y se protege después); getters, cambios, validadores y `registrarEmpleado`, `asignarAProyecto`, `desasignarDeProyecto` |
| Departamento | Nombre/gerente, lista de empleados, asignación y reasignación, getters/setters. **Pendientes UML:** `crearDepartamento`, `modificarDepartamento`, `buscarDepartamento`, `eliminarDepartamento` como operaciones completas |
| Proyecto | Nombre/descripcion/fecha, cambios y getters. **Pendientes UML:** `crearProyecto`, `modificarProyecto`, `eliminarProyecto` como operaciones completas |
| RegistroTiempo | Fecha/horas/descripcion, getters/cambios, asociación a Empleado–Proyecto y registro en BD |
| Informe | **Pendiente de futuras clases**: los cuatro métodos de generación y la dependencia de `ControlAcceso` |
| CuentaUsuario | **Pendiente**: nombre de usuario, hash de contraseña, sal, rol y verificación |
| ControlAcceso | **Pendiente**: autenticar, autorizar, cerrar sesión |

**Importante:** el UML contiene siete clases, pero el alcance de las diapositivas revisadas todavía no enseña el sistema de autenticación e informes. No hay implementaciones ficticias de seguridad ni se presenta esta carpeta como el sistema final completo.

## Relación N:M conservada (sin rediseñar)

- En Python `Empleado._proyectos` representa una colección de `Proyecto`.
- En SQL `empleado_proyecto(empleado_id, proyecto_id)` guarda las parejas.
- `empleado_proyecto` tiene clave primaria compuesta y dos foreign keys.
- `registro_tiempo` depende de una pareja previamente registrada (FK compuesta).
- No hay borrado en cascada: un DELETE de Empleado con proyectos relacionados debe ser rechazado.

## CRUD real de la Clase 4

- `EmpleadoDAO.insertar`: CREATE.
- `EmpleadoDAO.listar` y `buscar_por_id`: READ.
- `EmpleadoDAO.actualizar`: UPDATE **solo del correo**, según la demostración del profesor.
- `EmpleadoDAO.eliminar`: DELETE por ID con confirmación en el menú.

**Pendiente:** ampliar UPDATE para otros atributos y operaciones SQL para otras entidades cuando se trabaje en clases. El resto del proyecto está conservado.

## Material original y seguridad

Esta carpeta no incluye `.env`, `.venv`, bases de datos locales ni contraseñas. Mantén los documentos históricos que ya tienes en tu repositorio GitHub; no los elimines al incorporar los archivos remodelados.
