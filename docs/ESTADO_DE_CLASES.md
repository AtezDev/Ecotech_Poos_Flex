# Estado real EcoTech — versión remodelada para estudiar

- **Guía de diseño:** `audt_diagr/Diagrama_Final.drawio` con 3 vistas (7 clases).
- **U2 Clase 1:** objetos, `__init__`, `self`, `main`.
- **U2 Clase 2:** relaciones, multiplicidades, colecciones y encapsulamiento.
- **U2 SQL/DAO:** SQLite/MySQL, 5 tablas, `INSERT`, ID autogenerado, SQL parametrizado.
- **FLEX Clase 3:** `@property`, setters, nombre/correo, lista y búsqueda por ID.
- **FLEX Clase 4:** menú, `while True`, reintentos por campo, `try/except`, UPDATE de correo y DELETE confirmado.
- **CRUD completo (17-nov-2026):** actualizar nombre, dirección, teléfono, correo y salario del empleado; CRUD de Departamento, Proyecto y RegistroTiempo; asignar/quitar empleado de proyecto y de departamento; menú principal con todas las entidades (`python src/main.py`).
- **Conservado:** relación Empleado–Proyecto N:M, tabla puente y FK compuesta de RegistroTiempo.
- **Pendiente:** los comportamientos avanzados del UML y las clases Informe, CuentaUsuario y ControlAcceso, y métodos del UML como `crearDepartamento` o `eliminarProyecto`, que hoy cubren el DAO y el menú.
- **Pruebas:** SQLite temporal; ejecutar también en Windows y posteriormente en MySQL/WampServer.
- **Sin cambios en GitHub:** este paquete es una carpeta de estudio independiente.
