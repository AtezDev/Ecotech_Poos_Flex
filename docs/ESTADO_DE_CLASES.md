# Estado real EcoTech — versión remodelada para estudiar

- **Guía de diseño:** `audt_diagr/Diagrama_Final.drawio` con 3 vistas (7 clases).
- **U2 Clase 1:** objetos, `__init__`, `self`, `main`.
- **U2 Clase 2:** relaciones, multiplicidades, colecciones y encapsulamiento.
- **U2 SQL/DAO:** SQLite/MySQL, 5 tablas, `INSERT`, ID autogenerado, SQL parametrizado.
- **FLEX Clase 3:** `@property`, setters, nombre/correo, lista y búsqueda por ID.
- **FLEX Clase 4:** menú, `while True`, reintentos por campo, `try/except`, UPDATE de correo y DELETE confirmado.
- **CRUD completo (17-nov-2026):** actualizar nombre, dirección, teléfono, correo y salario del empleado; CRUD de Departamento, Proyecto y RegistroTiempo; asignar/quitar empleado de proyecto y de departamento; menú principal con todas las entidades (`python src/main.py`).
- **FLEX Clase 5 (17-nov-2026):** referencia y colección Empleado–Departamento, FK guardada y recuperada (`actualizar_departamento`, `buscar_con_empleados`), reportes con herencia y polimorfismo, gerente como FK a empleado (opcional) y departamento visible al listar empleados. Semillas sin duplicados (`persistencia/semillas.py`) y propiedad `departamento` validada (Paso 5). **Pendiente:** explicar y probar en Windows/MySQL; próxima clase Usuario e inicio de sesión.
- **FLEX Clase 6 (19-nov-2026):** `Usuario` asociado a `Empleado`, tabla `usuario`, hash bcrypt, `servicios/autenticacion.py`, menú de acceso con 3 intentos y login antes del menú principal. 130/130 pruebas en SQLite y sondeo en MariaDB. **Pendiente:** Windows/WampServer y permisos por rol (próxima clase). Ver `VERIFICACION_GUIA_REPASO_CLASE6.md`.
- **Conservado:** relación Empleado–Proyecto N:M, tabla puente y FK compuesta de RegistroTiempo.
- **Pendiente:** los comportamientos avanzados del UML y las clases Informe, CuentaUsuario y ControlAcceso, y métodos del UML como `crearDepartamento` o `eliminarProyecto`, que hoy cubren el DAO y el menú.
- **Pruebas:** SQLite temporal; ejecutar también en Windows y posteriormente en MySQL/WampServer.
- **Sin cambios en GitHub:** este paquete es una carpeta de estudio independiente.

- **Verificación de la carpeta v5 (19-nov-2026):** 94/94 pruebas ejecutadas en SQLite/Linux, individualmente y en conjunto. Windows y MySQL/WampServer quedan por validar. La PPT/PDF oficial de Clase 5 no está incluida en los materiales recibidos; la guía PDF añadida es una guía complementaria, no material oficial del profesor.
