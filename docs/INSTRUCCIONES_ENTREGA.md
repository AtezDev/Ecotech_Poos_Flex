# Instrucciones para la entrega (Evaluación 2, Unidades 2 y 3)

Entrega: viernes 27 de noviembre de 2026, antes de las 23:00, en AAI como carpeta comprimida.
No se aceptan entregas por correo. Después de la entrega viene la defensa individual (ver `docs/DEFENSA_INDIVIDUAL.md`).

## 1. Preparar el entorno
1. Copia la carpeta del proyecto en tu computador (la que contiene `.git`).
2. Crea o revisa tu `.env` con `DB_ENGINE`, `DB_NAME` y `ADMIN_PASSWORD` (mínimo 15 caracteres). El `.env` no se sube a GitHub.
3. Activa el entorno virtual e instala las dependencias: `python -m pip install -r requirements.txt`.

## 2. Verificar que todo funciona
1. Ejecuta las pruebas: `python -m unittest discover -s tests -p "test_*.py"`. Resultado esperado: `Ran 189 tests` y `OK`.
2. Ejecuta el programa: `python src/main.py`.
3. Inicia sesión como `admin` y prueba:
   - Opción 9, luego 2: actualizar UF, DOLAR y EURO desde la API. Debe salir `Origen: API`.
   - Opción 9, luego 1: consultar cada indicador guardado.
   - Opción 9, luego 3: consultar el clima (latitud -29.9, longitud -71.2).
4. Inicia sesión como un empleado (por ejemplo `luis.soto`) y prueba que no puede actualizar indicadores: debe salir `Acción solo para administrador.`.

## 3. Qué debe contener la carpeta
- `src/`, `tests/`, `docs/`, `Readme.md`, `requirements.txt` y `.env.example`.
- No incluir `.env`, `.git`, `.venv`, `__pycache__`, `*.db` ni el archivo `ecotech`.

## 4. Revisión final antes de subir
- [ ] Las 189 pruebas pasan.
- [ ] La API responde (o el respaldo funciona) en UF, DOLAR, EURO y clima.
- [ ] `docs/USO_DE_IA_Y_DECISIONES.md` está completo y coincide con lo que hiciste.
- [ ] El README coincide con el programa (menús, pruebas y pendientes).
- [ ] La carpeta no contiene archivos sensibles.

## 5. Subir
1. Comprime la carpeta sin los archivos excluidos.
2. Sube el ZIP a AAI antes de las 23:00 del viernes. No esperes al último minuto.

## Nota sobre la modalidad
La guía de la evaluación indica trabajo grupal (2 a 3 estudiantes). Si trabajas solo, confirma con el profesor antes de entregar, porque la modalidad afecta a la entrega y a la defensa.
