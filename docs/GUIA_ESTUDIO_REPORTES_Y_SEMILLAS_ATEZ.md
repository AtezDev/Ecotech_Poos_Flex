# Guía de estudio ATEZ — Reportes, herencia, polimorfismo y semillas

> Esta guía explica la implementación que viene en esta carpeta. El PDF `GUIA_CLASE5_MEJORAS_ECOTECH.pdf` es la guía complementaria que compartiste, no una diapositiva oficial del profesor. En el ZIP de materiales solo aparecen las clases 1 a 4; falta el archivo oficial de Clase 5 para contrastar cada laboratorio literalmente.

## 1. Dónde están las clases de reporte

Archivo: `src/dominio/reporte.py`. En esta versión hay **dos clases dentro del mismo archivo**:

- `ReporteEmpleados`: clase base del ejercicio; recibe una colección de empleados y sabe construir el formato común.
- `ReportePorDepartamento(ReporteEmpleados)`: clase derivada; recibe un departamento y reutiliza el comportamiento de la clase base.

No existe una clase llamada `Reporte` en el código. `reporte.py` es el nombre del archivo, no el nombre de una clase. La guía PDF es algo ambigua en la página 14 al titular “La clase nueva es Reporte”, pero las páginas 15 y 16 muestran el código concreto con `ReporteEmpleados` como clase base y `ReportePorDepartamento` como subclase. Esta carpeta sigue ese código concreto.

## 2. ¿Qué es herencia en este ejemplo?

Herencia significa que una clase nueva puede reutilizar atributos y métodos de otra clase. La clase que entrega el comportamiento común es la clase base; la que hereda es la clase derivada o subclase.

```python
class ReportePorDepartamento(ReporteEmpleados):
    def __init__(self, departamento):
        super().__init__(departamento.empleados)
        self.departamento = departamento

    def generar(self):
        titulo = f"Departamento: {self.departamento.nombre}"
        return self._formatear(self.empleados, titulo)
```

- Los paréntesis `(ReporteEmpleados)` indican de quién hereda.
- `super().__init__(...)` ejecuta el constructor de la clase base y prepara `self.empleados`.
- `self.departamento` conserva el departamento concreto del reporte.
- `generar()` se redefine para cambiar el título y producir el reporte de ese departamento.

## 3. ¿Y si creamos una clase llamada `Reporte`?

Sí, **es una alternativa válida de diseño**, especialmente si más adelante habrá reportes de empleados, departamentos, proyectos y registros de tiempo. En ese diseño se podría tener una clase general `Reporte` y varias clases derivadas. Sin embargo, eso no es lo que implementa el código de esta versión ni lo que explica el ejemplo concreto de las páginas 15–16 del PDF. No agregué esa tercera clase para no cambiar el ejercicio ni inventar una jerarquía distinta sin ver la PPT oficial.

Por ahora, aprende y defiende el diseño que está en el proyecto: `ReporteEmpleados` es la base y `ReportePorDepartamento` hereda de ella. Si la PPT oficial pide explícitamente una clase abstracta o base llamada `Reporte`, entonces adaptaremos el diseño con esa fuente en la mano.

## 4. ¿Qué es polimorfismo aquí?

Polimorfismo significa que objetos de clases distintas pueden responder a una misma operación, cada uno con su propio comportamiento. En `imprimir_reportes()` se construye una lista con ambos tipos y se llama a `generar()` sin preguntar qué tipo de objeto es cada uno:

```python
reportes = [
    ReporteEmpleados(empleados),
    ReportePorDepartamento(departamento),
]
for reporte in reportes:
    print(reporte.generar())
```

La llamada es la misma (`generar()`), pero el contenido cambia según el objeto: el primero genera el reporte general y el segundo genera el reporte del departamento.

## 5. ¿Por qué no va el SQL dentro de las clases de reporte?

El reporte recibe objetos que ya fueron recuperados por los DAO. Su responsabilidad es dar formato y devolver texto. La presentación decide cuándo imprimirlo y la persistencia se encarga de consultar la base de datos. Así se mantiene el orden de EcoTech: dominio, persistencia y presentación.

## 6. Semillas: qué son y para qué sirven

Una semilla (*seed*) es un conjunto de datos ficticios preparado para poblar una base de práctica. Sirve para probar listados, relaciones y reportes sin tener que registrar manualmente cada dato.

