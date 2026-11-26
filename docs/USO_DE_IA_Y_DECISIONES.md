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
