# Verificación contra la Guía de repaso (Objetos, persistencia y autenticación)

Estado: SQLite/Linux 130/130 pruebas OK; MariaDB 10.11 (como MySQL) con sondeo de `usuario`, registro y login OK. Pendiente: tu Windows y WampServer.

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
- Permisos por rol (autorizar): próxima clase.
- Crear cuenta sin sesión previa es un arranque de clase; en un sistema real lo haría un administrador.
- `--demo` y `--listar` no pasan por el login.
- Probar en Windows y WampServer. En Git Bash, `getpass` puede fallar; usa `winpty python src/main.py` o la terminal de Windows.
