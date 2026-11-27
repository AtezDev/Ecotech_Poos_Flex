# Uso de herramientas de IA y decisiones técnicas — EcoTech Solutions

Este documento registra el uso de herramientas de IA en el desarrollo de EcoTech Solutions. El trabajo fue individual: el estudiante estudió cada clase, revisó las propuestas, decidió cuáles aceptar, modificar o descartar, y ejecutó y verificó los cambios en su propio computador.

Dos herramientas participaron, en etapas distintas:
- **ChatGPT** acompañó el aprendizaje y la revisión progresiva del código durante las primeras clases, y luego en la comprensión de Git/GitHub, la arquitectura y la correspondencia con el UML.
- **Claude** escribió la mayor parte de los cambios y pruebas de la Unidad 3 (clima, indicadores, roles, validaciones). El estudiante los copió, los ejecutó, los ajustó cuando hizo falta y decidió qué quedaba.

Las pruebas de la API real se hicieron en el computador del estudiante, porque el entorno del asistente no tenía acceso a la API.

## 1. Enfoque de trabajo y responsabilidad del estudiante

El estudiante mantuvo la responsabilidad de coordinar el trabajo entre herramientas, revisar las propuestas, decidir qué incorporar y comprobar los cambios en su entorno. Que una respuesta haya sido propuesta por una IA no la hace correcta por sí sola.

En la Unidad 3, el flujo fue este: el asistente propuso los cambios y las pruebas; el estudiante los copió al proyecto, ejecutó las pruebas y el programa en su computador, reportó los resultados y pidió correcciones cuando algo no funcionó. Los commits y los `push` a GitHub del proyecto los hizo el estudiante. El asistente ejecutó solo dos o tres, en la última etapa, a pedido del estudiante.

## 2. Apoyo de ChatGPT durante el aprendizaje y desarrollo

### 2.1 Revisión progresiva del código según los contenidos de clases
En las primeras etapas, el estudiante compartía el avance y pedía una revisión basada en lo que había aprendido hasta ese momento. ChatGPT ayudaba a examinar la lógica, explicar por qué una instrucción o estructura funcionaba de cierta manera y señalar posibles errores, omisiones o mejoras. Cuando aparecía una mejora, primero se analizaba su propósito y funcionamiento; el estudiante evaluaba si correspondía aplicarla según los requerimientos y su comprensión de la materia.

Así se trabajó de forma incremental: estudiar el concepto, revisar cómo se reflejaba en el proyecto, entender la lógica de un cambio, implementarlo personalmente y pedir después una nueva revisión para comprobar que había quedado coherente.

### 2.2 Aprendizaje de Git, GitHub y organización del repositorio
ChatGPT apoyó el aprendizaje del flujo de trabajo con Git y GitHub: consultar el estado del repositorio, registrar cambios, preparar confirmaciones (*commits*), trabajar con la rama y publicar avances. También se estudió la organización del repositorio: propósito de cada carpeta, ubicación de los módulos y relación entre archivos.

El propósito fue que el estudiante entendiera qué hacía cada comando y cómo se reflejaba en el historial y en el repositorio remoto, en lugar de copiar instrucciones sin comprenderlas.

### 2.3 Revisión del UML y correspondencia con las clases
Clase a clase se revisó el modelo UML y su relación con la implementación en Python: qué representa cada clase, sus atributos y métodos, sus relaciones y qué debía comprobarse en el código para mantener coherencia con el diseño. El diagrama UML original se mantuvo como referencia; las revisiones del código no se usaron para alterar ese modelo.

### 2.4 Comprensión de la arquitectura y del patrón DAO
Se estudió la separación de responsabilidades: por qué el acceso a datos se separa de las clases del dominio, y cómo se relacionan la presentación, los servicios, las entidades, los DAO y la conexión con la base de datos. Las explicaciones se relacionaron con ejemplos del propio proyecto para que el estudiante pudiera justificar la arquitectura.

### 2.5 Propuestas de mejora y validación posterior
Una mejora detectada se presentaba como alternativa para analizar, no como cambio automático: se explicaba el problema, la lógica de la propuesta, sus ventajas y sus posibles efectos en el resto del proyecto. Si el estudiante decidía implementarla, después pedía una nueva revisión para confirmar la coherencia del cambio, detectar errores introducidos y verificar que correspondía a lo esperado.

## 3. Trabajo con Claude en la Unidad 3