En EcoTech están en `src/persistencia/semillas.py` y se ejecutan desde la opción 6 del menú principal. Incluyen:

- 2 departamentos: Soporte y Desarrollo.
- 3 empleados: Ana Torres, Luis Soto y María Pérez.
- Ana y María quedan como gerentes de sus departamentos.

Los correos se usan como identificador para comprobar si un empleado de ejemplo ya existe; el nombre identifica al departamento.

## 7. Cómo evita duplicados la semilla

La regla es **consultar antes de insertar**:

1. Ejecuta un `SELECT` para buscar el correo o el nombre.
2. Si `fetchone()` devuelve `None`, el dato no está y se puede insertar.
3. Si devuelve una fila con un ID, el dato ya existe y no se vuelve a insertar.

No es magia ni una función especial de Python: es una decisión de programación usando SQL y un `if`. La protección actual está en el código de la semilla; las tablas no tienen una restricción `UNIQUE` para correo o nombre.

## 8. ¿Por qué ese orden de inserción?

La relación tiene dos llaves foráneas:

- `empleado.departamento_id` referencia `departamento.id`.
- `departamento.gerente_id` referencia `empleado.id`.

Para evitar intentar guardar un ID que todavía no existe, el proceso sigue este orden:

1. Crear primero los empleados de ejemplo sin departamento.
2. Crear después los departamentos, asignando como gerente un empleado que ya tiene ID.
3. Finalmente, asignar cada empleado a su departamento y guardar la relación con `EmpleadoDAO.actualizar_departamento()`.

Esto también responde a la decisión del profesor: el gerente puede ser cualquier empleado, no tiene que pertenecer al departamento que dirige, y el campo `gerente_id` puede ser `NULL`.

## 9. Laboratorio: comprobar que no duplica

Usa una base de práctica nueva, por ejemplo `ecotech_practica`. No borres ni reutilices la base `ecotech` si contiene información que quieras conservar.

1. Ejecuta `python src/main.py`.
2. Elige la opción 6. La primera vez debe indicar que agregó 2 departamentos y 3 empleados nuevos.
3. Elige la opción 6 otra vez. Debe informar que las semillas ya estaban cargadas y que no duplicó datos.
4. Entra al menú de empleados y lista los empleados.
5. Usa la opción 11 para mostrar los departamentos con sus empleados.
6. Comprueba que Ana y María aparecen como gerentes y que los empleados pertenecen a los departamentos esperados.

Una prueba adicional importante: cambia a Luis de departamento y vuelve a ejecutar las semillas. El código está diseñado para no volver a asignarlo automáticamente si ya existía antes de esa ejecución; así no pisa cambios posteriores.

## 10. Pruebas automatizadas incluidas

La carpeta contiene 94 pruebas: 44 originales, 20 del CRUD y 30 de Clase 5. En esta revisión se ejecutaron por separado y también en conjunto en SQLite/Linux: **94/94 OK**. Eso no reemplaza la ejecución en tu Windows ni la comprobación contra MySQL/WampServer.

En PowerShell, desde la carpeta raíz del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
python -m compileall -q src
python -m unittest discover -s tests -v
```

## 11. Qué no se agregó

- No se creó una clase `RegistroEmpleado`: no aparece como requisito de la guía de Clase 5 que compartiste. El registro de empleados sigue en el menú y DAO existentes.
- No se creó una clase adicional `Reporte`: la versión actual sigue el ejemplo concreto `ReporteEmpleados` → `ReportePorDepartamento`.
- No se agregó `ON DELETE CASCADE`.
- No se cambió el UML ni se agregaron atributos de proyecto no definidos.

## 12. Preguntas para practicar la defensa

1. ¿Qué diferencia hay entre herencia y asociación?
2. ¿Qué reutiliza `ReportePorDepartamento` mediante `super()`?
3. ¿Por qué ambos reportes pueden responder a `generar()`?
4. ¿Qué devuelve `fetchone()` cuando no encuentra un registro?
5. ¿Por qué se consulta antes de insertar una semilla?
6. ¿Por qué se crean primero los empleados y después los departamentos?
7. ¿Qué dos llaves foráneas forman el ciclo Empleado–Departamento?
8. ¿Por qué repetir la carga de semillas no debe duplicar registros?

**Feynman:** explica en voz alta, en menos de un minuto, por qué una misma llamada `generar()` puede producir dos reportes distintos y por qué la semilla busca antes de insertar.
