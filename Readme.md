# EcoTech Solutions — Programación Orientada a Objetos

Proyecto de clases de **Analista Programador (INACAP)**. Se utiliza como referencia el UML final de tres vistas ubicado en `docs/audt_diagr/Diagrama_Final.drawio`.

Esta carpeta reúne los avances trabajados en clases: objetos, relaciones, atributos, encapsulamiento, validación de nombre/correo, conexión a SQLite/MySQL, `INSERT`, ID autoincremental y consultas `SELECT`. No incluye aún un menú completo, operaciones `UPDATE`/`DELETE`, informes ni autenticación.

## 1. Archivos del proyecto

```text
Ecotech_Poos_Flex/
├── src/
│   ├── main.py
│   ├── dominio/
│   │   ├── empleado.py
│   │   ├── departamento.py
│   │   ├── proyecto.py
│   │   └── registro_tiempo.py
│   └── persistencia/
│       ├── conexion.py
│       ├── creacion_bd.py
│       ├── empleado_dao.py
│       ├── departamento_dao.py
│       ├── proyecto_dao.py
│       ├── registro_tiempo_dao.py
│       └── empleado_proyecto_dao.py
├── docs/
│   └── audt_diagr/
│       └── Diagrama_Final.drawio
├── tests/
│   └── test_ecotech.py
├── .env.example
├── .gitignore
├── requirements.txt
└── Readme.md
```

Los documentos, capturas y versiones históricas que ya estén en `docs/` deben conservarse. `tests/` contiene verificaciones complementarias, no es una clase de dominio ni un nuevo requisito de la asignatura.

## 2. Preparación en Windows con Git Bash

Desde la carpeta del repositorio:

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

El archivo `requirements.txt` es el **único listado de dependencias externas**:

- `PyMySQL`: conexión con MySQL, por ejemplo usando WampServer.
- `python-dotenv`: lectura de variables del archivo `.env`.

`sqlite3`, `datetime`, `venv`, `unittest` y `pathlib` forman parte de Python; no necesitan `pip install` por separado.

Crea tu configuración local copiando `.env.example` a `.env` (sin compartir contraseñas). En Git Bash:

```bash
cp .env.example .env
```

El archivo `.env` debe quedar fuera de Git. Si ya tienes uno local con tus credenciales, consérvalo y revisa su motor antes de ejecutar.

## 3. Elegir SQLite o MySQL

**SQLite**, recomendado para la primera ejecución:

```dotenv
DB_ENGINE=sqlite
DB_NAME=ecotech_practica.db
```

El programa crea un archivo SQLite en la raíz y activa `PRAGMA foreign_keys = ON` en cada conexión.

**MySQL** (WampServer, MySQL Workbench o phpMyAdmin): crea una **base de prueba nueva** en MySQL:

```sql
CREATE DATABASE ecotech_practica CHARACTER SET utf8mb4;
```

Configura `.env` (adaptando usuario, contraseña y puerto según tu equipo):

```dotenv
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech_practica
DB_USER=root
DB_PASSWORD=
```

La conexión utiliza `sqlite3` o PyMySQL según `DB_ENGINE`. Los DAO emplean `?` con SQLite y `%s` con PyMySQL. Las tablas MySQL utilizan `InnoDB` para las claves foráneas.

**No utilices directamente la base histórica `ecotech`**: contiene la primera tabla de empleados con solo `id`, `nombre` y `correo`. El nuevo modelo necesita más columnas. `crear_tablas()` revisa columnas esenciales de las tablas existentes y rechaza esquemas incompatibles, pero no realiza migraciones ni comprueba todos los índices de una base antigua.

## 4. Clases y UML

| Archivo | Qué representa |
|---|---|
| `empleado.py` | ID, nombre, dirección, teléfono, correo, fecha de inicio de contrato y salario; nombre y correo se validan con propiedades (`@property` y setter). |
| `departamento.py` | Nombre, gerente y colección de empleados. Asignación/reasignación básica de objetos. |
| `proyecto.py` | Nombre, descripción y fecha de inicio (`date`). |
| `registro_tiempo.py` | Fecha, horas, descripción de tarea y referencias a empleado y proyecto. |

