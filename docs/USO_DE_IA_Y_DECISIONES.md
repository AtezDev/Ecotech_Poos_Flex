# Uso de herramientas de IA y decisiones técnicas

Este documento registra qué fragmentos del proyecto se apoyaron en herramientas de IA,
qué se modificó y qué se descartó. Cada integrante debe completar su parte antes de la defensa.

## Herramientas usadas
- Asistente de IA (Claude) para generar borradores de código y pruebas.

## Fragmentos apoyados por IA y decisión tomada

| Fragmento | Uso | Qué se revisó o modificó | Criterio técnico |
|---|---|---|---|
| `dominio/usuario.py` (rol y validación) | Adoptado con ajustes | Se validó el rol contra una lista fija para evitar valores inventados | Seguridad: un rol desconocido no debe entrar a la BD |
| `persistencia/creacion_bd.py` (migración de `rol`) | Adoptado con ajustes | Se probó con una base creada sin la columna | Estabilidad: una base de la Unidad 2 no debe romperse |
| `servicios/api_indicadores.py` y `servicios/api_clima.py` | Adoptado con ajustes | Se fijó `timeout=(3, 5)` y se agregó `raise_for_status()` | Continuidad: la aplicación no debe quedarse esperando |
| `servicios/indicadores.py` y `servicios/clima.py` (respaldo) | Adoptado con ajustes | Solo se informa «API» después de guardar con éxito | Integridad: no mostrar un dato como actual si no se comprobó |
| `servicios/permisos.py` | Adoptado | Se comprueba el rol en el servicio, no solo en el menú | Autorización: el menú no basta para proteger una acción |
| `persistencia/indicador_dao.py` y `clima_dao.py` | Adoptado con ajustes | Clave compuesta para evitar filas duplicadas | Integridad de datos |

## Hallazgos de revisión (mensajes de error y seguridad)
- Los mensajes que se muestran al usuario no imprimen trazas técnicas ni rutas.
- La clave del administrador se lee desde `.env` (`ADMIN_PASSWORD`) y nunca se escribe en el código.
- Las contraseñas se guardan con bcrypt; nunca en texto plano.

## Pendientes de análisis
- Un fragmento generado por IA que no se pudo verificar contra la API real desde el entorno de desarrollo (bloqueo de red).
  Se validó solo con respuestas ficticias.
