# EcoTech Solutions — Poos Remodelado (guía de aprendizaje)

**Objetivo:** conservar el UML final como contrato de clases, atributos, operaciones y multiplicidades, pero escribir el código con la forma sencilla utilizada por el profesor en las clases de POO. La remodelación es de **estilo y explicación**, no del modelo.

## Antes de empezar

- `docs/audt_diagr/Diagrama_Final.drawio`: UML FINAL, tres vistas. **No reemplazar**.
- `docs/GUIA_CLASE_POR_CLASE.md`: repaso gradual, con ejercicios para escribir el código tú mismo.
- `docs/MAPA_UML_Y_PENDIENTES.md`: qué está implementado y qué falta según el diagrama.
- `docs/material_profesor/`: PDFs de las clases usados para adaptar el estilo.
- `src/dominio/`: Empleado, Departamento, Proyecto y RegistroTiempo.
- `src/persistencia/`: conexión, creación de cinco tablas y DAOs.
- `src/presentacion/`: menú de empleados y las validaciones de entrada.
- `tests/`: pruebas automáticas con base temporal de SQLite.

## Preparar en Windows (Git Bash)

Desde la carpeta **Ecotech_Poos_Remodelado**:

```bash
py -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

No publiques `.env`: podría contener credenciales de MySQL. Usa SQLite primero:

```dotenv
DB_ENGINE=sqlite
DB_NAME=ecotech_practica.db
```

**No uses la base antigua `ecotech`**: tiene una tabla Empleado de tres columnas incompatible con el UML actual.

## Ejecutar y comprobar

```bash
python -m compileall -q src
python -m unittest discover -s tests -v
python src/main.py
```

El menú tiene registrar, listar, buscar por ID, cambiar correo y eliminar con confirmación. Para ver las asociaciones previas, puedes ejecutar **solo en una base de prueba**, porque inserta filas:

```bash
python src/main.py --demo
```

Para leer sin agregar datos:

```bash
python src/main.py --listar
```

## Tres responsabilidades, como en la Clase 4

1. **Dominio:** `Empleado` comprueba reglas y mantiene atributos.
2. **Presentación:** `menu_empleado.py` solicita datos, repite los incorrectos y explica fallos.
3. **Persistencia:** `EmpleadoDAO` utiliza SQL, `commit()` y `finally` para cerrar conexiones.

`solicitar("Nombre", Empleado.validar_nombre)` pasa un método estático a una función. No es una librería extra ni un patrón avanzado.

## Cómo se conservó la multiplicidad N:M

`Empleado.asignarAProyecto(proyecto)` conserva la referencia en memoria. `EmpleadoProyectoDAO.asignar(empleado, proyecto)` guarda la pareja en la tabla `empleado_proyecto`, con dos FOREIGN KEY y clave primaria compuesta. `RegistroTiempo` solo se puede guardar para una pareja que ya existe. No se eliminaron ni se reemplazaron estas reglas.

## Importante acerca del UML completo

El UML tiene **siete clases**. Hasta el alcance revisado de FLEX Clase 4 están en funcionamiento las cuatro principales y sus DAOs asociados. **Informe, CuentaUsuario y ControlAcceso, y operaciones futuras de Departamento/Proyecto, no están implementados todavía**. Están enumerados, no omitidos, en `docs/MAPA_UML_Y_PENDIENTES.md`.

Este ZIP **no reemplaza tu repositorio GitHub ni su historial**. Si decides integrar cambios, copia los scripts a la misma ruta y conserva el `.git`, tus documentos históricos y `.env`. No hagas `git push` sin probar primero en tu equipo.

## Material revisado

Se cotejaron las cinco entregas de Unidad 2 / FLEX (UML→Python, relaciones/encapsulamiento, SQLite/MySQL+INSERT/ID, empleado válido+lectura y menú+excepciones) más las tres primeras clases de Unidad 1. No se inventaron funciones de autenticación que el profesor aún no ha explicado.
