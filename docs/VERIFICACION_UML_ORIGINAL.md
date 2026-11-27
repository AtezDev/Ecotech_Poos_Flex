# Verificación del código frente al UML original (Evaluación 1)

## 1. Diagrama de referencia

- Archivo: `docs/audt_diagr/Diagrama_Final.drawio`
- SHA-256: `28a183c6355907a9ffff3f560c3345c6ceb52c46f766b3f9915ac383ba726c1e`
- Este archivo **se conserva intacto**. No fue rediseñado, actualizado, ampliado ni reemplazado con clases de unidades 2 y 3.
- Páginas: `01 - UML ecotech` (7 clases con atributos y métodos), `02 - Relaciones de Informe y autorizacion`, `03 - Constructores, accesores y validaciones`.

Las clases incorporadas después (`Indicador`, `Clima`, y la tabla `usuario` con rol) se documentan en la sección 4 como extensiones separadas. No se dibujan en el diagrama original.

## 2. Matriz de correspondencia

Leyenda: **Cumple** = existe con el mismo nombre y propósito. **Diferencia** = existe, pero con nombre o diseño distinto (se justifica). **No implementado** = no está en el código como método de dominio.

### 2.1 Empleado

| Elemento del UML | Código (`src/dominio/empleado.py`) | Estado |
|---|---|---|
| `- idEmpleado: Integer` | `id` (propiedad) | Diferencia: nombre `id`, mismo tipo entero |
| `- nombre`, `- direccion`, `- telefono` | `nombre`, `direccion`, `telefono` | Cumple |
| `- correoElectronico` | `correoElectronico` | Cumple |
| `- fechaInicioContrato: Date` | `fechaInicioContrato` (validada con `date.fromisoformat`) | Cumple |
| `- salario: Float` | `salario` (valida positivo y finito) | Cumple |
| `+ registrarEmpleado(...)` | `registrarEmpleado(...)` | Cumple |
| `+ asignarAProyecto(proyecto)` | `asignarAProyecto(proyecto)` | Cumple |
| `+ desasignarDeProyecto(proyecto)` | `desasignarDeProyecto(proyecto)` | Cumple |
| Constructor `Empleado(nombre, direccion, ...)` | `__init__` con los mismos campos más `id=None` | Cumple (campo `id` opcional para la BD) |
| `obtenerIdEmpleado()` | `obtenerIdEmpleado()` | Cumple |
| `obtenerNombre()` / `cambiarNombre()` | Presentes | Cumple |
| `obtenerDireccion()` / `cambiarDireccion()` | Presentes | Cumple |
| `obtenerTelefono()` / `cambiarTelefono()` | Presentes | Cumple |
| `obtenerCorreoElectronico()` / `cambiarCorreoElectronico()` | Presentes | Cumple |
| `obtenerFechaInicioContrato()` | Presente (sin `cambiar`, según UML) | Cumple |
| `obtenerSalario()` / `cambiarSalario()` | Presentes | Cumple |

Extensiones presentes en el código y no en el UML: `validar_*` (validaciones de campo), `departamento` (vínculo con Departamento), `mostrar_datos()`. Se mantienen porque el UML 3 pide validaciones.

### 2.2 Departamento

| Elemento del UML | Código (`src/dominio/departamento.py`) | Estado |
|---|---|---|
| `- nombre: String`, `- gerente: String` | `nombre`, `gerente` | Cumple |
| `+ crearDepartamento(...)` | Creación en `src/persistencia/departamento_dao.py` y `src/servicios` (no como método de instancia) | Diferencia: la creación pasa por el DAO |
| `+ modificarDepartamento(...)` | `cambiarNombre`, `cambiarGerente` | Diferencia: desglosado en dos métodos |
| `+ buscarDepartamento(nombre)` | Búsqueda en el DAO | Diferencia: en persistencia |
| `+ eliminarDepartamento()` | Eliminación en el DAO | Diferencia: en persistencia |
| `+ asignarEmpleado(empleado)` | `asignarEmpleado(empleado)` | Cumple |
| `+ reasignarEmpleado(empleado, nuevoDepartamento)` | `reasignarEmpleado(empleado, nuevoDepartamento)` | Cumple |
| Constructor `Departamento(nombre, gerente)` | `__init__(nombre, gerente=None, id=None)` | Cumple |
| `obtenerNombre()`, `obtenerGerente()` y cambios | Presentes | Cumple |
| `- validarNombre(nombre)` (página 3) | `validarNombre(nombre)` | Cumple |

### 2.3 Proyecto

| Elemento del UML | Código (`src/dominio/proyecto.py`) | Estado |
|---|---|---|
| `- nombre`, `- descripcion`, `- fechaInicio: Date` | Mismos atributos | Cumple |
| `+ crearProyecto(...)` | Constructor y DAO | Diferencia: creación por constructor y persistencia |
| `+ modificarProyecto(...)` | `cambiarNombre`, `cambiarDescripcion`, `cambiarFechaInicio` | Diferencia: desglosado |
| `+ eliminarProyecto()` | Eliminación en persistencia | Diferencia: no es método de instancia |
| Accesores (página 3) | `obtenerNombre`, `obtenerDescripcion`, `obtenerFechaInicio` y cambios | Cumple |

