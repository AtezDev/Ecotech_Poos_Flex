# EcoTech Solutions — Programación Orientada a Objetos

Proyecto de clases de INACAP, basado en `docs/Diagrama_Final.drawio` (tres vistas del mismo UML).

La versión actual implementa las cuatro entidades trabajadas en Python y su persistencia. Conserva el patrón de clases, `main.py`, DAO, SQLite/MySQL, validación de empleados y lectura de datos. El menú, el CRUD completo, los informes y la autenticación corresponden a etapas posteriores.

## 1. Estructura

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
│   ├── Diagrama_Final.drawio
│   └── ALCANCE_Y_AUDITORIA.md
├── .env.example
├── .gitignore
├── requirements.txt
└── Readme.md
```

**Ejecutar `src/main.py`, no los DAO individualmente.** Desde la raíz del repositorio, el comando es `python src/main.py`. Así Python encuentra `dominio` y `persistencia` dentro de `src` y no aparece el error `No module named 'persistencia'`.

## 2. Instalación en Windows con Git Bash

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Crear un archivo `.env` copiando `.env.example`. El archivo `.env` es privado y no debe subirse a GitHub.

```bash
python src/main.py
```

- `venv` y `sqlite3`: módulos incluidos en Python; no se instalan con `pip`.
- `PyMySQL`: permite conectar con MySQL, por ejemplo mediante WampServer.
- `python-dotenv`: lee los valores del archivo `.env`.
- `requirements.txt`: contiene las dos dependencias externas.
- `requeriments.txt`: compatibilidad con la antigua escritura del nombre; utiliza `requirements.txt`.

## 3. Seleccionar el motor de base de datos

### SQLite: primera prueba recomendada

```dotenv
DB_ENGINE=sqlite
DB_NAME=ecotech_practica.db
```

Se crea un archivo `.db` local en la raíz del proyecto. Se activan claves foráneas con `PRAGMA foreign_keys = ON`. Los archivos `.db` no se suben a Git.

### MySQL: WampServer, Workbench o phpMyAdmin

Primero, crear **otra base de datos** en phpMyAdmin o MySQL Workbench:

```sql
CREATE DATABASE ecotech_practica CHARACTER SET utf8mb4;
```

Configurar el archivo `.env` local:

```dotenv
DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecotech_practica
DB_USER=root
DB_PASSWORD=
```

Modificar usuario, puerto y contraseña según tu instalación. WampServer debe tener iniciado MySQL. El código Python no cambia: `conexion.py` selecciona el motor usando `DB_ENGINE`. El mismo `main.py` funciona en ambos entornos, con los distintos marcadores SQL: `?` en SQLite y `%s` con PyMySQL.

**No apuntar inicialmente a la base `ecotech` antigua:** contiene empleados con las columnas `id`, `nombre` y `correo`, mientras el UML exige más campos. `crear_tablas()` detecta ese esquema antiguo, informa qué columnas faltan y se detiene **antes de realizar cambios**. `CREATE TABLE IF NOT EXISTS` no migra tablas antiguas. Respalda la base antigua antes de planificar una migración.

## 4. Clases de dominio (UML)

| Archivo | Responsabilidad |
|---|---|
| `empleado.py` | ID, nombre, dirección, teléfono, correo, fecha de inicio de contrato y salario. Valida nombre/correo; usa `@property`, setters y getters. Mantiene proyectos asociados en memoria. |
| `departamento.py` | Nombre y gerente. Administra una lista de empleados y las operaciones básicas de asignación y reasignación en memoria. |
| `proyecto.py` | Nombre, descripción y fecha de inicio (`datetime.date`); métodos de consulta y cambio. |
| `registro_tiempo.py` | Fecha, horas, descripción de tarea y referencias a Empleado y Proyecto. |

El `id` de las entidades es un identificador generado por la base de datos. En el UML de Empleado aparece como `idEmpleado`; en el código se usa `id` para conservar la sintaxis del laboratorio y `obtenerIdEmpleado()` para consultarlo. `fechaInicioContrato` sí está incorporada y se almacena también en la tabla.

## 5. Persistencia y DAO

| Archivo | Operación actual | Qué realiza |
|---|---|---|
| `conexion.py` | `obtener_motor()`, `abrir_conexion()` | Conecta a SQLite o MySQL según `.env`. |
| `creacion_bd.py` | `crear_tablas()` | Crea cinco tablas con claves primarias y foráneas. |
| `empleado_dao.py` | `insertar()`, `listar()`, `buscar_por_id()` | Inserta al empleado y recupera registros como objetos; `listar()` usa `fetchall()`, la búsqueda usa `fetchone()`. |
| `departamento_dao.py` | `insertar()` | Guarda departamento y asigna su ID. |
| `proyecto_dao.py` | `insertar()` | Guarda proyecto y fecha de inicio. |
| `empleado_proyecto_dao.py` | `asignar()` | Guarda la relación N:M; no repite una misma pareja. |
| `registro_tiempo_dao.py` | `insertar()` | Guarda horas solo si el empleado está asignado al proyecto. |

Patrón aprendido: `abrir_conexion()`, `cursor()`, `execute()` con parámetros, `cursor.lastrowid`, `commit()` y `close()`. Los valores se pasan por separado a `execute()`.

### Multiplicidad muchos a muchos

El UML permite que un empleado participe en varios proyectos y que un proyecto tenga varios empleados. Se representa con:

```text
empleado (1) ── (N) empleado_proyecto (N) ── (1) proyecto
```

`empleado_proyecto` tiene `empleado_id`, `proyecto_id` y clave primaria compuesta. `RegistroTiempo` se vincula a una asignación existente mediante una clave foránea compuesta. Esta tabla puente es una adaptación mínima necesaria para persistir la relación del UML; no es una octava clase de dominio.

## 6. Qué demuestra main.py

`python src/main.py`:

1. Prepara el esquema según el motor.
2. Crea y guarda un Departamento y un Proyecto.
3. Crea y guarda un Empleado con todos sus atributos y muestra el ID antes (`None`) y después.
4. Guarda su asignación al Proyecto en la tabla puente.
5. Registra horas asociadas al mismo empleado y proyecto.
6. Recupera el listado de empleados con `EmpleadoDAO.listar()`.
7. Prueba un ID existente y uno inexistente mediante `buscar_por_id()`.
8. Demuestra dos rechazos de datos con el `try/except ValueError` enseñado en la clase de validación.

**Cada ejecución de `main.py` agrega nuevos registros de demostración.** Para ver registros anteriores sin agregar otros, consulta la base con phpMyAdmin/Workbench o SQLite. En las pruebas de clase se puede verificar también reiniciando Python y volviendo a ejecutar una consulta DAO.

## 7. Git Bash: subir los avances

Desde la carpeta raíz del repositorio:

```bash
git status
git add .
git status
git commit -m "Avance EcoTech: validaciones, consultas y relaciones UML"
git push
```

`git push` utiliza el remoto/rama de seguimiento configurado. `origin` es el nombre habitual del remoto y `main` es el nombre de una rama; no son rutas de carpetas.

Verificar que el archivo privado está excluido:

```bash
git check-ignore -v .env
git ls-files .env
```

El segundo comando no debería mostrar el archivo. Si `.env` ya fue rastreado anteriormente, debes retirarlo del índice y reemplazar las credenciales que pudieron quedar expuestas.

## 8. Próximos contenidos

Quedan pendientes el menú, actualizar/eliminar, manejo general de errores de BD y la implementación funcional de `Informe`, `CuentaUsuario` y `ControlAcceso`. Estas tres clases están modeladas en el UML final, pero todavía no se presentan como implementadas. La clase actual sí incluye `try/except ValueError` en la consola para mostrar un error de validación.

Consulta `docs/ALCANCE_Y_AUDITORIA.md` para la correspondencia entre los materiales del profesor y las decisiones de implementación.
