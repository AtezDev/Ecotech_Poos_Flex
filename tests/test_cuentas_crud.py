import contextlib
import io
import os
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion
from persistencia.creacion_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from persistencia.usuario_dao import UsuarioDAO
from presentacion import menu_usuario
from presentacion.menu_principal import menu_principal
from servicios.autenticacion import (
    actualizar_usuario, autenticar, cambiar_clave_propia, cambiar_nombre_propio,
    eliminar_cuenta_propia, registrar_usuario, crear_cuenta
)

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_ANA = 'Clave de Ana para prueba 2026'
NUEVA_ANA = 'Clave nueva de Ana 2026!!'


def ejecutar(funcion, entradas=(), claves=()):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            mock.patch('presentacion.menu_usuario.getpass', side_effect=list(claves)), \
            contextlib.redirect_stdout(salida):
        resultado = funcion()
    return resultado, salida.getvalue()


class TestCuentasCrud(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clave_previa = os.environ.get('ADMIN_PASSWORD')
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        os.environ['ADMIN_PASSWORD'] = CLAVE_ADMIN
        crear_tablas()
        cargar_semillas()
        asegurar_admin_inicial()
        self.admin = autenticar('admin', CLAVE_ADMIN)
        self.ana = crear_cuenta(2, 'luis.soto', CLAVE_ANA)

    def tearDown(self):
        if self.clave_previa is None:
            os.environ.pop('ADMIN_PASSWORD', None)
        else:
            os.environ['ADMIN_PASSWORD'] = self.clave_previa
        self.tmp.cleanup()

    def contar(self, tabla):
        with closing(abrir_conexion()) as c:
            return c.execute(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]

    def test_01_nadie_puede_registrar_el_nombre_admin(self):
        with self.assertRaises(ValueError):
            registrar_usuario(2, 'Admin', CLAVE_ANA)
        self.assertEqual(UsuarioDAO.buscar_por_nombre('admin').empleado_id, 1)

    def test_02_otra_cuenta_no_puede_tomar_el_nombre_admin(self):
        with self.assertRaises(ValueError):
            actualizar_usuario(self.ana.id, nuevo_nombre='admin')

    def test_03_la_cuenta_admin_no_puede_renombrarse(self):
        with self.assertRaises(ValueError):
            actualizar_usuario(self.admin.id, nuevo_nombre='jefe')
        self.assertIsNotNone(autenticar('admin', CLAVE_ADMIN))

    def test_04_cambiar_nombre_propio_exige_clave_actual(self):
        with self.assertRaises(ValueError):
            cambiar_nombre_propio(self.ana.id, 'clave incorrecta de prueba', 'luis.nuevo')
        self.assertIsNone(UsuarioDAO.buscar_por_nombre('luis.nuevo'))
        cambiar_nombre_propio(self.ana.id, CLAVE_ANA, 'luis.nuevo')
        self.assertIsNotNone(autenticar('luis.nuevo', CLAVE_ANA))
        self.assertIsNone(autenticar('luis.soto', CLAVE_ANA))

    def test_05_cambiar_nombre_propio_no_permite_admin(self):
        with self.assertRaises(ValueError):
            cambiar_nombre_propio(self.ana.id, CLAVE_ANA, 'admin')

    def test_06_cambiar_clave_propia(self):
        with self.assertRaises(ValueError):
            cambiar_clave_propia(self.ana.id, 'clave incorrecta de prueba', NUEVA_ANA)
        with self.assertRaises(ValueError):
            cambiar_clave_propia(self.ana.id, CLAVE_ANA, CLAVE_ANA)
        with self.assertRaises(ValueError):
            cambiar_clave_propia(self.ana.id, CLAVE_ANA, 'corta')
        cambiar_clave_propia(self.ana.id, CLAVE_ANA, NUEVA_ANA)
        self.assertIsNotNone(autenticar('luis.soto', NUEVA_ANA))
        self.assertIsNone(autenticar('luis.soto', CLAVE_ANA))

    def test_07_eliminar_cuenta_propia_exige_clave_y_conserva_al_empleado(self):
        with self.assertRaises(ValueError):
            eliminar_cuenta_propia(self.ana.id, 'clave incorrecta de prueba')
        self.assertEqual(self.contar('usuario'), 2)
        self.assertEqual(eliminar_cuenta_propia(self.ana.id, CLAVE_ANA), 1)
        self.assertIsNone(autenticar('luis.soto', CLAVE_ANA))
        self.assertIsNotNone(EmpleadoDAO.buscar_por_id(2))

    def test_08_la_cuenta_admin_no_se_puede_eliminar_desde_mi_cuenta(self):
        with self.assertRaises(ValueError):
            eliminar_cuenta_propia(self.admin.id, CLAVE_ADMIN)
        self.assertIsNotNone(autenticar('admin', CLAVE_ADMIN))

    def test_09_menu_mi_cuenta_cambia_el_nombre(self):
        entradas = ['1', 'luis.nuevo', '0']
        resultado, texto = ejecutar(lambda: menu_usuario.menu_mi_cuenta(self.ana), entradas, [CLAVE_ANA])
        self.assertFalse(resultado)
        self.assertIn('Nombre actualizado a: luis.nuevo', texto)
        self.assertEqual(self.ana.nombre_usuario, 'luis.nuevo')

    def test_10_menu_mi_cuenta_cambia_la_clave(self):
        entradas = ['2', '0']
        claves = [CLAVE_ANA, NUEVA_ANA, NUEVA_ANA]
        _, texto = ejecutar(lambda: menu_usuario.menu_mi_cuenta(self.ana), entradas, claves)
        self.assertIn('Contraseña actualizada correctamente.', texto)
        self.assertIsNotNone(autenticar('luis.soto', NUEVA_ANA))

    def test_11_menu_mi_cuenta_elimina_con_confirmacion(self):
        resultado, texto = ejecutar(lambda: menu_usuario.menu_mi_cuenta(self.ana), ['3', 's'], [CLAVE_ANA])
        self.assertTrue(resultado)
        self.assertIn('Cuenta eliminada', texto)
        self.assertIsNone(autenticar('luis.soto', CLAVE_ANA))

    def test_12_menu_mi_cuenta_cancela_si_no_se_confirma(self):
        resultado, texto = ejecutar(lambda: menu_usuario.menu_mi_cuenta(self.ana), ['3', 'n', '0'], [])
        self.assertFalse(resultado)
        self.assertIn('Eliminación cancelada.', texto)
        self.assertIsNotNone(autenticar('luis.soto', CLAVE_ANA))

    def test_13_admin_registra_cuenta_desde_su_menu(self):
        maria = EmpleadoDAO.buscar_por_id(3)
        claves = ['Clave de Maria para prueba 2026', 'Clave de Maria para prueba 2026']
        _, texto = ejecutar(lambda: menu_usuario.menu_administrar_usuarios(self.admin), ['1', str(maria.id), 'maria.perez', '0'], claves)
        self.assertIn('Cuenta creada para el usuario: maria.perez', texto)
        self.assertIsNotNone(UsuarioDAO.buscar_por_nombre('maria.perez'))

    def test_14_listado_sin_hash(self):
        _, texto = ejecutar(lambda: menu_usuario.menu_administrar_usuarios(self.admin), ['2', '0'])
        self.assertIn('ID: 1 | Usuario: admin | Empleado ID: 1', texto)
        self.assertIn('Usuario: luis.soto', texto)
        self.assertNotIn('$2', texto)

    def test_15_mostrar_datos_no_expone_el_hash(self):
        self.assertNotIn('$2', self.ana.mostrar_datos())
        self.assertIn('luis.soto', self.ana.mostrar_datos())

    def test_16_menu_principal_muestra_mi_cuenta_a_todos_y_administrar_solo_al_admin(self):
        salida = io.StringIO()
        with mock.patch('builtins.input', side_effect=['0']), contextlib.redirect_stdout(salida):
            menu_principal(self.ana)
        self.assertIn('2. Modificar mis datos', salida.getvalue())
        self.assertIn('4. Mi cuenta', salida.getvalue())
        self.assertNotIn('Administrar usuarios', salida.getvalue())
        salida = io.StringIO()
        with mock.patch('builtins.input', side_effect=['0']), contextlib.redirect_stdout(salida):
            menu_principal(self.admin)
        self.assertIn('7. Mi cuenta', salida.getvalue())
        self.assertIn('8. Administrar usuarios', salida.getvalue())
        self.assertIn('9. Indicadores económicos', salida.getvalue())

    def test_17_usuario_normal_no_entra_a_administrar(self):
        _, texto = ejecutar(lambda: menu_usuario.menu_administrar_usuarios(self.ana), [], [])
        self.assertIn('Acceso denegado', texto)


if __name__ == '__main__':
    unittest.main()
