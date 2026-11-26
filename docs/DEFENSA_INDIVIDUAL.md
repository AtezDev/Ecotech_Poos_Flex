# Preparación de la defensa individual

Cada pregunta indica dónde está la respuesta en el código. Antes de la defensa, explica cada punto con tus propias palabras.

## Unidad 2

**2.1.1 UML a código.** ¿Qué clases del UML están en `src/dominio/`? Revisa `usuario.py`, `indicador.py` y `clima.py`, y explica qué atributos tienen y cómo se relacionan con el diagrama.

**2.1.2 Encapsulamiento y reutilización.** ¿Cómo proteges los datos? Revisa las validaciones de `Usuario` (`validar_rol`, `normalizar_usuario`, `validar_clave`) y de `Indicador`. Explica por qué `password_hash` no se muestra en `mostrar_datos()`.

**2.1.3 Conexión a la base de datos.** ¿Qué librería usas para SQLite y para MySQL? Revisa `persistencia/conexion.py`. Explica la diferencia entre `?` y `%s` en las consultas parametrizadas.

**2.1.4 Manejo de errores.** ¿Qué errores capturas al conectar con la base? Revisa `tipos_errores_bd()` en `presentacion/menu_empleado.py`.

**2.1.5 Uso crítico de IA.** Explica qué fragmento viene de la IA y qué cambiaste. Usa la tabla de `docs/USO_DE_IA_Y_DECISIONES.md`.

## Unidad 3

**3.1.1 Consumo de APIs.** Revisa `servicios/api_indicadores.py` y `servicios/api_clima.py`. Explica qué hace `requests.get`, por qué `timeout=(3, 5)` y qué hace `raise_for_status()`.

**3.1.2 Seguridad.** ¿Cómo se autentica el usuario? Revisa `servicios/autenticacion.py` (`autenticar` y `crear_hash`). Explica qué es bcrypt, qué es un hash y por qué no se guarda la contraseña. Explica también cómo `servicios/permisos.py` impide que un empleado actualice indicadores.

**3.1.3 Manejo de errores externos.** ¿Qué pasa si la API no responde? Revisa `actualizar_indicadores` en `servicios/indicadores.py`. Explica el respaldo y por qué solo se informa `Origen: API` después de guardar.

**3.1.4 Revisión crítica de la IA.** Explica un fragmento que la IA sugirió y que cambiaste: el caso del formato de la API es el más claro.

## Preguntas de práctica
1. ¿Qué pasa si `ADMIN_PASSWORD` no está en `.env`? (Respuesta: `asegurar_admin_inicial` lanza un `ValueError` con mensaje claro.)
2. ¿Qué pasa si guardas dos veces UF con la misma fecha? (Respuesta: una sola fila; el valor se actualiza.)
3. ¿Por qué el empleado no puede ver la opción de actualizar indicadores? (Respuesta: la opción aparece, pero `exigir_admin` rechaza la acción.)
