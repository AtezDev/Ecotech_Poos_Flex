# Plan de estudio EcoTech remodelado — ATEZ

**Regla de diseño:** las tres vistas de `docs/audt_diagr/Diagrama_Final.drawio` son el contrato del proyecto. Las diapositivas explican **cómo implementar**, no autorizan a quitar atributos, relaciones ni métodos del diagrama.

## Material del profesor integrado para estudiar

1. `Unidad2_Clase1_Del_UML_al_Proyecto_Python_EcoTech.pdf`: pasar una clase del UML a `class`, `__init__`, `self`, `main.py`.
2. `Unidad2_Clase2_Relaciones_Encapsulamiento_Herencia_EcoTech.pdf`: referencias, listas, multiplicidades y `@property`.
3. `Unidad2_Clase4_SQLite_MySQL_Insert_ID.pdf`: conexión SQLite/MySQL, SQL parametrizado, DAO, `lastrowid`, `commit` y `close`.
4. `Flex_U2_U3_Clase3_Empleado_Valido_Lectura_Datos.pdf`: validar nombre/correo, `raise ValueError`, setters, `listar()` y `buscar_por_id()`.
5. `Flex_U2_U3_Clase4_Menu_CRUD_Excepciones.pdf`: `while True`, `try`, `except`, `else`, `finally`, actualizar correo y borrar con confirmación.

También se incluyen los materiales de las tres primeras clases de Unidad 1, para repasar cómo se construyó el UML.

## Orden para reescribir a mano (sin copiar a ciegas)

**Sesión 1 (20 min):** `src/dominio/empleado.py`. Escribe primero solo `class`, `__init__` y sus asignaciones. Después explica `self`, parámetros, `id=None`. Finalmente agrega un validador y su `@staticmethod`.

**Sesión 2 (20 min):** `src/dominio/departamento.py` y `proyecto.py`. Construye dos objetos y verifica relaciones en memoria. Dibuja qué significa 0..* y por qué `self._empleados` es una lista.

**Sesión 3 (20 min):** `src/dominio/registro_tiempo.py`. Explica por qué se debe asociar a un Empleado y Proyecto antes de guardarlo.

**Sesión 4 (20 min):** `src/presentacion/menu_empleado.py`. Reescribe `solicitar()` y `solicitar_id()` sin mirar. Corrige la indentación de `while True`, `try` y `except`.

**Sesión 5 (20 min):** `src/persistencia/conexion.py`, `empleado_dao.py` y `creacion_bd.py`. Explica por qué hay `?` o `%s`, qué hace `lastrowid`, `fetchone`, `fetchall`, `commit` y `finally`.

**Sesión 6 (20 min):** `empleado_proyecto_dao.py` y `registro_tiempo_dao.py`. Explica la tabla puente y por qué no se debe eliminar un empleado que tiene referencias.

## Indentación fundamental

```python
def solicitar(campo, validador):
    while True:
        texto = input(campo + ": ")
        try:
            return validador(texto)
        except ValueError as error:
            print(error)
```

- `while` está dentro de la función; `try` y `except` están dentro del `while`.
- `except` se alinea con `try`, no con el `return`.
- `return` termina la función entera cuando la validación fue correcta.
- Cuando ocurre `ValueError`, se muestra el mensaje y se repite solamente ese campo.

## Preguntas de recuperación activa

1. ¿Qué representa `self` y qué cambia entre parámetro y atributo?
2. ¿Por qué `Empleado.validar_nombre` se pasa sin `()` a `solicitar`?
3. ¿Qué diferencia hay entre devolver `False` y lanzar `ValueError`?
4. ¿Por qué SQLite requiere `PRAGMA foreign_keys = ON`?
5. ¿Por qué una relación N:M requiere la tabla puente `empleado_proyecto`?
6. ¿Por qué el mensaje de éxito debe aparecer después de `commit()`?
7. ¿Qué diferencia hay entre `break`, `continue` y `return`?

## Experimentos rápidos

- Escribe `Ana123`, luego `Ana Torres` en el menú: solo debes repetir nombre.
- Escribe `abc` como teléfono, luego `+56912345678`: solo debes repetir teléfono.
- Escribe `2026-02-30`: debe pedir nuevamente la fecha real.
- Busca un ID inexistente: `buscar_por_id` devuelve `None`, no un error.
- Intenta eliminar un empleado relacionado con un proyecto: la FK debe impedirlo.

## Reglas extra decididas por el proyecto, no impuestas por el docente

- Dirección: texto no vacío, como máximo 200 caracteres.
- Teléfono: 8 a 15 dígitos, con `+` inicial opcional.
- Salario: número finito no negativo; se escribe sin puntos de miles (`950000`).
- Nombres: letras, espacios y apóstrofes; se conserva la regla de 2–80 de la Clase 3.

Si el docente cambia estas reglas, se ajustan aquí y en los validadores, sin alterar el UML.
