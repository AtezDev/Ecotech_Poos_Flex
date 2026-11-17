# EcoTech Solutions — Programación Orientada a Objetos

**Proyecto académico de Analista Programador · INACAP · Programación Orientada a Objeto Seguro (TI3V21 FLEX)**  
**Repositorio:** [AtezDev/Ecotech_Poos_Flex](https://github.com/AtezDev/Ecotech_Poos_Flex)  
**Guía de diseño:** [`docs/audt_diagr/Diagrama_Final.drawio`](docs/audt_diagr/Diagrama_Final.drawio) — UML definitivo de **tres vistas**.  
**Alcance documentado:** avances hasta **FLEX Unidades 2–3, Clase 4: «Menú y manejo de excepciones»**, más las implementaciones complementarias necesarias para respetar el UML y la **ampliación del CRUD a todas las entidades implementadas** (sección 4, «CRUD completo»).

**Estado de GitHub comprobado:** rama `main`, commit `49432e9` (*actualizacion Readme*, 13 de noviembre de 2026). El estudiante confirmó que las **44 pruebas originales terminaron en `OK` en Windows** y que el `push` de la fusión fue exitoso.

**Ampliación del 17 de noviembre de 2026 (CRUD completo):** se agregan actualización de nombre, dirección, teléfono y salario del empleado, CRUD de Departamento, Proyecto y RegistroTiempo, asignación y cambio de proyecto, y un menú principal que reúne todo (`python src/main.py`). En el entorno de revisión (Linux) pasaron **64/64 pruebas en SQLite** (44 originales, con 4 de ellas ajustadas por el nuevo menú principal, + 20 nuevas) y un recorrido completo del CRUD contra **MariaDB 10.11 con PyMySQL** en una base nueva. **No se ha probado todavía en Windows ni en MySQL de WampServer**: ese paso lo debes hacer tú antes del `push` (sección 8).

> **Principio de EcoTech:** el **UML define qué debe tener y hacer el sistema**; las **diapositivas del profesor enseñan cómo implementarlo**. Simplificamos la escritura y la explicación del código, **no** los atributos, operaciones, relaciones ni multiplicidades del diagrama. Es un proyecto de aprendizaje progresivo, no una aplicación empresarial terminada.

---

## 1. ¿Qué es EcoTech y qué problema aborda?

EcoTech es un sistema de práctica en Python para gestionar información de **empleados**, **departamentos**, **proyectos** y **registros de tiempo**. Permite ejercitar la transición entre el diseño UML, la programación orientada a objetos y la persistencia de datos en una base relacional.

Los materiales de la Unidad 1 plantean un problema habitual: cuando la información está dispersa en planillas o sistemas aislados, aparecen duplicaciones e inconsistencias. El proyecto permite representar los datos como objetos relacionados, aplicar reglas al modificarlos y guardarlos en una base de datos para recuperarlos después de cerrar Python.

El proyecto **no es el informe de evaluación**: este repositorio documenta el desarrollo de las clases, las prácticas y las decisiones técnicas tomadas a partir del UML. Los ejemplos del profesor suelen mostrar un `Empleado` con nombre y correo; nuestro diseño conserva además dirección, teléfono, fecha de contratación, salario e ID, porque así lo exige el UML.

### Objetivos de aprendizaje

1. Leer y justificar clases, atributos, métodos, visibilidad y multiplicidades de un diagrama UML.
2. Implementar objetos Python utilizando `class`, `__init__`, `self`, métodos y asociaciones.
3. Aplicar validaciones reutilizables mediante `@staticmethod`, `@property`, setters y `ValueError`.
4. Persistir y recuperar objetos con SQL parametrizado y el patrón DAO visto en clases.
5. Construir una consola que solicite, valide, consulte, actualice y elimine sin cerrarse por errores de entrada.
6. Utilizar Git/GitHub para conservar avances, trabajar desde distintos computadores y documentar decisiones.
7. Comprender **por qué** funciona cada línea, no únicamente copiar código.

---

## 2. Reglas de trabajo y fuentes de referencia

| Fuente | Responsabilidad en el proyecto |
|---|---|
| **UML final de tres vistas** | Contrato de clases, atributos, tipos, métodos y relaciones. No se rediseña por comodidad del código. |
| **Material de las clases** | Guía pedagógica para implementar cada parte con conceptos efectivamente estudiados. |
| **Scripts de dominio** | Representan objetos, estado, reglas y relaciones en memoria. No ejecutan SQL. |
| **Scripts de persistencia** | Abren conexiones, crean tablas y ejecutan consultas parametrizadas. |
| **Scripts de presentación** | Solicitan datos, comunican errores y mantienen el menú activo. |
| **Pruebas** | Ayudan a comprobar que cada avance nuevo no rompe los anteriores. |
| **`docs/`** | Archivo histórico: versiones de diagramas, material docente, auditorías y guías. **No eliminar ni reemplazar indiscriminadamente.** |

### Material académico utilizado

Los PDF de referencia están en [`docs/material_profesor/`](docs/material_profesor/) y tienen un índice en [`INDICE.md`](docs/material_profesor/INDICE.md):

**Unidad 1 — modelamiento**

- [`U1_Clase1_Introduccion_POO.pdf`](docs/material_profesor/U1_Clase1_Introduccion_POO.pdf): clases, objetos, atributos, tipos, visibilidad y métodos.
- [`U1_Clase2_Modelado_UML.pdf`](docs/material_profesor/U1_Clase2_Modelado_UML.pdf): asociaciones, navegabilidad, multiplicidades, encapsulamiento y evolución del modelo.
- [`U1_Clase3_Relaciones_UML.pdf`](docs/material_profesor/U1_Clase3_Relaciones_UML.pdf): justificación de relaciones, herencia y concepto de polimorfismo.

**Unidad 2 y FLEX — implementación**

- [`01_U2_Del_UML_al_Proyecto.pdf`](docs/material_profesor/01_U2_Del_UML_al_Proyecto.pdf): pasar del UML a Python, entorno virtual, archivos y repositorio.
- [`02_U2_Relaciones_Encapsulamiento.pdf`](docs/material_profesor/02_U2_Relaciones_Encapsulamiento.pdf): referencias entre objetos, listas, multiplicidades y encapsulamiento.
- [`03_U2_SQLite_MySQL_Insert_ID.pdf`](docs/material_profesor/03_U2_SQLite_MySQL_Insert_ID.pdf): conexión SQLite/MySQL, DAO, primer `INSERT` e ID generado.
- [`04_FLEX_Empleado_Valido_Lectura.pdf`](docs/material_profesor/04_FLEX_Empleado_Valido_Lectura.pdf): validación, `@property`, `listar()`, `buscar_por_id()`, `fetchall()` y `fetchone()`.
- [`05_FLEX_Menu_CRUD_Excepciones.pdf`](docs/material_profesor/05_FLEX_Menu_CRUD_Excepciones.pdf): menú, reintentos por campo, `try/except/else/finally`, `UPDATE` y `DELETE` con confirmación.

> **Nota sobre la numeración:** el PDF de persistencia se titula *Unidad 2 · Clase 4*, y el último PDF se titula *FLEX U2–U3 · Clase 4*. Son **dos materiales distintos**; se mantienen aquí sus nombres originales para evitar confusiones.

---

## 3. Estructura del repositorio

```text
Ecotech_Poos_Flex/
├── src/
│   ├── main.py                         # Punto de entrada y demostración anterior
│   ├── dominio/                        # Objetos y reglas del UML
│   │   ├── __init__.py
│   │   ├── empleado.py
│   │   ├── departamento.py
│   │   ├── proyecto.py
│   │   └── registro_tiempo.py
│   ├── persistencia/                   # Bases de datos y DAO
│   │   ├── __init__.py
│   │   ├── conexion.py
│   │   ├── creacion_bd.py
│   │   ├── empleado_dao.py
│   │   ├── departamento_dao.py
│   │   ├── proyecto_dao.py
│   │   ├── empleado_proyecto_dao.py
│   │   └── registro_tiempo_dao.py
│   └── presentacion/                   # Interacción con el usuario
│       ├── __init__.py
│       ├── menu_empleado.py
│       ├── menu_comun.py               # Ayudas compartidas: listar, buscar, eliminar, confirmar
│       ├── menu_departamento.py
│       ├── menu_proyecto.py
│       ├── menu_asignacion.py          # Empleado–Proyecto y Empleado–Departamento
│       ├── menu_registro_tiempo.py
│       └── menu_principal.py           # Menú principal (lo abre python src/main.py)
├── tests/
│   ├── test_ecotech.py                # 44 casos de prueba originales
│   └── test_crud.py                   # 20 casos nuevos del CRUD completo
├── docs/
│   ├── audt_diagr/
│   │   ├── Diagrama_Final.drawio       # UML definitivo: 3 vistas
│   │   └── ALCANCE_Y_AUDITORIA.md
│   ├── material_profesor/             # Diapositivas de las unidades
│   ├── GUIA_CLASE_POR_CLASE.md
│   ├── MAPA_UML_Y_PENDIENTES.md
│   ├── ESTADO_DE_CLASES.md
│   ├── Diagrama.drawio
│   ├── avance_diagrama_v3.drawio
│   ├── avance_v2.drawio
│   ├── diagrama_iteracion_1.drawio
│   └── ...                            # Otros documentos y diagramas históricos
├── .env.example                        # Configuración compartible, sin secretos
├── .gitignore                          # Archivos que Git no debe subir
├── requirements.txt                    # Dependencias externas
└── Readme.md                           # Esta guía
```

El directorio histórico puede contener otros documentos, como `Actividad_Clase3_EcoTech_Formato_INACAP.pdf`, y un archivo previo llamado `ecotech`. **No deben eliminarse solo porque no aparezcan en el esquema resumido.** Conservar el historial ayuda a explicar cómo evolucionó el diagrama.

### Responsabilidad de cada carpeta

- **`dominio/`:** define qué es un Empleado, Departamento, Proyecto o RegistroTiempo, con sus atributos, operaciones y relaciones.
- **`persistencia/`:** transforma operaciones sobre objetos en consultas SQL y viceversa.
- **`presentacion/`:** solicita entradas mediante `input()`, repite campos inválidos y presenta resultados.
- **`tests/`:** comprueba comportamiento en una base SQLite temporal, sin necesitar WampServer.
- **`docs/`:** conserva diseño, decisiones, material de aprendizaje y sus versiones anteriores.

Esta separación se trabaja para **entender responsabilidades**, no para introducir frameworks ni complejidad ajena a las clases.

---

## 4. Desarrollo y aprendizaje clase por clase

Cada etapa distingue **contenido del profesor**, **aplicación en EcoTech** y **aprendizaje obtenido**. Algunas implementaciones de nuestra versión son ampliaciones necesarias para respetar el UML, y no ejemplos literalmente entregados en el PPT.

### Unidad 1 · Clase 1 — Introducción a POO: clases, atributos y métodos

**Material:** `U1_Clase1_Introduccion_POO.pdf`.

**Vimos en clases:** la diferencia entre **clase** y **objeto**, entre nombre/tipo/valor de un atributo, visibilidad (`+` público, `-` privado) y firma de un método (parámetros y tipo de retorno).

**Avance en EcoTech:** identificamos las entidades del caso —Empleado, Departamento, Proyecto y RegistroTiempo— y comenzamos a distinguir qué **sabe** cada una (atributos) y qué **hace** (métodos). Esta etapa es principalmente de análisis: **no presupone que ya exista una base de datos**.

**Qué debemos saber explicar:** `Empleado` es una definición; «Ana Torres» sería una instancia. `correoElectronico: String` declara un dato, mientras `cambiarCorreoElectronico(...)` representa un comportamiento.

### Unidad 1 · Clase 2 — Modelado UML, asociaciones y multiplicidades

**Material:** `U1_Clase2_Modelado_UML.pdf`.

**Vimos en clases:** diagramas de clases, asociaciones, navegabilidad, multiplicidades, encapsulamiento, generalización y el valor de justificar cada relación con el caso. El material propone conservar revisiones del UML y explicar las decisiones.

**Avance en EcoTech:** construimos y revisamos versiones del diagrama. Las conservamos en `docs/` en vez de dejar únicamente la versión final. El modelo relaciona empleados con departamentos, proyectos y registros de tiempo.

**Qué debemos saber explicar:** `1`, `0..1` y `0..*` expresan cantidades distintas. Una asociación no es automáticamente herencia; **un Empleado participa en un Proyecto**, pero no «es un tipo de Proyecto».

### Unidad 1 · Clase 3 — Relaciones, herencia y polimorfismo

**Material:** `U1_Clase3_Relaciones_UML.pdf`.

**Vimos en clases:** profundización de asociaciones y multiplicidades, criterio «ES UN» para decidir herencia y noción de polimorfismo. Antes de programar, el modelo debe justificar sus responsabilidades.

**Avance en EcoTech:** consolidamos las relaciones del diseño. El UML final conserva la relación **muchos a muchos (N:M)** entre Empleado y Proyecto, sin introducir una herencia artificial. Las clases de informes y autorización quedaron representadas como parte del alcance global.

**Distinción importante:** haber estudiado **el concepto** de polimorfismo no significa que este proyecto ya implemente una jerarquía polimórfica. No añadimos subclases solo para demostrarlo.

### Unidad 2 · Clase 1 — Del UML al proyecto Python

**Material:** `01_U2_Del_UML_al_Proyecto.pdf`.

**Vimos en clases:** traducción de una clase UML a `class`, constructor `__init__`, uso de `self`, creación de objetos, `main.py`, entorno virtual `.venv` y respaldo con Git.

**Avance en EcoTech:** estructuramos `src/` por carpetas, creamos las clases principales y organizamos un punto de entrada. La versión Python comienza a reflejar las decisiones del UML en lugar de inventar un modelo nuevo.

Un constructor sencillo de Empleado mantiene los datos exigidos por el diagrama:

```python
from datetime import date

class Empleado:
    def __init__(self, nombre, direccion, telefono,
                 correoElectronico, fechaInicioContrato,
                 salario, id=None):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.fechaInicioContrato = fechaInicioContrato
        self.salario = salario
```

**Este fragmento ilustra los atributos, no sustituye el constructor real**, que también utiliza setters y validadores. Las reglas se mantienen en métodos separados para conservar claridad, sin permitir que se construyan objetos inválidos.

**Qué debemos saber explicar:** `self.nombre` es un atributo del objeto; `nombre` es un parámetro. `id=None` representa un empleado todavía no guardado en la base de datos.

### Unidad 2 · Clase 2 — Relaciones, colecciones y encapsulamiento

**Material:** `02_U2_Relaciones_Encapsulamiento.pdf`.

**Vimos en clases:** traducir las multiplicidades del UML a referencias o colecciones de Python, encapsular cambios y comprobar que dos objetos colaboren sin duplicar innecesariamente sus datos.

**Avance en EcoTech:**

- `Departamento` conserva una lista interna de objetos `Empleado`, con `agregar_empleado()`, `asignarEmpleado()` y `reasignarEmpleado()`.
- `Empleado` mantiene `departamento` y una colección `_proyectos` para representar sus asociaciones en memoria.
- `Empleado.asignarAProyecto()` y `desasignarDeProyecto()` gestionan la referencia a objetos Proyecto.
- `RegistroTiempo` se vincula con un Empleado y un Proyecto cuando se registra el trabajo.
- Los cambios de nombre/correo se apoyan en encapsulamiento y propiedades, evitando asignaciones que eludan sus reglas.

**Qué debemos saber explicar:** guardar `Empleado` dentro de una colección no significa guardar solo su nombre. Una lista representa «muchos» en memoria; después, la base de datos necesitará otra representación para la relación N:M.

### Unidad 2 · Material de persistencia — SQLite/MySQL, primer INSERT e ID

**Material:** `03_U2_SQLite_MySQL_Insert_ID.pdf` (en la portada original se denomina **Unidad 2, Clase 4**).

**Vimos en clases:** diferencia entre objeto en memoria y registro persistente; conexión; separación dominio/persistencia; creación de tablas; DAO; `INSERT`, parámetros SQL, `cursor.lastrowid`, `commit()` y cierre de conexiones.

**Avance en EcoTech:**

- `conexion.py` abre SQLite o MySQL según las variables de `.env`.
- `creacion_bd.py` crea las tablas necesarias del modelo y verifica columnas esenciales si la tabla ya existía.
- Los DAO (`EmpleadoDAO`, `DepartamentoDAO`, `ProyectoDAO`, `RegistroTiempoDAO`) realizan las inserciones pertinentes.
- `EmpleadoDAO.insertar()` obtiene el ID generado por la base de datos y lo asigna al objeto después de confirmar el registro.
- `EmpleadoProyectoDAO` representa en SQL la relación N:M mediante la tabla puente `empleado_proyecto`.

**Relación fundamental:** `Empleado` **no** debe conocer la sintaxis de SQLite/MySQL; el DAO sí. De esta forma podemos aprender a persistir un objeto sin mezclar todas las responsabilidades en `empleado.py`.

Ejemplo ilustrativo de una sentencia parametrizada:

```python
marcador = "?" if obtener_motor() == "sqlite" else "%s"
sql = f"SELECT id FROM empleado WHERE id = {marcador}"
cursor.execute(sql, (id_empleado,))
```

Los valores se pasan por separado; **no** se concatenan entradas del usuario dentro del SQL. En SQLite se usa `?` y en PyMySQL `%s`.

**Qué debemos saber explicar:** `lastrowid` devuelve la identidad generada al insertar; `commit()` confirma la operación; `close()` libera la conexión. Los DAO de esta versión utilizan `finally` para asegurar el cierre.

### FLEX · Unidades 2–3 · Clase 3 — Empleado válido y lectura de datos

**Material:** `04_FLEX_Empleado_Valido_Lectura.pdf`.

**Vimos en clases:** reglas de nombre y correo, `strip()`, `@property`, setters, `raise ValueError`, `fetchall()`, `fetchone()`, listas de objetos, búsqueda por ID y resultado `None` cuando no existe un registro.

**Avance en EcoTech:**

- `Empleado` valida nombre y correo antes de conservar sus valores.
- Se agregaron validadores para **dirección, teléfono, fecha de contrato y salario**, porque el UML exige más campos que el ejemplo reducido del profesor.
- La fecha se maneja con objetos `datetime.date`, no como texto arbitrario dentro del dominio.
- `EmpleadoDAO.listar()` ejecuta `SELECT`, transforma las filas en objetos `Empleado` y devuelve `[]` si no hay resultados.
- `EmpleadoDAO.buscar_por_id()` obtiene una fila y devuelve `Empleado` o `None`.
- Los setters mantienen los valores anteriores si se rechaza un cambio inválido.

**Reglas adicionales de nuestra implementación**, sujetas a ajustes si el docente define otras: nombre de 2–80 caracteres; dirección no vacía y hasta 200 caracteres; teléfono con 8–15 dígitos y `+` opcional; salario numérico, finito y no negativo. El correo requiere usuario, una `@`, un dominio con punto y ausencia de espacios; **no está restringido solo a `.com`**. Estas reglas concretas no deben atribuirse todas al profesor.

**Qué debemos saber explicar:** `isalpha()` sirve para comprobar letras (con adecuaciones si se permiten espacios y apóstrofes); `isdigit()` comprueba texto de dígitos; `isfinite()` evita `NaN` e infinitos en los cálculos del salario. `ValueError` comunica una entrada inválida; `None` en `buscar_por_id()` es un resultado normal, no necesariamente una excepción.

### FLEX · Unidades 2–3 · Clase 4 — Menú, excepciones y operaciones CRUD

**Material:** `05_FLEX_Menu_CRUD_Excepciones.pdf`.

**Vimos en clases:** `while True` para mantener el menú activo; validación por campo; `try`, `except`, `else`, `finally`; distinción entre opción inválida, conversión inválida, ID inexistente y falla de base de datos; ejemplos de `UPDATE` y `DELETE`.

**Avance en EcoTech:**

- `src/presentacion/menu_empleado.py` implementa un menú repetitivo.
- `solicitar(campo, validador)` reutiliza funciones de validación; el usuario repite **solo el campo incorrecto**.
- `solicitar_fecha()` convierte texto `AAAA-MM-DD` a `date` con `date.fromisoformat()`.
- `solicitar_salario()` comprueba el texto antes de convertirlo a número.
- `solicitar_id()` convierte con `int()` y pide un entero positivo.
- La consola permite **registrar, listar, buscar, actualizar el correo y eliminar** un empleado.
- `confirmar_eliminacion()` acepta únicamente `s` o `n` (sin importar mayúsculas ni espacios externos); otras entradas se vuelven a pedir.
- El menú captura errores específicos de integridad y operación de SQLite o PyMySQL, según el motor configurado.
- El DAO aplica `UPDATE ... WHERE id = ?/%s` y `DELETE ... WHERE id = ?/%s`, confirmando sus cambios con `commit()`.

La función central de la clase es sencilla y reutilizable:

```python
def solicitar(campo, validador):
    while True:
        valor = input(f"{campo}: ")
        try:
            return validador(valor)
        except ValueError as error:
            print(f"{campo} inválido: {error}")
```

**Indentación:** `while True` está dentro de `solicitar`; `try` y `except` están alineados entre sí dentro del ciclo; `return` termina la función cuando el dato es válido. Aquí `validador` recibe **una función**, no un booleano: por ejemplo, `solicitar("Nombre", Empleado.validar_nombre)`.

**Estado del CRUD de Empleado al cierre de la Clase 4** (la ampliación posterior está en la sección siguiente):

| Operación | Empleado | Observación |
|---|---|---|
| **C — Create** | Implementada | `insertar()` guarda y obtiene el ID. |
| **R — Read** | Implementada | `listar()` y `buscar_por_id()`. |
| **U — Update** | **Parcial en la Clase 4** | En la clase se actualiza **solo el correo**; luego se amplió (ver sección siguiente). |
| **D — Delete** | Implementada con controles | Se busca el empleado, se pide confirmación y se intenta eliminar por ID. Las FK pueden impedirlo si tiene relaciones. |

**Estado al cierre de la Clase 4:** faltaba cambiar desde el menú la dirección, el teléfono, el salario y el nombre; gestionar proyectos por el menú; asignar proyectos por el menú; y el CRUD de las demás entidades. **Todo eso se resolvió en la ampliación descrita en la sección siguiente.**


### FLEX — CRUD completo de todas las entidades (ampliación del 17 de noviembre)

**Qué pedía el proyecto:** si cambia el teléfono, la dirección, el nombre o el salario de un empleado, debe poder actualizarse; los proyectos deben poder registrarse, modificarse y eliminarse; un empleado puede dejar un proyecto y recibir otro; lo mismo para departamentos y registros de tiempo.

**Qué se reutilizó de las clases (no se inventó nada nuevo):** `@staticmethod`, métodos `obtener…/cambiar…` del UML, `solicitar(campo, validador)`, `while True`, `if/elif`, `for … in` con `append`, `try/except/else`, `finally`, SQL parametrizado (`?` en SQLite, `%s` en PyMySQL), `commit()` y `close()`. El patrón de actualizar es el de la diapositiva «Actualizar el correo de un empleado encontrado» de la Clase 4 (buscar → validar → comparar → guardar → comprobar `filas == 1`). Se evitaron a propósito las comprensiones de lista, `lambda`, `getattr/setattr` y pasar métodos de instancia como argumentos, porque no se han visto en clases. **Una excepción:** `cursor.rowcount` (ya usado en tu `EmpleadoDAO.actualizar/eliminar`) no aparece en las diapositivas revisadas; su uso aquí sigue ese precedente de tu código.

**Decisión de estilo:** por ahora el código nuevo **no lleva comentarios**; la explicación está en este README.

#### Qué se agregó, archivo por archivo

| Archivo | Qué hace | Detalle que conviene entender |
|---|---|---|
| `persistencia/empleado_dao.py` | `actualizar()` ahora guarda **nombre, dirección, teléfono, correo y salario** con un solo `UPDATE`. | El objeto ya validó los datos con `cambiarNombre()`, `cambiarDireccion()`, etc. El DAO solo guarda lo que el objeto tiene. |
| `persistencia/departamento_dao.py` | `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()`, `asignar_empleado()`, `quitar_empleado()`, `listar_empleados()`. | `asignar_empleado()` cambia `empleado.departamento_id`; como es una sola columna, un empleado solo puede estar en **un** departamento (multiplicidad 0..1 del UML). Quitarlo es poner `NULL`. |
| `persistencia/proyecto_dao.py` | `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()`. | La fecha se guarda como texto ISO y se reconstruye con `date.fromisoformat(str(fecha))`, igual que en Empleado. |
| `persistencia/empleado_proyecto_dao.py` | Se agrega `desasignar(empleado, proyecto)`. | Devuelve `True` si borró la pareja y `False` si no existía. |
| `persistencia/registro_tiempo_dao.py` | `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()` y `reconstruir()`. | `reconstruir()` arma el objeto y vuelve a cargar su Empleado y su Proyecto con los DAO que ya existían. Solo se actualizan fecha, horas y tarea; empleado y proyecto **no se cambian** (para eso se elimina y se crea otro registro). |
| `presentacion/menu_empleado.py` | Opciones **6** (dirección), **7** (teléfono), **8** (nombre) y **9** (salario). Las opciones 1 a 5 no cambian. | Una función por dato (`actualizar_direccion()`, etc.), todas con el mismo molde, más `solicitar_id_de()`. |
| `presentacion/menu_comun.py` | `listar_todo()`, `buscar_uno()`, `eliminar_con_confirmacion()`, `confirmar()`, `validar_texto_obligatorio()`, `validar_horas()`. | Evita repetir el mismo bloque `try/except` en cada menú. |
| `presentacion/menu_departamento.py`, `menu_proyecto.py`, `menu_registro_tiempo.py` | Un menú CRUD por entidad. | Siguen el molde del menú de empleados: `while True`, opciones con `if/elif`, `0` para volver. |
| `presentacion/menu_asignacion.py` | Asignar/quitar empleado de proyecto; ver proyectos de un empleado y empleados de un proyecto; asignar/quitar empleado de departamento; ver empleados de un departamento. | Aquí se resuelve «se le asigna otro proyecto»: se quita el anterior y se asigna el nuevo. |
| `presentacion/menu_principal.py` | Menú principal que enlaza todos los demás. | Se abre con `python src/main.py`. |
| `main.py` | Sin argumentos abre ahora el **menú principal** (antes abría directo el menú de empleados). | `--demo` y `--listar` no cambiaron. |
| `tests/test_crud.py` | 20 pruebas nuevas. | En `tests/test_ecotech.py` solo se ajustaron 4 pruebas de menú (39 a 42): ahora escriben primero `1` para entrar a Empleados y terminan con otro `0` para salir del menú principal. |

#### El molde de cada actualización

Cada dato tiene su propia función, todas iguales salvo por el nombre del dato. Este es el molde, con la dirección del empleado como ejemplo:

```python
def actualizar_direccion():
    id_empleado = solicitar_id_de("empleado")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe empleado con ese ID.")
            return
        nuevo = solicitar("Dirección", Empleado.validar_direccion)
        if nuevo == empleado.obtenerDireccion():
            print("El valor es el mismo; no hay cambios.")
            return
        empleado.cambiarDireccion(nuevo)
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Dirección actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")
```

Es el mismo recorrido de esa diapositiva, aplicado a otro dato:

| Paso | Línea | Para qué sirve |
|---|---|---|
| 1 | `EmpleadoDAO.buscar_por_id(...)` | Traer el objeto desde la base de datos; devuelve el objeto o `None`. |
| 2 | `if empleado is None` | Resultado normal («no existe»): se resuelve con `if`, no con excepción. |
| 3 | `solicitar("Dirección", Empleado.validar_direccion)` | Pedir el dato y repetir **solo ese campo** hasta que sea válido. Aquí se pasa una **función sin paréntesis**. |
| 4 | `if nuevo == empleado.obtenerDireccion()` | Detectar «sin cambios» con el método `obtener…` del UML. |
| 5 | `empleado.cambiarDireccion(nuevo)` | Aplicar el cambio con el método `cambiar…` del UML. |
| 6 | `EmpleadoDAO.actualizar(empleado)` | Ejecutar el `UPDATE ... WHERE id` y devolver cuántas filas cambió. |
| 7 | `except` / `else` | Los errores de BD se capturan; el mensaje de éxito va en `else`, solo cuando todo terminó bien. |

Las demás funciones (`actualizar_nombre`, `actualizar_telefono`, `actualizar_salario`, y las de departamento, proyecto y registro de tiempo) cambian únicamente el DAO, el validador y los métodos `obtener…/cambiar…`.

**Por qué se compara con el valor actual:** en MySQL, un `UPDATE` que deja el mismo valor devuelve 0 filas, y eso parecería un error. Detectar «sin cambios» antes evita ese falso fallo.

**Por qué hay tanto código repetido:** es a propósito. Se prefirió el estilo de las clases (una función clara por acción) a un truco más corto que aún no se ha enseñado. Cuando se vean funciones más avanzadas, esta repetición se podrá reducir.

#### Reglas de integridad (qué NO se puede hacer, a propósito)

| Operación | Resultado | Por qué |
|---|---|---|
| Eliminar un departamento con empleados | Rechazado | La FK `empleado.departamento_id` lo impide. Primero se quita o reasigna a los empleados. |
| Eliminar un proyecto con empleados asignados | Rechazado | La FK de `empleado_proyecto` lo impide. Primero se quita la asignación. |
| Quitar a un empleado de un proyecto donde tiene horas registradas | Rechazado | La FK compuesta de `registro_tiempo` lo impide. Primero se eliminan esos registros. |
| Registrar horas en un proyecto no asignado | Rechazado | `RegistroTiempoDAO.insertar()` lo comprueba. |
| Eliminar un empleado con proyectos | Rechazado | Ya estaba implementado en la Clase 4. |

No hay `ON DELETE CASCADE`: la base de datos **nunca borra datos relacionados en silencio**.

#### Decisión pendiente: «terminar un proyecto»

El UML define `Proyecto` solo con `nombre`, `descripcion` y `fechaInicio`: **no tiene estado ni fecha de término**. Por eso, en esta versión, «un empleado terminó un proyecto» se resuelve **quitando su asignación** (menú *Asignaciones*, opción 2). Si el profesor quiere un estado «terminado» o una fecha de término, eso significa **agregar un atributo al UML y una columna a la base de datos**, y no se hizo sin tu autorización.

#### Cómo probarlo a mano

```bash
python src/main.py
```

1. **Departamentos** → registrar «Desarrollo».
2. **Proyectos** → registrar «EcoTech» con fecha `2026-11-17`.
3. **Empleados** → registrar uno y luego probar las opciones 6, 7, 8 y 9.
4. **Asignaciones** → asignar el empleado al proyecto y al departamento; luego quitarlo del proyecto y asignarle otro.
5. **Registros de tiempo** → registrar horas; luego intentar quitar al empleado de ese proyecto y leer el mensaje.

**Preguntas de recuperación activa (respóndelas sin mirar el código):**

- En `solicitar("Dirección", Empleado.validar_direccion)`, ¿por qué `validar_direccion` va **sin paréntesis**?
- ¿Qué pasa si escribes la misma dirección que ya tiene el empleado, y por qué?
- ¿Por qué no se puede eliminar un departamento con empleados? ¿Qué debes hacer antes?
- ¿Por qué cambiar de proyecto son dos operaciones (quitar y asignar) y no un `UPDATE`?
- **Feynman:** explícale a un compañero, en tres frases, por qué `RegistroTiempo` impide quitar a un empleado de un proyecto con horas registradas.
- **Palacio de la memoria:** coloca en tu casa cinco objetos: `buscar_por_id` (puerta de entrada), `solicitar` (recibidor), `obtener…` (sala), `cambiar…` (cocina), `actualizar` del DAO (dormitorio). Recorre la casa en ese orden.

---

## 5. UML definitivo: clases, atributos, relaciones y estado

El diagrama se conserva en tres vistas: **(1) modelo de clases**, **(2) relaciones de Informe y autorización** y **(3) constructores, accesores y validaciones**. Es el contrato principal para continuar.

| Clase del UML | Contenido | Estado actual |
|---|---|---|
| **Empleado** | `idEmpleado`, `nombre`, `direccion`, `telefono`, `correoElectronico`, `fechaInicioContrato`, `salario`; getters, cambios y asignaciones a proyectos. | Implementación funcional del dominio, validadores, persistencia y **CRUD completo** (actualiza nombre, dirección, teléfono, correo y salario). `id` representa técnicamente `idEmpleado`. |
| **Departamento** | `nombre`, `gerente`, asociación a empleados, operaciones de asignación y gestión. | Objeto, lista de empleados, asignación/reasignación y **CRUD SQL** (registrar, listar, buscar, actualizar nombre y gerente, eliminar, asignar y quitar empleados). Los métodos del UML `crearDepartamento`, `modificarDepartamento`, `buscarDepartamento` y `eliminarDepartamento` **siguen sin existir como métodos de la clase**: su función la cumplen hoy el DAO y el menú. |
| **Proyecto** | `nombre`, `descripcion`, `fechaInicio`, operaciones de creación/modificación/eliminación previstas. | Objeto, cambios de atributos y **CRUD SQL** (registrar, listar, buscar, actualizar nombre, descripción y fecha, eliminar). Los métodos `crearProyecto`, `modificarProyecto` y `eliminarProyecto` **siguen sin existir como métodos de la clase**: los cubren el DAO y el menú. |
| **RegistroTiempo** | `fecha`, `horasTrabajadas`, `descripcionTarea`, relación con Empleado y Proyecto. | Objeto, validaciones, asociación, inserción condicionada a proyecto asignado y **CRUD SQL** (listar, buscar, actualizar fecha/horas/tarea, eliminar). |
| **Informe** | Generar informes de empleados, departamentos, proyectos y registros de tiempo; recibe `ControlAcceso`. | **Pendiente** en Python. |
| **CuentaUsuario** | Nombre de usuario, información protegida de contraseña, sal y rol; comprobación de credenciales. | **Pendiente** en Python. |
| **ControlAcceso** | Autenticación, autorización, sesión y usuario autenticado. | **Pendiente** en Python. |

Algunos métodos del UML, como `crearDepartamento`, `modificarDepartamento`, `buscarDepartamento`, `eliminarDepartamento`, `crearProyecto`, `modificarProyecto` y `eliminarProyecto`, **no están completos**. No se deben presentar como implementados solo porque existan métodos para cambiar atributos o una operación de inserción.

### La multiplicidad Empleado–Proyecto N:M no se cambia

Un empleado puede participar en varios proyectos y un proyecto puede tener varios empleados. En Python, `Empleado._proyectos` permite mantener referencias; en SQL, esa multiplicidad se representa con una **tabla puente**, no con una nueva subclase:

```text
empleado                empleado_proyecto                  proyecto
--------                -----------------                  --------
id (PK)  ─────────────── empleado_id (FK, PK)               id (PK)
                         proyecto_id  (FK, PK) ──────────── id (PK)
```

La tabla `empleado_proyecto` utiliza una **clave primaria compuesta** `(empleado_id, proyecto_id)` para impedir asignaciones duplicadas. `EmpleadoProyectoDAO.asignar()` revisa la pareja antes de insertarla, y existen consultas para recuperar proyectos de un empleado y empleados de un proyecto.

### RegistroTiempo depende de una asignación válida

La tabla `registro_tiempo` guarda `empleado_id` y `proyecto_id` y utiliza una **clave foránea compuesta** hacia `empleado_proyecto`. Además, `RegistroTiempoDAO.insertar()` verifica que esa pareja esté registrada. Por eso **no se pueden guardar horas de un empleado en un proyecto al que no está asignado**.

El modelo tampoco utiliza `ON DELETE CASCADE` para borrar automáticamente esas relaciones: si un empleado tiene referencias existentes, la base de datos puede impedir su eliminación mediante una restricción de integridad. El menú explica el problema en lugar de borrar datos relacionados silenciosamente.

---

## 6. Bases de datos, esquema y DAO

### Tablas implementadas

| Tabla | Datos esenciales | Relación |
|---|---|---|
| `departamento` | `id`, `nombre`, `gerente` | Departamento independiente; empleado puede referenciarlo. |
| `empleado` | `id`, `nombre`, `direccion`, `telefono`, `correo`, `fecha_inicio_contrato`, `salario`, `departamento_id` | `departamento_id` es FK opcional. |
| `proyecto` | `id`, `nombre`, `descripcion`, `fecha_inicio` | Entidad de proyectos. |
| `empleado_proyecto` | `empleado_id`, `proyecto_id` | Tabla puente N:M, PK compuesta y dos FK. |
| `registro_tiempo` | `id`, `fecha`, `horas_trabajadas`, `descripcion_tarea`, `empleado_id`, `proyecto_id` | FK compuesta a `empleado_proyecto`. |

### Funciones de persistencia disponibles

| Archivo | Funciones principales | Alcance |
|---|---|---|
| `conexion.py` | `obtener_motor()`, `abrir_conexion()` | Configura SQLite/MySQL. |
| `creacion_bd.py` | `crear_tablas()` | Revisa tablas existentes y crea las cinco tablas. No migra bases antiguas. |
| `empleado_dao.py` | `insertar()`, `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()` | CRUD completo; `actualizar()` guarda nombre, dirección, teléfono, correo y salario. |
| `departamento_dao.py` | `insertar()`, `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()`, `asignar_empleado()`, `quitar_empleado()`, `listar_empleados()` | CRUD y pertenencia de empleados al departamento. |
| `proyecto_dao.py` | `insertar()`, `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()` | CRUD completo. |
| `empleado_proyecto_dao.py` | `asignar()`, `desasignar()`, `listar_por_empleado()`, `listar_por_proyecto()` | Persistencia de la relación N:M, quitar asignaciones y lectura de ambas direcciones. |
| `registro_tiempo_dao.py` | `insertar()`, `listar()`, `buscar_por_id()`, `actualizar()`, `eliminar()`, `reconstruir()` | Inserta solo cuando hay una asignación válida; actualiza fecha, horas y tarea. |

`cursor.execute(sql, parametros)` recibe valores separados del texto SQL. `fetchall()` recupera todas las filas; `fetchone()` recupera una fila o `None`. `cursor.rowcount` permite comprobar cuántas filas modificó o eliminó una operación; `cursor.lastrowid` obtiene el identificador de un `INSERT`.

### ¿SQLite o MySQL?

- **SQLite:** se utiliza para practicar sin servidor y para las pruebas automáticas. `conexion.py` activa `PRAGMA foreign_keys = ON` en cada conexión.
- **MySQL:** se conecta mediante `PyMySQL` a una base de prueba, por ejemplo en WampServer; las tablas se crean con `ENGINE=InnoDB`. Es una posibilidad implementada en código, **no una ejecución de MySQL ya comprobada en el equipo del estudiante**.
- En SQLite los parámetros usan `?`; en PyMySQL usan `%s`.
- Los archivos `.db`, las credenciales y el entorno virtual son **locales** y se excluyen de Git.

> **Base histórica:** no utilices la antigua base `ecotech` (tabla `empleado` con tres columnas: `id`, `nombre`, `correo`) para ejecutar automáticamente el modelo ampliado. Trabaja en `ecotech_practica`. `crear_tablas()` detecta algunas columnas esenciales incompatibles, pero **no constituye un sistema de migraciones** ni una auditoría integral de índices y restricciones existentes.

---

## 7. Instalación y ejecución en Windows / Git Bash

### Requisitos

- Python 3 con `venv` y `pip`.
- Git y Git Bash (para los comandos que utilizan `source`, `cp`, etc.).
- `requirements.txt` con **PyMySQL** y **python-dotenv**.
- SQLite viene con la biblioteca estándar de Python; `sqlite3`, `datetime`, `pathlib` y `unittest` no requieren instalarse mediante pip.
- WampServer/MySQL es **opcional para la primera práctica**; se utiliza si queremos comprobar ese motor por separado.

### Primera instalación: clonar y preparar

```bash
git clone https://github.com/AtezDev/Ecotech_Poos_Flex.git
cd Ecotech_Poos_Flex
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Si `py` no está disponible en ese computador, utiliza el comando de Python que tengas instalado (`python -m venv .venv`). Si `.env` **ya existe**, **no lo sobrescribas**: conserva la configuración local que estabas utilizando.

Una terminal nueva puede necesitar reactivar el entorno:

```bash
source .venv/Scripts/activate
```

Si aparece `ModuleNotFoundError: No module named 'dotenv'`, comprueba la activación de `.venv` y ejecuta `python -m pip install -r requirements.txt`; no hace falta reescribir `conexion.py` por ese error.

### Configuración inicial con SQLite

En el archivo local `.env`:

```dotenv
DB_ENGINE=sqlite
DB_NAME=ecotech_practica.db
```

La aplicación crea `ecotech_practica.db` en la raíz del proyecto al ejecutar la preparación de tablas. Ese archivo **no se comparte por Git**.

### Configuración alternativa con MySQL

Crear primero una **base de práctica nueva** en phpMyAdmin o MySQL Workbench:

```sql
CREATE DATABASE ecotech_practica CHARACTER SET utf8mb4;
```

Después, configurar **solo tu archivo local** `.env`:

```dotenv
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech_practica
DB_USER=root
DB_PASSWORD=
```

Ajustar host, puerto, usuario y contraseña a tu instalación real. **No subir credenciales a GitHub.** La creación/consulta real con MySQL y sus claves foráneas debe comprobarse antes de considerarla verificada.

### Comandos del programa

Desde la raíz del repositorio:

```bash
python src/main.py
```

Abre el **menú principal** con todas las entidades:

```text
1. Empleados
2. Departamentos
3. Proyectos
4. Asignaciones
5. Registros de tiempo
0. Salir
```

La opción **1. Empleados** abre el menú de empleados, cuyas opciones son:

```text
1. Registrar empleado
2. Listar empleados
3. Buscar empleado por ID
4. Actualizar correo
5. Eliminar empleado
6. Actualizar dirección
7. Actualizar teléfono
8. Actualizar nombre
9. Actualizar salario
0. Salir
```

En cada submenú, la opción `0` vuelve al menú principal.

Para consultar empleados sin registrar nuevos:

```bash
python src/main.py --listar
```

Para repetir la demostración de Departamento, Proyecto, Empleado, relación N:M y RegistroTiempo:

```bash
python src/main.py --demo
```

**Atención:** `--demo` realiza inserciones reales. Cada ejecución puede agregar registros de ejemplo. Úsalo únicamente en una base de práctica, no sobre datos importantes.

---

## 8. Pruebas automatizadas y errores que aprendimos a resolver

### Ejecutar las pruebas

```bash
python -m compileall -q src
python -m unittest discover -s tests -v
```

La versión actual contiene **64 pruebas**: 44 en `tests/test_ecotech.py` y 20 en `tests/test_crud.py`. En el entorno de revisión (Linux) se comprobó **64/64 `OK` en SQLite**. Las 44 originales ya las confirmaste en tu computador Windows (antes del ajuste de 4 pruebas de menú); **ni ese ajuste ni las 20 nuevas se han ejecutado todavía en Windows**. Además, el CRUD completo se recorrió contra MariaDB 10.11 con PyMySQL en una base nueva. Nada de esto sustituye una prueba real con MySQL/WampServer.

Las pruebas cubren, entre otros aspectos:

- Creación de cinco tablas e integridad de claves foráneas.
- Validación de nombre, correo, dirección, teléfono, fecha y salario.
- Comprobación de `@property`, setters y conservación de datos válidos.
- Inserción, recuperación del ID y prevención de inserciones duplicadas del mismo objeto.
- Listado vacío `[]`, búsqueda existente y búsqueda inexistente `None`.
- Asociación N:M en ambos sentidos, sin registrar pares duplicados.
- RegistroTiempo con y sin asignación previa a Proyecto.
- Detección de tablas antiguas incompatibles sin borrar sus registros.
- Actualización del correo y eliminación de empleados sin referencias.
- Bloqueo de eliminación cuando existen relaciones.
- Reintentos individuales de entradas inválidas y cancelación de eliminación.

### Aprendizaje: `WinError 32` con SQLite en Windows

Al trabajar con bases temporales en `unittest`, Windows puede rechazar la limpieza porque el archivo `.db` sigue abierto. Aprendimos que:

```python
with sqlite3.connect(ruta) as conexion:
    ...
```

controla el **contexto transaccional**, pero **no garantiza cerrar** por sí solo la conexión. En pruebas que crean archivos temporales utilizamos:

```python
from contextlib import closing

with closing(sqlite3.connect(ruta)) as conexion:
    ...
```

De esa manera `closing()` cierra la conexión al salir del bloque y `tearDown()` puede limpiar el directorio temporal. La versión de reemplazo incorpora esa corrección para las pruebas 27 y 28.

### Aprendizaje: errores de consola y de base de datos

| Caso | Qué esperamos hacer |
|---|---|
| Opción fuera del menú | Mensaje `if/else`; repetir el menú. |
| ID como `abc` | `int()` produce `ValueError`; repetir solo el ID. |
| Nombre, correo, fecha o salario inválidos | El validador lanza `ValueError`; repetir solo ese campo. |
| ID sin coincidencia | `buscar_por_id()` devuelve `None`; mostrar «No existe». |
| Restricción referencial al borrar | `IntegrityError`; explicar que hay relaciones o restricciones. |
| Problema de operación de BD | `OperationalError`; no anunciar éxito. |
| Operación confirmada | `else` puede mostrar éxito después del `commit()`. |
| Conexión que debe cerrarse | `finally` asegura el cierre dentro del DAO. |

No conviene capturar indiscriminadamente con `except:` o `except Exception:`: la Clase 4 indica capturar **la causa concreta** que podemos tratar.

---

## 9. Git y GitHub: comandos que utilizamos

### Conceptos básicos

- **Repositorio local:** carpeta del computador, con historial en `.git/`.
- **Repositorio remoto:** la copia en GitHub, normalmente identificada como `origin`.
- **`main`:** rama principal de trabajo.
- **`git add`:** prepara cambios; **no** los sube.
- **`git commit`:** registra los cambios preparados en el historial local.
- **`git push`:** envía los commits locales al remoto.
- **`git fetch`:** descarga la información del remoto sin modificar automáticamente los archivos locales.
- **`git merge`:** integra historias, a veces con conflictos que hay que resolver.

### Revisar antes de crear un commit

```bash
git status
git diff --stat
git diff --check
git check-ignore -v .env
git ls-files .env
```

`git ls-files .env` debe quedar vacío: significa que el archivo privado no está siendo seguido. La salida de `git check-ignore -v .env` debe mostrar una regla del `.gitignore`. **Nunca incluyas `.env` ni `.venv` en un commit.**

### Actualizar este README y eliminar un TXT de reemplazo

En la fusión se publicó un archivo transitorio llamado **`LEEME_ANTES_DE_REEMPLAZAR.txt`**. Ya no es necesario conservarlo en la raíz. Una vez copiado este `Readme.md` dentro del repositorio, ejecuta:

```bash
git status
git rm -- LEEME_ANTES_DE_REEMPLAZAR.txt
git add Readme.md
git diff --cached --check
git diff --cached --stat
git commit -m "Documentar avances por clase y retirar archivo temporal"
git push origin main
git status
```

`git rm` elimina un archivo **seguido por Git** y deja preparada la eliminación para el próximo commit. A diferencia de `rm`, no tienes que hacer un `git add -A` adicional para registrar la baja. Si el archivo ya no está en esa copia de trabajo, consulta `git status` antes de repetir el comando. **Nunca uses `git rm` sobre `docs/` para limpiar diagramas históricos.**

Para comprobar los scripts antes de cualquier cambio posterior:

```bash
python -m compileall -q src
python -m unittest discover -s tests -v
```

`git add -A` añade **también eliminaciones**. Antes de usarlo hay que revisar especialmente que no aparezcan documentos de `docs/` eliminados por accidente. No borres diagramas antiguos para «limpiar» el repositorio.

### Si trabajaste desde dos computadores y el push es rechazado

Un error como `main -> main (fetch first)` suele indicar que GitHub tiene commits que tu computador aún no integra. **No utilices `git push --force` para resolverlo.** Primero:

```bash
git status
git fetch origin
git log --oneline --graph --decorate --all -10
```

Si ya tienes un commit local y no hay operaciones de Git pendientes, puedes crear una referencia de respaldo antes de combinar historias:

```bash
git branch respaldo-atez-antes-merge
```

Después se decide cómo integrar los cambios; `git merge origin/main` puede generar conflictos. Para resolverlos, **revisar cada archivo** y elegir qué se conserva. `--ours` es la versión de la rama local en ese merge y `--theirs` la que se integra; no se debe aplicar automáticamente a todos los archivos sin comparar las diferencias.

**Si la terminal muestra `(main|MERGING)`**, ya hay un merge abierto. No inicies otro ni ejecutes `git pull` a ciegas. Tras resolver y guardar los archivos, comprueba:

```bash
git status
git diff --cached --check
python -m unittest discover -s tests -v
```

Solo cuando no queden conflictos y las pruebas sean correctas se finaliza el merge mediante `git commit` (con un mensaje que describa la fusión) y después `git push origin main`. Si algo falla, detenerse y revisar antes de publicar.

### Mantener los archivos históricos

En particular, conservar `docs/audt_diagr/ALCANCE_Y_AUDITORIA.md`, el UML final, los diagramas de iteraciones y el material del profesor. Si un documento desapareció del árbol de trabajo, **comprobar primero** su estado e historial con Git antes de restaurar o reemplazar. Nunca sustituir todo `docs/` por una carpeta más pequeña.

---

## 10. Estado comprobado y trabajos pendientes

### Ya implementado en la versión descrita

- Cuatro clases de dominio principales, con los atributos y comportamientos implementados de acuerdo con el UML.
- Relaciones de Empleado con Departamento y Proyecto; multiplicidad N:M representada correctamente.
- Cinco tablas SQL y creación controlada de esquema para SQLite/MySQL.
- DAO para inserción de las entidades principales y consultas de empleados.
- Validación reutilizable de los campos de Empleado.
- Menú de consola con reintentos individuales y búsqueda por ID.
- `UPDATE` de nombre, dirección, teléfono, correo y salario, y `DELETE` confirmado de Empleado.
- CRUD de Departamento, Proyecto y RegistroTiempo, y asignación/cambio de proyecto y de departamento.
- Pruebas automáticas de persistencia, validación y restricciones.
- Documentos y versiones anteriores de los diagramas conservados en `docs/`.

### Pendiente o no comprobado todavía

1. **Fecha de contrato del empleado:** no se puede cambiar por menú, porque el UML no define `cambiarFechaInicioContrato`.
2. **Estado «terminado» de un proyecto:** el UML no lo define (ver «Decisión pendiente» en la sección 4).
3. **Métodos del UML en las clases de dominio:** `crearDepartamento`, `modificarDepartamento`, `buscarDepartamento`, `eliminarDepartamento`, `crearProyecto`, `modificarProyecto` y `eliminarProyecto` siguen sin existir como métodos; su función la cumplen el DAO y los menús.
4. **Otras clases del UML:** `Informe`, `CuentaUsuario` y `ControlAcceso`, con sus comportamientos y validaciones, cuando corresponda al curso.
5. **Prueba real en MySQL/WampServer:** apertura de conexión, creación del esquema, `INSERT`/`SELECT`, relaciones, errores de integridad y operaciones CRUD. No se afirma que esté realizada.
6. **Publicación de la ampliación:** las 44 pruebas originales en Windows y la fusión de Git ya fueron confirmadas por el estudiante; la rama `main` se verificó en el commit `49432e9`. **El CRUD completo y este README todavía requieren ejecutar las 64 pruebas en Windows, copiarse y publicarse** mediante los comandos de la sección 9. Se debe comprobar el resultado final de ese push.

### Criterio para los próximos avances

Cada incorporación debe seguir este recorrido:

1. **Consultar el UML:** identificar clase, atributo, método, tipo y relación correspondiente.
2. **Consultar el material de clase:** elegir una construcción que podamos explicar (`if`, `while`, funciones, objetos, `try/except`, DAO, etc.).
3. **Implementar el cambio mínimo:** modificar el archivo responsable, sin borrar funcionalidades anteriores.
4. **Probar un caso válido y uno inválido:** confirmar el resultado real y las relaciones.
5. **Documentar el aprendizaje:** qué se añadió, qué enseñó la clase y qué decidimos nosotros.
6. **Verificar Git:** proteger `docs/`, `.env`, `.venv` y el historial antes del push.

---

## 11. Guía de estudio para entender el proyecto, no solo ejecutarlo

Orden sugerido para reescribir los archivos por tu cuenta:

1. **`empleado.py`:** escribir primero `class`, `__init__` y `self`; después un validador con `@staticmethod`, `raise ValueError`, `@property` y un setter.
2. **`departamento.py` y `proyecto.py`:** crear objetos y explicar por qué las relaciones son referencias/listas y no cadenas duplicadas.
3. **`registro_tiempo.py`:** explicar por qué se vincula a empleado y proyecto.
4. **`menu_empleado.py`:** practicar indentación de `while True`, `try`, `except`, `return` y las opciones `if/elif`.
5. **`conexion.py` y `empleado_dao.py`:** seguir la secuencia abrir conexión → crear cursor → ejecutar SQL → confirmar → cerrar.
6. **`empleado_proyecto_dao.py` y `registro_tiempo_dao.py`:** dibujar la relación N:M y justificar la tabla puente y la FK compuesta.
7. **`main.py`:** explicar cómo coordina las funciones sin concentrar toda la lógica.

**Preguntas de recuperación activa:**

- ¿Qué diferencia hay entre `nombre` y `self.nombre`?
- ¿Por qué `Empleado.validar_nombre` se pasa a `solicitar()` sin `()`?
- ¿Qué ocurre al escribir `Ana123` o una fecha inexistente?
- ¿Por qué `return` sale de la función mientras `break` sale del ciclo?
- ¿Qué representan `None`, `[]` y `ValueError` en situaciones distintas?
- ¿Por qué `lastrowid` se obtiene después del `INSERT`?
- ¿Por qué una relación N:M necesita `empleado_proyecto`?
- ¿Por qué `RegistroTiempo` no debe guardarse sin esa relación?
- ¿Por qué `finally` y `closing()` ayudan a evitar el bloqueo de SQLite en Windows?
- ¿Qué debo comprobar antes de `git push`?

Para profundizar, consultar también [`docs/GUIA_CLASE_POR_CLASE.md`](docs/GUIA_CLASE_POR_CLASE.md), [`docs/MAPA_UML_Y_PENDIENTES.md`](docs/MAPA_UML_Y_PENDIENTES.md) y [`docs/ESTADO_DE_CLASES.md`](docs/ESTADO_DE_CLASES.md).

---

## 12. Nota de mantenimiento de este README

Este documento **amplía el README original**, conserva sus indicaciones de instalación, SQLite/MySQL, UML, DAO, Git y ejecución, y añade la historia de aprendizaje por clase, el alcance comprobado de la versión de reemplazo y los aprendizajes reales de depuración y sincronización entre dos computadores. **No cambia los scripts ni el diagrama por sí mismo**.

Para evitar errores de documentación, no confundir **«el profesor mostró la técnica»** con **«la implementamos completa para todas las entidades»**. Todo requisito del UML que aún no tenga código debe permanecer registrado como **pendiente**, nunca desaparecer del diseño.

**EcoTech se construye clase por clase: UML fiel, código entendible, evidencia de pruebas y avances conservados.**
