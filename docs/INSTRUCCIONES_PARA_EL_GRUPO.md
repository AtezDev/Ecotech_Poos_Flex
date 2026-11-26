# Instrucciones para terminar la entrega (Evaluación 2)

Entrega: viernes 27 de noviembre de 2026, antes de las 23:00, subida a la plataforma AAI como carpeta comprimida.
No se aceptan entregas por correo.

## 1. Antes de empezar
1. Copia la carpeta `Ecotech_Poos_Flex` en tu computador.
2. Crea tu archivo `.env` copiando `.env.example` y pon tu propia `ADMIN_PASSWORD` (mínimo 15 caracteres). No subas `.env` al repositorio.
3. Instala las dependencias: `python -m pip install -r requirements.txt`.

## 2. Verificar que todo funciona
1. `python src/main.py --demo` (opcional, carga la demostración de clases anteriores).
2. `python src/main.py` → opción 3 (semillas) para crear empleados, departamentos y la cuenta admin.
3. Inicia sesión como `admin`, crea la cuenta de `luis.soto` si hace falta, y prueba la opción 9 → 2 (actualizar UF).
4. Inicia sesión como `luis.soto` y prueba que no puede actualizar la UF pero sí consultarla.
5. Prueba la consulta de clima (opción 3 dentro de «Indicadores económicos») con La Serena: latitud -29.9, longitud -71.2.
6. Ejecuta las pruebas: `python -m unittest discover -s tests -p "test_*.py"`.

## 3. Lo que debe quedar listo
- [ ] Consumo de API de clima y de API de indicadores con `requests` (ya implementado: UF y clima).
- [ ] Validación de entradas: ciudad, latitud, longitud y rol.
- [ ] Autenticación con contraseñas encriptadas y sesión obligatoria.
- [ ] Manejo de errores: conexión, respuesta sin datos y permisos, con mensajes sin información sensible.
- [ ] Respaldo local cuando la API no responde.
- [ ] `docs/USO_DE_IA_Y_DECISIONES.md` completado por cada integrante con sus propios fragmentos.
- [ ] README revisado.

## 4. Pendiente que debe decidir el grupo
- **Moneda (tipo de cambio):** la guía pide monedas internacionales. Hoy está la UF. Si tu grupo tiene una API de moneda, avisar para agregarla igual que el clima.

## 5. Entrega
1. Comprime la carpeta `Ecotech_Poos_Flex` **sin** `.env`, `.git`, `.venv`, `__pycache__`, `*.db` ni `ecotech`.
2. Sube el ZIP a AAI antes de las 23:00 del viernes. No esperes al último minuto.

## 6. Defensa individual
Cada integrante debe poder explicar:
- Qué clases y métodos escribió y cómo se relacionan con el UML.
- Cómo funciona el `try/except` de la API y qué pasa cuando falla.
- Qué fragmentos vinieron de IA, qué cambió y por qué.
