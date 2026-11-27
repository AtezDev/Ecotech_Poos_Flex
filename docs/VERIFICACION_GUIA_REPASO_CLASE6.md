# Verificación contra la Guía de repaso (Objetos, persistencia y autenticación)

Estado histórico de la Clase 6: SQLite/Linux 161/161 pruebas OK (la suite actual tiene 209) con `unittest` y `pytest`; MariaDB 10.11 (como MySQL) con la evidencia de abajo. Pendiente: tu Windows y WampServer.

| Sección de la guía | Qué pide | Dónde se cumple | Prueba |
|---|---|---|---|
| 1–2 Objetos, atributos, métodos | Referencias y estado por objeto | `dominio/empleado.py` | `test_ecotech.py` |
| 3 Validación con `@classmethod` | Reglas en la clase | `Empleado.validar_nombre`, `Usuario.normalizar_usuario`, `Usuario.validar_clave` | `test_01`–`test_04` de `test_clase6.py` |
| 4 `@property` y setter | Validar al asignar | `Empleado`, `Departamento` | `test_ecotech.py`, `test_clase5.py` |
| 5 `None` e ID vs objeto | Comprobar `is None` antes de usar | DAO `buscar_*`, `mostrar_empleado_vinculado` | `test_12`, `test_27` |
| 6 Capas | `input` solo en presentación, reglas en dominio, SQL en DAO | `presentacion/`, `servicios/`, `persistencia/` | `test_15` (el servicio no imprime ni pide datos) |
| 7–8 INSERT, SELECT, `lastrowid` | Persistir y reconstruir | `UsuarioDAO.insertar`, `buscar_por_nombre` | `test_07`, `test_12` |
| 9 Excepciones y reintentos | `try/except`, mensajes claros | `menu_usuario.py` | `test_16`–`test_23` |
| 10 Relación Empleado–Departamento | FK y colección | `EmpleadoDAO`, `DepartamentoDAO` | `test_clase5.py` |
| 11 Herencia y polimorfismo | `ReportePorDepartamento(ReporteEmpleados)` | `dominio/reporte.py` | `test_clase5.py` |
| 12 Semillas idempotentes | Buscar antes de insertar | `persistencia/semillas.py` | `test_24`, `test_25` |
| 13 Usuario asociado a Empleado | `id` de cuenta ≠ `empleado_id`; asociación, no herencia | `usuario.empleado_id` FK UNIQUE; `mostrar_empleado_vinculado` | `test_11`, `test_26`, `test_36` |
| 14 bcrypt | Guardar solo el hash; sal nueva cada vez; `checkpw` | `crear_hash`, `autenticar` | `test_05`, `test_07`, `test_13` |
| 14 Límite de 72 bytes | Rechazar, no recortar; contar bytes UTF-8 | `MAX_BYTES_BCRYPT` | `test_06` |
| 15 Autenticación por capas | `input`/`getpass` en menú, `checkpw` en servicio, `SELECT` en DAO; si la consulta falla, sin acceso | `servicios/autenticacion.py`, `menu_usuario.solicitar_login` | `test_18`, `test_30` |
| 15 Mensaje único | No revelar si falló el usuario o la clave | `autenticar` devuelve `None` en ambos casos | `test_16` |
| Actividad integradora (pasos 1–7) | Empleado → ID → departamento → reiniciar → reporte → cuenta → login bueno y malo | opciones del menú de acceso y principal | `test_32`, `test_33` |
| Evidencia sin secretos | No mostrar claves ni hashes | `getpass`; el menú no imprime el hash | `test_22`, `test_26`, `test_29` |

## Decisiones donde la guía y las diapositivas no coinciden

| Tema | Diapositiva | Guía | Decisión |
|---|---|---|---|
| Largo mínimo de la clave | 6 | 15 | 15 (`Usuario.MIN_CLAVE`); es una constante, se cambia en un lugar. Confírmalo con el profesor. |
| Caracteres del usuario | letras, números y `_` | ejemplo `ana.torres` con punto | Se permite también el punto. |
| Qué devuelve `autenticar` | diccionario | objeto | Un `Usuario` (la guía habla de objetos). |
| Mensajes del servicio | `print` | sin `print` en el servicio | Sin `print`; el menú muestra los mensajes. |

## Pendientes declarados
- Permisos por rol (autorizar): implementados en la Clase 7.
- Crear cuenta sin sesión previa es un arranque de clase; en un sistema real lo haría un administrador.
- `--demo` y `--listar` no pasan por el login.
- Probar en Windows y WampServer. En Git Bash, `getpass` puede fallar; usa `winpty python src/main.py` o la terminal de Windows.

## Evidencia de laboratorio (resultado esperado y observado)

Lo que la guía pide en las actividades 1 y 2: caso, resultado esperado y resultado observado. «Observado» quiere decir que se ejecutó el programa de punta a punta. Cuando dice «pruebas automáticas», el caso lo cubre la suite, no una ejecución manual.

| Caso | Resultado esperado | Observado en SQLite | Observado en MariaDB 10.11 |
|---|---|---|---|
| S1 Semillas, primera carga | 2 departamentos y 3 empleados nuevos | Sí | Sí |
| S2 Semillas repetidas (2 y 3 veces) | Ningún dato nuevo | Sí | Sí |
| S3 Semillas sin `ADMIN_PASSWORD` | Carga los datos, no crea `admin` y lo informa | Sí | Sí |
| S4 Semillas con `ADMIN_PASSWORD` | Crea `admin` ligado a Ana Torres (ID 1) | Sí | Sí |
| S5 Clave de admin de 7 caracteres (`ecotech`) | Rechazada: mínimo 15 | Sí | Sí |
| S6 Login con clave incorrecta | No abre el menú; mensaje público | Sí | Sí |
| S7 Login `admin` correcto | Muestra el empleado vinculado y la opción 8 (Administrar usuarios) | Sí | Sí |
| S8 `--demo` dos veces | Solo la primera carga inserta | Sí | Sí |
| S9 Registrar empleado con correo repetido | Rechazado con mensaje | Sí | Sí |
| S10 Admin elimina la cuenta de otro, con confirmación | Se elimina la cuenta | Sí | Sí |
| S11 Admin intenta eliminar su propia cuenta | Bloqueado | Sí | Sí |
| S12 Falla la consulta de cuentas (tabla borrada) | No entra al menú | Pruebas automáticas (`test_18`, `test_30`) | Pruebas automáticas |
| S13 Departamento con empleados tras reiniciar | Se recupera desde la BD | Pruebas automáticas (`test_clase5.py`) | Pruebas automáticas |

**Commit identificable:** anota aquí el hash del commit con el que subas esta actualización: `________`.
