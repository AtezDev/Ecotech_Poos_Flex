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

import main as programa
from persistencia.conexion import abrir_conexion
from persistencia.creacion_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from persistencia.usuario_dao import UsuarioDAO
from presentacion import menu_departamento, menu_empleado, menu_proyecto
from servicios.autenticacion import autenticar

CLAVE_ADMIN = 'Clave de prueba 2026!'


def ejecutar(funcion, entradas=(), claves=()):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            mock.patch('presentacion.menu_usuario.getpass', side_effect=list(claves)), \
            contextlib.redirect_stdout(salida):
        resultado = funcion()
    return resultado, salida.getvalue()


class TestIdempotencia(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clave_previa = os.environ.get('ADMIN_PASSWORD')
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        os.environ['ADMIN_PASSWORD'] = CLAVE_ADMIN
        crear_tablas()

    def tearDown(self):
        if self.clave_previa is None:
            os.environ.pop('ADMIN_PASSWORD', None)
        else:
            os.environ['ADMIN_PASSWORD'] = self.clave_previa
        self.tmp.cleanup()

    def contar(self, tabla):
        with closing(abrir_conexion()) as c:
            return c.execute(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]

    def conteos(self):
        return {t: self.contar(t) for t in ('empleado', 'departamento', 'proyecto', 'usuario')}

    def test_01_semillas_tres_veces_no_multiplican_datos(self):
        self.assertEqual(cargar_semillas(), (2, 3))
        antes = self.conteos()
        self.assertEqual(cargar_semillas(), (0, 0))
        self.assertEqual(cargar_semillas(), (0, 0))
        self.assertEqual(self.conteos(), antes)
        self.assertEqual((antes['empleado'], antes['departamento']), (3, 2))

    def test_02_admin_inicial_no_se_duplica(self):
        cargar_semillas()
        self.assertTrue(asegurar_admin_inicial())
        primera = UsuarioDAO.buscar_por_nombre('admin')
        self.assertFalse(asegurar_admin_inicial())
        self.assertFalse(asegurar_admin_inicial())
        self.assertEqual(self.contar('usuario'), 1)
        self.assertEqual(UsuarioDAO.buscar_por_nombre('admin').id, primera.id)

    def test_03_opcion_semillas_del_acceso_repetida_no_duplica_cuentas(self):
        for _ in range(3):
            _, texto = ejecutar(_menu_semillas_y_salir, ["3", "0"])
        self.assertEqual(self.conteos(), {'empleado': 3, 'departamento': 2, 'proyecto': 0, 'usuario': 1})
        self.assertIsNotNone(autenticar('admin', CLAVE_ADMIN))

    def test_04_demo_dos_veces_no_duplica(self):
        with contextlib.redirect_stdout(io.StringIO()):
            programa.demostrar_relaciones()
        primera = self.conteos()
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            programa.demostrar_relaciones()
        self.assertEqual(self.conteos(), primera)
        self.assertIn('no se duplicó ningún dato', salida.getvalue())
        self.assertEqual(primera['empleado'], 1)
        self.assertEqual(primera['proyecto'], 1)

    def test_05_demo_despues_de_semillas_reutiliza_el_departamento(self):
        cargar_semillas()
        with contextlib.redirect_stdout(io.StringIO()):
            programa.demostrar_relaciones()
        with contextlib.redirect_stdout(io.StringIO()):
            programa.demostrar_relaciones()
        self.assertEqual(self.contar('departamento'), 2)
        self.assertEqual(self.contar('empleado'), 4)
        self.assertEqual(self.contar('proyecto'), 1)

    def test_06_correo_repetido_al_registrar_empleado_se_rechaza(self):
        cargar_semillas()
        entradas = ['Ana Torres Repetida', 'Av. Test 123, La Serena', '+56911119999',
                    'ana.torres@ecotech.cl', '2026-03-02', '900000']
        _, texto = ejecutar(menu_empleado.crear_empleado, entradas)
        self.assertIn('Ya existe un empleado con ese correo', texto)
        self.assertEqual(self.contar('empleado'), 3)

    def test_07_correo_nuevo_si_se_registra(self):
        cargar_semillas()
        entradas = ['Pedro Nuevo', 'Av. Test 123, La Serena', '+56911119999',
                    'pedro.nuevo@ecotech.cl', '2026-03-02', '900000']
        _, texto = ejecutar(menu_empleado.crear_empleado, entradas)
        self.assertIn('Empleado registrado', texto)
        self.assertEqual(self.contar('empleado'), 4)

    def test_08_actualizar_correo_a_uno_ajeno_se_rechaza(self):
        cargar_semillas()
        _, texto = ejecutar(menu_empleado.actualizar_empleado, ['2', 'ana.torres@ecotech.cl'])
        self.assertIn('Ese correo ya pertenece a otro empleado', texto)
        luis = EmpleadoDAO.buscar_por_id(2)
        self.assertEqual(luis.correoElectronico, 'luis.soto@ecotech.cl')

    def test_09_departamento_repetido_se_rechaza(self):
        cargar_semillas()
        _, texto = ejecutar(menu_departamento.crear_departamento, ['Soporte'])
        self.assertIn('Ya existe un departamento con ese nombre', texto)
        self.assertEqual(self.contar('departamento'), 2)

    def test_10_proyecto_repetido_se_rechaza(self):
        ejecutar(menu_proyecto.crear_proyecto, ['EcoTech', 'Descripción', '2026-11-10'])
        _, texto = ejecutar(menu_proyecto.crear_proyecto, ['EcoTech', 'Otra', '2026-11-10'])
        self.assertIn('Ya existe un proyecto con ese nombre', texto)
        self.assertEqual(self.contar('proyecto'), 1)

    def test_12_sin_admin_password_no_se_crea_la_cuenta(self):
        cargar_semillas()
        os.environ.pop('ADMIN_PASSWORD')
        with self.assertRaises(ValueError) as contexto:
            asegurar_admin_inicial()
        self.assertIn('Falta ADMIN_PASSWORD', str(contexto.exception))
        self.assertEqual(self.contar('usuario'), 0)
        _, texto = ejecutar(_menu_semillas_y_salir, ['3', '0'])
        self.assertIn('No se pudo crear el administrador inicial: Falta ADMIN_PASSWORD', texto)
        self.assertEqual(self.contar('usuario'), 0)

    def test_13_clave_admin_corta_se_rechaza(self):
        cargar_semillas()
        os.environ['ADMIN_PASSWORD'] = 'ecotech'
        with self.assertRaises(ValueError) as contexto:
            asegurar_admin_inicial()
        self.assertIn('al menos 15 caracteres', str(contexto.exception))
        self.assertEqual(self.contar('usuario'), 0)

    def test_14_admin_existente_no_exige_la_clave(self):
        cargar_semillas()
        asegurar_admin_inicial()
        os.environ.pop('ADMIN_PASSWORD')
        self.assertFalse(asegurar_admin_inicial())
        self.assertEqual(self.contar('usuario'), 1)

    def test_11_buscadores_devuelven_none_si_no_existe(self):
        self.assertIsNone(EmpleadoDAO.buscar_id_por_correo('nadie@ecotech.cl'))
        self.assertIsNone(DepartamentoDAO.buscar_id_por_nombre('Nada'))
        self.assertIsNone(ProyectoDAO.buscar_id_por_nombre('Nada'))


def _menu_semillas_y_salir():
    from presentacion.menu_usuario import menu_acceso
    return menu_acceso()


if __name__ == '__main__':
    unittest.main()
