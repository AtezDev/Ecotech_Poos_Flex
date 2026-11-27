import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from persistencia.creacion_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from presentacion.menu_principal import modificar_mis_datos
from servicios.autenticacion import autenticar, crear_cuenta

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_ANA = 'Clave de Ana para prueba 2026'


def ejecutar(usuario, entradas):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            contextlib.redirect_stdout(salida):
        modificar_mis_datos(usuario)
    return salida.getvalue()


class TestModificarMisDatos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clave_previa = os.environ.get('ADMIN_PASSWORD')
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        os.environ['ADMIN_PASSWORD'] = CLAVE_ADMIN
        crear_tablas()
        cargar_semillas()
        asegurar_admin_inicial()
        autenticar('admin', CLAVE_ADMIN)
        self.ana = crear_cuenta(2, 'ana.mis', CLAVE_ANA)
        self.original = EmpleadoDAO.buscar_por_id(2)

    def tearDown(self):
        if self.clave_previa is None:
            os.environ.pop('ADMIN_PASSWORD', None)
        else:
            os.environ['ADMIN_PASSWORD'] = self.clave_previa
        self.tmp.cleanup()

    def test_01_cambia_la_direccion_propia(self):
        ejecutar(self.ana, ['1', 'Calle Nueva 456', '0'])
        self.assertEqual(EmpleadoDAO.buscar_por_id(2).obtenerDireccion(), 'Calle Nueva 456')

    def test_02_telefono_invalido_se_repite_y_el_valido_se_guarda(self):
        salida = ejecutar(self.ana, ['2', 'abc', '+56987654321', '0'])
        self.assertIn('Teléfono inválido', salida)
        self.assertEqual(EmpleadoDAO.buscar_por_id(2).obtenerTelefono(), '+56987654321')

    def test_03_correo_repetido_no_se_guarda(self):
        otro = EmpleadoDAO.buscar_por_id(1)
        salida = ejecutar(self.ana, ['3', otro.correoElectronico, '0'])
        self.assertIn('ya está registrado', salida)
        self.assertEqual(EmpleadoDAO.buscar_por_id(2).correoElectronico, self.original.correoElectronico)

    def test_04_nombre_salario_y_fecha_no_se_modifican(self):
        ejecutar(self.ana, ['1', 'Calle Nueva 456', '0'])
        actual = EmpleadoDAO.buscar_por_id(2)
        self.assertEqual(actual.nombre, self.original.nombre)
        self.assertEqual(actual.salario, self.original.salario)
        self.assertEqual(actual.fechaInicioContrato, self.original.fechaInicioContrato)

    def test_05_mismo_valor_no_hace_cambios(self):
        salida = ejecutar(self.ana, ['1', self.original.obtenerDireccion(), '0'])
        self.assertIn('no hay cambios', salida)

    def test_06_opcion_invalida_pide_de_nuevo(self):
        salida = ejecutar(self.ana, ['9', '0'])
        self.assertIn('Elige una opción entre 0 y 3', salida)


if __name__ == '__main__':
    unittest.main()
