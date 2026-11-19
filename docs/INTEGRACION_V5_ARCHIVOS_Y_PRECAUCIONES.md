# Integración de la versión v5 — archivos y precauciones

Esta carpeta conserva la estructura original `src/dominio`, `src/persistencia`, `src/presentacion`, `tests` y `docs`. No se renombraron ni movieron carpetas.

## Archivos de Clase 5 incluidos en esta versión

- `src/dominio/reporte.py` — clases `ReporteEmpleados` y `ReportePorDepartamento`.
- `src/persistencia/semillas.py` — carga de dos departamentos y tres empleados sin duplicar en ejecuciones repetidas.
- `src/dominio/empleado.py` y `src/dominio/departamento.py` — relación y validaciones.
- `src/persistencia/creacion_bd.py`, `empleado_dao.py`, `departamento_dao.py` — FK y reconstrucción.
- `src/presentacion/menu_empleado.py`, `menu_departamento.py`, `menu_principal.py` — opciones de Clase 5.
- `tests/test_clase5.py` — 30 pruebas de Clase 5.

## Documentos agregados en v5

- `docs/GUIA_CLASE5_MEJORAS_ECOTECH.pdf` — PDF que compartiste (guía complementaria).
- `docs/GUIA_ESTUDIO_REPORTES_Y_SEMILLAS_ATEZ.md` — explicación pedagógica adicional.

## Reemplazo seguro

1. Haz una copia de respaldo de tu carpeta EcoTech local.
2. No reemplaces ni borres tu `.env`, tu base `ecotech` ni archivos locales que no estén en este ZIP.
3. Compara la carpeta `src`, `tests` y `docs` con tu proyecto actual antes de copiar.
4. Usa una base nueva de práctica (`ecotech_practica`) porque el esquema antiguo con `gerente` texto no se migra automáticamente.
5. Ejecuta `python -m compileall -q src` y `python -m unittest discover -s tests -v`.
6. Recién si las pruebas pasan, revisa `git status`, `git diff --stat` y los cambios antes de `git add`.

No se ha hecho commit ni push desde esta carpeta.