El atributo `id` de Empleado corresponde al `idEmpleado` del UML: se inicializa sin ID (`None`), y el DAO asigna el ID generado por la base. `obtenerIdEmpleado()` permite consultarlo. La validación de nombre y correo usa `strip()`, longitudes y `ValueError` tal como indica el material de lectura de datos. Salario no negativo, horas positivas y fechas de tipo `date` son reglas de implementación que deben justificarse con el UML y confirmarse si el docente define límites distintos.

Las siete clases del UML incluyen además `Informe`, `CuentaUsuario` y `ControlAcceso`, todavía **no implementadas** en esta etapa. Algunos métodos completos de gestión (crear/modificar/eliminar) aparecen en UML pero permanecen para clases posteriores. Cambiar un atributo Python no modifica automáticamente su fila en SQL.

## 5. Persistencia y DAO

| Archivo | Operaciones disponibles |
|---|---|
| `conexion.py` | `obtener_motor()`, `abrir_conexion()` |
| `creacion_bd.py` | `crear_tablas()` |
| `empleado_dao.py` | `insertar()`, `listar()`, `buscar_por_id()` |
| `departamento_dao.py` | `insertar()` |
| `proyecto_dao.py` | `insertar()` |
| `empleado_proyecto_dao.py` | `asignar()`, `listar_por_empleado()`, `listar_por_proyecto()` |
| `registro_tiempo_dao.py` | `insertar()` |

`INSERT` guarda filas; `SELECT` recupera datos. `cursor.execute(sql, parametros)` separa la instrucción SQL de sus valores. `cursor.lastrowid` obtiene el ID generado por una inserción, `commit()` confirma la transacción y `close()` cierra la conexión. `fetchall()` obtiene todas las filas de una consulta; `fetchone()` una sola (o `None` si no hay resultado). `listar()` devuelve una lista de objetos `Empleado` o `[]` si está vacía.

### Relación entre Empleado y Proyecto

El UML indica multiplicidad N:M: un empleado participa en varios proyectos y un proyecto tiene varios empleados. La tabla `empleado_proyecto` guarda cada par `(empleado_id, proyecto_id)` con clave primaria compuesta y claves foráneas. La tabla puente no elimina la multiplicidad: **la representa en SQL**. `EmpleadoProyectoDAO.asignar()` registra esa relación y evita duplicados; las consultas permiten verificar ambos sentidos. `RegistroTiempo` se guarda solo para una pareja previamente registrada en esa tabla, reforzada con una FK compuesta.

## 6. Cómo ejecutar

El programa principal es `src/main.py`, **no los archivos DAO de forma individual**. Desde la raíz del repositorio:

```bash
python src/main.py
```

El modo normal crea las tablas y ejecuta una demostración completa con un departamento, un proyecto, un empleado, su participación y un registro de tiempo. **Cada ejecución normal agrega nuevos registros de demostración**.

Para consultar empleados sin añadir registros nuevos:

```bash
python src/main.py --listar
```

Para revisar sintaxis y ejecutar pruebas SQLite temporales (opcionales):

```bash
python -m compileall -q src
python -m unittest discover -s tests -v
```

Estas pruebas no dependen de WampServer y no sustituyen la ejecución real con MySQL en tu computador. Cuando el docente indique el avance correspondiente, añadiremos las funciones de actualización, eliminación, menú y manejo general de errores de conexión.

## 7. Git Bash y GitHub

```bash
git status
git add .
git status
git commit -m "Avance EcoTech POO - clases y persistencia"
git push
```

`git push` utiliza la rama de seguimiento configurada. `origin` es el nombre convencional del repositorio remoto, no una carpeta local.

Verifica los archivos privados antes de subir:

```bash
git check-ignore -v .env
git ls-files .env
git diff --cached --stat
```

`git ls-files .env` debe devolver vacío; nunca subas contraseñas. Conserva los archivos anteriores en `docs/` y tu historial de `.git`.

## 8. Estado del avance

Implementados y comprobados en SQLite: clases principales, validaciones de nombre/correo, `INSERT`, `listar()`, `buscar_por_id()`, claves foráneas, relación N:M y registro de tiempo con asignación.

Pendientes de probar en **MySQL/WampServer**: conexión real, permisos, creación de cinco tablas, integridad referencial y consultas desde tu computadora. El programa no debe presentarse como probado en MySQL hasta ejecutar esas pruebas.