### 2.4 RegistroTiempo

| Elemento del UML | Código (`src/dominio/registro_tiempo.py`) | Estado |
|---|---|---|
| `- fecha: Date`, `- horasTrabajadas: Float`, `- descripcionTarea: String` | Mismos atributos | Cumple |
| `+ registrarTiempo(fecha, horas, descripcion, empleado, proyecto)` | `registrarTiempo(...)` con empleado y proyecto | Cumple |
| `+ obtenerHorasTrabajadas()` | `obtenerHorasTrabajadas()` | Cumple |
| Accesores y cambios (página 3) | Presentes | Cumple |

Pendiente conocido: la FK de registro de tiempo sin asignación previa **no fue probada** en la verificación MySQL.

### 2.5 CuentaUsuario

En el código la clase se llama `Usuario` (`src/dominio/usuario.py`).

| Elemento del UML | Código | Estado |
|---|---|---|
| `- nombreUsuario: String` | `nombre_usuario` | Cumple |
| `- hashContrasena: String` | `password_hash` | Cumple |
| `- sal: String` | No existe como atributo separado | Diferencia: `bcrypt` incluye la sal dentro del hash, así que no hace falta guardarla aparte |
| `- rol: String` | `rol`, validado contra `ROLES = ("admin", "empleado")` | Cumple (con restricción) |
| `+ verificarContrasena(...)` | Verificación en `src/servicios/autenticacion.py` (`autenticar`, `verificar_clave_actual`) | Diferencia: la verificación vive en el servicio |
| `+ obtenerNombreUsuario()`, `+ obtenerRol()` | Atributos y `es_admin` | Diferencia: se leen como atributos |
| `- generarHash`, `- validarRol` (página 3) | `crear_hash` y `validar_rol` | Cumple |

### 2.6 ControlAcceso

No existe una clase `ControlAcceso` en el código. Sus responsabilidades se repartieron así:

| Elemento del UML | Código | Estado |
|---|---|---|
| `- usuarioAutenticado` | Sesión en `main.py` (variable de sesión que se pasa a los menús) | Diferencia |
| `+ autenticarUsuario(nombre, contraseña)` | `autenticar(nombre, clave)` en `autenticacion.py` | Diferencia: función de servicio |
| `+ autorizarAcceso(modulo)` | `exigir_sesion(usuario)` y `exigir_admin(usuario)` en `permisos.py` | Diferencia: dos funciones por rol |
| `+ cerrarSesion()` | Salida del menú de sesión en `main.py` | Diferencia |

Estado: **parcial**. La lógica existe, pero no como clase única. Se declara así en el README.

### 2.7 Informe

No existe una clase `Informe` en el código. Lo más cercano es `src/dominio/reporte.py` (`ReporteEmpleados`, `ReportePorDepartamento`), que cubre el informe de empleados y de departamento.

| Elemento del UML | Código | Estado |
|---|---|---|
| `generarInformeEmpleado(...)` | `ReporteEmpleados` | Diferencia: no recibe `ControlAcceso` como parámetro |
| `generarInformeDeptos(...)` | `ReportePorDepartamento` | Diferencia: mismo caso |
| `generarInformeProyectos(...)` | No implementado | No implementado |
| `generarInformeRegistroTiempo(...)` | No implementado | No implementado |

Estado: **pendiente**. Coincide con el estado declarado en `docs/MAPA_UML_Y_PENDIENTES.md`. El informe no está completo.

## 3. Resumen

- Clases del UML original presentes en el código: Empleado, Departamento, Proyecto, RegistroTiempo, CuentaUsuario (como `Usuario`). Cinco de siete.
- ControlAcceso: parcial, repartida en servicios de autenticación y permisos.
- Informe: parcial. Dos de cuatro métodos tienen equivalente.
- Diferencias de diseño justificadas: creación y eliminación pasan por la capa de persistencia (DAO), para separar dominio y SQL. La sal de la contraseña la gestiona `bcrypt`.

## 4. Extensiones de unidades 2 y 3 (separadas del UML original)

| Clase o artefacto | Archivo | Motivo |
|---|---|---|
| `Indicador` | `src/dominio/indicador.py` | Indicadores económicos de la API (UF, dólar, euro) |
| `Clima` | `src/dominio/clima.py` | Clima de una ciudad desde Open-Meteo |
| Tabla `indicador`, tabla `clima` | `src/persistencia/` | Respaldo local cuando la API falla |
| Columna `usuario.rol` | `src/persistencia/creacion_bd.py` (migración) | Roles `admin` y `empleado` |

Estas extensiones **no modifican** `Diagrama_Final.drawio`.

## 5. Nota sobre la verificación

Esta matriz fue revisada leyendo el código y el diagrama. No es una prueba automatizada. Las pruebas de la suite (`tests/`) cubren la lógica de las clases, no esta correspondencia.
