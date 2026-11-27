# Verificación de criterios de la Evaluación 2 (Unidades 2 y 3)

Cada criterio se relaciona con el archivo donde se implementa y con la prueba que lo verifica.
Las pruebas se ejecutan con `python -m unittest discover -s tests -p "test_*.py"` (218 pruebas).

| Criterio | Implementación | Prueba o verificación | Estado |
|---|---|---|---|
| 2.1.1 Clases y métodos según UML | `src/dominio/*.py`, `Readme.md` (sección 5), `docs/MAPA_UML_Y_PENDIENTES.md` | `test_ecotech.py`, `test_crud.py` | Cumplido, con pendientes UML declarados (Informe, ControlAcceso como clase) |
| 2.1.2 Principios POO | Encapsulamiento en `Usuario`, `Indicador`, `Clima`; herencia de reportes en `dominio/reporte.py` | `test_ecotech.py`, `test_unidad3.py` | Cumplido |
| 2.1.3 Librería oficial de BD | `sqlite3` y `PyMySQL` en `persistencia/conexion.py` | `test_clase5.py`, `test_clase6.py` | Cumplido en SQLite; MySQL probado solo en MariaDB 10.11 del entorno de desarrollo |
| 2.1.4 Manejo de errores | `tipos_errores_bd()`, `try/except` en menús y servicios | `test_idempotencia.py`, `test_unidad3.py` | Cumplido |
| 2.1.5 Revisión de código de IA | `docs/USO_DE_IA_Y_DECISIONES.md` | Revisión manual | Cumplido; cada integrante debe revisar su parte |
| 3.1.1 Consumo de APIs con librerías oficiales | `servicios/api_indicadores.py` (UF, dólar, euro), `servicios/api_clima.py` (clima), con `requests` | `test_unidad3.py`, `test_clima.py` (JSON ficticio) y prueba real en el computador del estudiante | Cumplido; la prueba real la hizo el estudiante |
| 3.1.2 Autenticación y validación de entradas | `servicios/autenticacion.py` (bcrypt), `servicios/permisos.py`, validación de ciudad y coordenadas en `dominio/clima.py` y `servicios/clima.py` | `test_clase6.py`, `test_cuentas_crud.py`, `test_clima.py` | Cumplido |
| 3.1.3 Manejo de errores externos | `validar_respuesta_http()` (200, 404, 500 y otros), respaldo local en `servicios/indicadores.py` y `servicios/clima.py` | `test_unidad3.py` (`test_11b_codigos_http_se_validan`), `test_clima.py` | Cumplido. El menú no muestra el código HTTP al usuario; solo informa el respaldo |
| 3.1.4 Ajuste de seguridad con IA | `docs/USO_DE_IA_Y_DECISIONES.md` | Revisión manual | Cumplido; cada integrante debe completar su defensa |

## Pendientes que no se pueden verificar desde el entorno de desarrollo
- Prueba real de la API en el computador del estudiante: realizada por el estudiante (UF, dólar, euro y clima respondieron con `Origen: API`).
- Prueba completa con MySQL/WampServer en el computador del estudiante: no realizada.
- Confirmar con el profesor la modalidad de trabajo (la guía indica grupo de 2 a 3 estudiantes).
