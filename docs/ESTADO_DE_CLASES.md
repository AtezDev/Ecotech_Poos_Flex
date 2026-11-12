# Estado del aprendizaje en EcoTech

**Implementado:** cuatro entidades de dominio; relaciones entre Empleado, Departamento y Proyecto; `EmpleadoDAO.insertar`, `listar` y `buscar_por_id`; otros DAO con `insertar`; relación N:M en tabla puente; fecha de contrato y de proyecto; configuración SQLite/MySQL.

**Contenido específico de las diapositivas:** `__init__`, `self`, colecciones, `@property`, setters, `strip`, `isinstance`, `ValueError`, SQL parametrizado, `lastrowid`, `fetchall`, `fetchone`, `None` y demostraciones en consola.

**Adaptaciones al UML:** campos adicionales de Empleado, fecha de Proyecto, referencias en RegistroTiempo, cinco tablas y tabla puente, controles numéricos de salario y horas, lectura de la relación N:M.

**No implementado aún:** tres clases de informes/acceso del UML, menú, actualización/eliminación SQL y manejo global de excepciones. `main.py` incluye únicamente los ejemplos de `try/except ValueError` asociados a validación.

**Base original:** nunca ejecutes esta extensión sobre la base `ecotech` con empleado de tres columnas sin planificar primero una migración. Usa una base nueva para las prácticas.

**Estado de verificación:** pruebas SQLite reproducibles incluidas en `tests/`; ejecución en MySQL/WampServer pendiente de la comprobación local del estudiante.
