# Uso de herramientas de IA y decisiones técnicas

Este documento registra el proceso de trabajo con el asistente de IA (Claude) en la Unidad 3 (clima, indicadores y roles).
Quien toma las decisiones es el estudiante: cada cambio se propuso, se probó en su computador y se aceptó o se descartó.
Las pruebas de la API real se hicieron en el computador del estudiante, porque el entorno del asistente no tenía acceso a la API.

## 1. Cómo se trabajó
- El asistente revisó el material de clase (diapositivas de Clase 6 y Clase 7, y la guía de estudio) y propuso la estructura de cambios.
- El asistente escribió los cambios y las pruebas en su entorno y entregó carpetas actualizadas.
- El estudiante copió los cambios, ejecutó las pruebas y el programa en su computador, y reportó resultados.
- El estudiante hizo los commits y los `push` a GitHub.
- Cuando algo no funcionó, el asistente propuso una corrección y el estudiante decidió si se aplicaba.

## 2. Registro de decisiones

| Fecha | Propuesta del asistente | Decisión del estudiante | Resultado |
|---|---|---|---|
| 24-nov | Agregar rol (`admin`/`empleado`) a `Usuario` y reemplazar la validación por nombre | Aceptada (la pidió con la guía de Clase 7) | Migración de la tabla `usuario`; pruebas OK |
| 24-nov | Consumo de la API de indicadores con `requests`, `timeout=(3, 5)` y `raise_for_status()` | Aceptada | Pruebas con JSON ficticio OK |
| 24-nov | Tabla `indicador` con clave `(codigo, fecha)` para no duplicar datos | Aceptada | Prueba de guardar dos veces: una sola fila |
| 24-nov | Respaldo local cuando la API falla | Aceptada | Pruebas con fallas simuladas OK |
| 25-nov | Menú del empleado con solo ficha, indicadores y cuenta | Propuesta. **Pendiente de confirmar por el estudiante** | Implementada tal como se propuso |
| 26-nov | Módulo de clima con Open-Meteo (sin clave) | Aceptada | Funciona en el computador del estudiante |
| 26-nov | Adaptador de la API ajustado al formato real (`data.uf`, `data.dolar`, `data.euro`) | Aceptada tras la prueba real del estudiante | UF, dólar y euro guardados y consultados |
| 26-nov | Agregar dólar y euro (tipo de cambio) | Aceptada | Pruebas OK y consulta real OK |

## 3. Código revisado y cambiado tras la revisión
- **Adaptador de la API.** El primer diseño seguía el ejemplo de la diapositiva (`codigo` y `serie`). La respuesta real tiene otra forma (`status` y `data`). El fallo se detectó en la prueba real del estudiante y se corrigió. Criterio: la prueba con el servicio real vale más que el ejemplo de la diapositiva.
- **Clave del administrador.** Se leen desde `.env` (`ADMIN_PASSWORD`) y no se escriben en el código. Criterio: seguridad y no exponer credenciales.
- **Contraseñas.** Se guardan con bcrypt. Criterio: no guardar contraseñas en texto plano.
- **Mensajes de error.** No muestran trazas técnicas ni rutas. Criterio: no exponer información sensible al usuario.

## 4. Pendientes que el estudiante debe revisar
- Confirmar la restricción del menú del empleado (fila de la tabla).
- Confirmar que la modalidad de trabajo es individual (ver `docs/INSTRUCCIONES_ENTREGA.md`).
- Ejecutar las pruebas en el computador antes de subir la entrega.

## 5. Revisión de validación de entradas (26-nov, última sesión)

Pedido del estudiante: que todas las entradas del programa se validen y que ningún dato vacío, con caracteres no válidos o fuera de rango haga caer el programa o avance al paso siguiente.

| Entrada | Problema encontrado | Corrección | Prueba |
|---|---|---|---|
| Ciudad del clima | Se aceptaba vacía y el programa pasaba a latitud | Se valida al instante y se vuelve a pedir; no admite vacío, solo espacios, ni números o símbolos | `test_validacion_entradas.py` 01, 02, 03 |
| Latitud y longitud | Aceptaban texto vacío y, en algunos casos, `nan` o `inf` | Se vuelven a pedir si no son números finitos o están fuera de rango | 04, 05 |
| Código de indicador | Un código inválido se mostraba como error al final | Se vuelve a pedir hasta UF, DOLAR o EURO | 06 |
| Confirmaciones S/N | Algunas aceptaban cualquier respuesta como «no» | Se vuelve a pedir si no es s o n (`confirmar`) | 07, 08 |
| IDs de empleado | Aceptan solo enteros positivos | Se vuelven a pedir | 09 |
| Gerente de un departamento | `isdigit()` acepta el superíndice `²`, que luego hacía fallar `int()` y cerraba el programa | Conversión con `try/except` y control de positivo | 10 |
| Salario y horas | Mismo riesgo con `²` | Se rechaza y se vuelve a pedir | 12 |
| Login con usuario vacío | Se rechaza con mensaje genérico, sin revelar si el usuario existe | Se mantiene | 11 |

**Decisión del estudiante:** cualquiera puede crear su propia cuenta y cargar semillas sin ser administrador. Esto no se cambió. Sí se conservan las restricciones por rol para menús, indicadores y administración.

**Decisión tomada:** los accesos `--demo` y `--listar` de `main.py` funcionan sin iniciar sesión y se documentan como comandos de desarrollo (riesgos y uso permitido en `Readme.md`, sección de comandos). No se agrega login ni un rol `sys` por ahora.

## 8. Colaboración con ChatGPT y Claude en la Evaluación 2

Este trabajo fue hecho en colaboración. Ninguna herramienta trabajó sola, y las decisiones finales fueron del estudiante.

**ChatGPT** participó en etapas anteriores del proyecto:
- Explicación de POO, UML y la separación en capas (dominio, persistencia, servicios, presentación).
- Diseño del CRUD, de la persistencia y de las semillas sin duplicados.
- Autenticación con bcrypt, y depuración de duplicados y del menú.
- Diseño de pruebas, revisión del repositorio y de los envíos.
- Orientación sobre APIs y roles.
- Revisión documental del paquete de revisión de esta entrega.

**Claude** participó en la implementación de la Unidad 3:
- Roles `admin` y `empleado`, con su migración y permisos.
- Integración de la API de indicadores (UF, dólar, euro) y de la API de clima.
- Respaldo local cuando la API falla.
- Validación de entradas y manejo de errores.
- Pruebas automatizadas (209 en la suite actual).
- Documentación de verificación (`docs/VERIFICACION_UML_ORIGINAL.md`).

**Lo que ChatGPT y Claude no hicieron:**
- No ejecutaron las pruebas en el equipo del estudiante. Las pruebas se corrieron en un entorno Linux de trabajo y el estudiante debe repetirlas en Windows.
- No crearon commits con la identidad del estudiante. Los commits fueron revisados y autorizados por él antes de subirse.

**Decisiones del estudiante:** la forma de los menús y del registro abierto; los roles (sin rol `sys`); dejar `--demo` y `--listar` como comandos de desarrollo sin login; y qué entrega final se sube.

**Pendiente de completar por el estudiante:** su propio relato de consultas con ChatGPT en clase y la respuesta del profesor, en sus propias palabras. Esta sección no reemplaza ese relato.
