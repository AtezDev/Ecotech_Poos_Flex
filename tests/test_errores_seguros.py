import contextlib
import io
import sqlite3
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import main


class TestErroresSeguros(unittest.TestCase):
    def test_01_fallo_de_base_no_muestra_detalle_tecnico(self):
        detalle = 'C:/secreto/ecotech.db no such table: usuario'
        salida = io.StringIO()
        with mock.patch.object(main, 'crear_tablas', side_effect=sqlite3.OperationalError(detalle)), \
                mock.patch('sys.argv', ['main.py']), \
                contextlib.redirect_stdout(salida):
            main.main()
        texto = salida.getvalue()
        self.assertIn('No se pudo preparar la base de datos', texto)
        self.assertNotIn('secreto', texto)
        self.assertNotIn('no such table', texto)


if __name__ == '__main__':
    unittest.main()