Claude propuso y escribió la mayor parte del código y de las pruebas de la Unidad 3, a partir de las preguntas del estudiante y del material de clase que él entregaba. El estudiante decidió qué incorporar, ejecutó las pruebas en su computador y pidió los ajustes. Los cambios de la Unidad 3 incluyeron:
- Roles `admin` y `empleado`, con su migración y permisos (`servicios/permisos.py`).
- Integración de la API de indicadores (UF, dólar, euro) y de la API de clima (Open-Meteo).
- Respaldo local cuando la API falla.
- Validación de entradas y manejo de errores.
- Pruebas automatizadas de esas funciones (218 pruebas en la suite actual).
- Documentación de verificación (`docs/VERIFICACION_UML_ORIGINAL.md`).

Las propuestas se aplicaban como cambios que el estudiante probaba en su computador. Cuando algo fallaba, el asistente proponía una corrección y el estudiante decidía.

## 4. Registro de decisiones (Unidad 3)

| Fecha | Propuesta del asistente | Decisión del estudiante | Resultado |
|---|---|---|---|
| 24-nov | Agregar rol (`admin`/`empleado`) a `Usuario` y reemplazar la validación por nombre | Aceptada (la pidió con la guía de Clase 7) | Migración de la tabla `usuario`; pruebas OK |
| 24-nov | Consumo de la API de indicadores con `requests`, `timeout=(3, 5)` y `raise_for_status()` | Aceptada | Pruebas con JSON ficticio OK |
| 24-nov | Tabla `indicador` con clave `(codigo, fecha)` para no duplicar datos | Aceptada | Prueba de guardar dos veces: una sola fila |
| 24-nov | Respaldo local cuando la API falla | Aceptada | Pruebas con fallas simuladas OK |
| 25-nov | Menú del empleado con ficha, indicadores y cuenta | Aceptada | Implementada |
| 26-nov | Módulo de clima con Open-Meteo (sin clave) | Aceptada | Funciona en el computador del estudiante |
| 26-nov | Adaptador de la API ajustado al formato real (`data.uf`, `data.dolar`, `data.euro`) | Aceptada tras la prueba real del estudiante | UF, dólar y euro guardados y consultados |
| 26-nov | Agregar dólar y euro (tipo de cambio) | Aceptada | Pruebas OK y consulta real OK |
| 27-nov | Opción «Modificar mis datos» para el empleado: dirección, teléfono y correo (nombre, salario, fecha e ID no se cambian) | Pedida por el estudiante | Implementada con validadores y pruebas (`test_mis_datos.py`) |
| 27-nov | Verificar correo repetido al modificar datos, en el admin y en el empleado | Aceptada | Pruebas 07 y 08 de `test_mis_datos.py` |
| 27-nov | Ocultar el detalle técnico de errores al arrancar la base de datos | Aceptada | `test_errores_seguros.py` |

## 5. Código revisado y fragmentos apoyados por IA

### 5.1 Correcciones tras revisión
- **Adaptador de la API.** El primer diseño seguía el ejemplo de la diapositiva (`codigo` y `serie`). La respuesta real tiene otra forma (`status` y `data`). El fallo se detectó en la prueba real del estudiante y se corrigió. Criterio: la prueba con el servicio real vale más que el ejemplo de la diapositiva.
- **Clave del administrador.** Se lee desde `.env` (`ADMIN_PASSWORD`) y no se escribe en el código. Criterio: no exponer credenciales.
- **Contraseñas.** Se guardan con bcrypt. Criterio: no guardar contraseñas en texto plano.
- **Mensajes de error.** No muestran trazas técnicas ni rutas. Criterio: no exponer información sensible al usuario. El arranque de la base ya no imprime el error técnico completo.

### 5.2 Fragmentos apoyados por IA y decisión tomada

| Fragmento | Origen | Decisión | Criterio técnico |
|---|---|---|---|
| `src/servicios/api_indicadores.py` (consulta y extracción) | Propuesta del asistente, con el formato del ejemplo de la diapositiva | Modificado | La respuesta real de la API tiene otra forma (`status` y `data`); se detectó en la prueba real |
| `src/servicios/api_clima.py` (Open-Meteo) | Propuesta del asistente | Aceptado tras prueba real | Sin clave, con latitud y longitud validadas |
| `src/servicios/permisos.py` (`exigir_sesion`, `exigir_admin`) | Propuesta del asistente | Aceptado | Dos niveles de control de acceso |
| `src/presentacion/menu_clima.py` (`solicitar_numero`) | Propuesta del asistente | Aceptado y reforzado | Rechaza vacío, texto, `nan`, `inf` y valores fuera de rango |
| Respaldo local de la API (`servicios/indicadores.py`, `servicios/clima.py`) | Propuesta del asistente | Aceptado | Muestra el último dato guardado; no consulta otra API |

## 6. Aportes y límites de cada herramienta

**ChatGPT** cumplió sobre todo una función de tutoría técnica, análisis y revisión iterativa:
- Explicación de conceptos de POO y revisión de su aplicación en las clases del proyecto.
- Revisión del código del estudiante según los contenidos de cada etapa.
- Análisis de la lógica de métodos, atributos, constructores y relaciones entre clases.
- Explicación de la separación por capas y del rol de los DAO.
- Apoyo para comprender Git, GitHub y la organización del repositorio.
- Revisión de la correspondencia entre el UML original y la implementación.
- Análisis de alternativas de implementación, explicando su fundamento antes de que el estudiante decidiera.
- Revisión externa de la documentación de entrega.

**Claude** escribió la mayor parte de los cambios y pruebas de la Unidad 3, y los documentos de verificación. Ejecutó pruebas en su entorno de trabajo, no en el equipo del estudiante.

**Lo que ninguna de las dos herramientas hizo:**
- No ejecutaron las pruebas ni el programa en el equipo del estudiante. Las pruebas en Windows y en MySQL/WampServer las debe repetir el estudiante.
- No se atribuye a ninguna de las dos la autoría exclusiva del proyecto ni decisiones que tomó el estudiante.

## 7. Criterios para evaluar propuestas de IA

Las propuestas se analizaron según el caso:
1. **Correspondencia con los requerimientos:** si resolvían una necesidad real de la evaluación y del sistema.
2. **Comprensión:** si el estudiante podía explicar qué hacía el cambio y por qué era necesario.
3. **Coherencia arquitectónica:** si respetaban las responsabilidades de las clases y capas existentes.
4. **Compatibilidad:** si se integraban con el código, la base de datos y el flujo existente.
5. **Seguridad y validación:** si evitaban exponer información sensible, aceptar entradas inválidas o permitir operaciones no autorizadas.
6. **Mantenibilidad:** si reducían duplicación o complejidad sin introducir abstracciones innecesarias.
7. **Verificación:** si el resultado podía revisarse por lectura del código, ejecución o pruebas.

Cuando una propuesta no se ajustaba al diseño, excedía los contenidos o requerimientos, o no podía justificarse, se modificaba o se descartaba. La decisión final fue del estudiante.

## 8. Validación de entradas y decisiones de acceso

Pedido del estudiante: que todas las entradas se validen y que ningún dato vacío, con caracteres no válidos o fuera de rango haga caer el programa o avance al paso siguiente.

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

**Decisión del estudiante:** cualquiera puede crear su propia cuenta y cargar semillas sin ser administrador. Se conservan las restricciones por rol para menús, indicadores y administración.

**Decisión del estudiante:** los accesos `--demo` y `--listar` de `main.py` funcionan sin iniciar sesión y se documentan como comandos de desarrollo (riesgos y uso permitido en `Readme.md`). No se agrega login ni un rol `sys` por ahora.

**Decisión del estudiante:** el empleado puede modificar su dirección, teléfono y correo; nombre, salario, fecha de contrato e ID no se modifican desde su menú.

## 9. Evidencia y transparencia

Este documento describe el proceso de colaboración y aprendizaje, pero no presenta estas descripciones como transcripciones literales de prompts. Los mensajes exactos solo deben citarse cuando se disponga de su registro original.

Las conversaciones disponibles pueden asociarse con los archivos y cambios del repositorio: revisiones de código, explicaciones de arquitectura y DAO, análisis del UML, consultas sobre Git/GitHub y revisiones posteriores a cambios del estudiante. No se inventan fechas, prompts textuales, pruebas ni modificaciones que no estén respaldadas.

Los relatos del estudiante sobre sus consultas a ChatGPT son los de las secciones 2.1 a 2.5. No se agregan prompts textuales que no estén respaldados.

## 10. Pendientes que el estudiante debe revisar
- Confirmar con el profesor que el empleado puede modificar su dirección, teléfono y correo, y que nombre, salario, fecha de contrato e ID no se modifican.
- Ejecutar las pruebas en Windows y probar MySQL/WampServer antes de subir la entrega.

## 11. Reflexión del estudiante

El uso de IA fue parte de un proceso de aprendizaje progresivo. La utilidad principal no fue obtener código para copiar, sino contar con explicaciones y revisiones que permitieran entender lo desarrollado en clases y relacionarlo con un proyecto real. El estudiante contrastó las propuestas con lo aprendido, preguntó por la lógica de las soluciones, decidió cuáles tenían sentido y realizó los cambios que consideró pertinentes.

La responsabilidad por el resultado final y por las decisiones adoptadas permaneció en el estudiante.
