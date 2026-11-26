import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from persistencia.creacion_bd import crear_tablas
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from presentacion import menu_clima, menu_comun, menu_departamento, menu_empleado, menu_indicadores
from servicios.autenticacion import autenticar, crear_cuenta

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_LUIS = 'Clave de Luis para prueba 2026'


def correr(funcion, entradas, *args, consulta=None):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            contextlib.redirect_stdout(salida):
        if consulta is None:
            resultado = funcion(*args)
        else:
            with mock.patch(consulta, side_effect=AssertionError('no debía consultar la API')):
                resultado = funcion(*args)
    return resultado, salida.getvalue()


class TestValidacionEntradas(unittest.TestCase):
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
        self.luis = crear_cuenta(2, 'luis.soto', CLAVE_LUIS)

    def tearDown(self):
        if self.clave_previa is None:
            os.environ.pop('ADMIN_PASSWORD', None)
        else:
            os.environ['ADMIN_PASSWORD'] = self.clave_previa
        self.tmp.cleanup()

    # Clima: ciudad
    def test_01_ciudad_vacia_o_con_solo_espacios_se_vuelve_a_pedir(self):
        entradas = ['', '   ', 'La Serena', 'La Serena 2', '2', 'La Serena', '-29.9', '-71.2']
        _, texto = correr(menu_clima.solicitar_ciudad, entradas[:3])
        self.assertIn('Ciudad no válida', texto)

    def test_02_ciudad_con_numeros_o_simbolos_se_rechaza(self):
        for mala in ('La Serena 2', 'Lima;DROP', '123', '@@'):
            with self.subTest(ciudad=mala):
                resultado, texto = correr(menu_clima.solicitar_ciudad, [mala, 'Coquimbo'])
                self.assertEqual(resultado, 'Coquimbo')
                self.assertIn('Ciudad no válida', texto)

    def test_03_ciudad_vacia_no_avanza_a_latitud(self):
        entradas = ['', 'La Serena', '-29.9', '-71.2']
        with mock.patch('builtins.input', side_effect=entradas) as entrada, \
                mock.patch('servicios.clima.consultar_api_clima', side_effect=requests.ConnectionError('sin red')), \
                contextlib.redirect_stdout(io.StringIO()):
            menu_clima.menu_clima(self.luis)
        prompts = [llamada.args[0] for llamada in entrada.call_args_list]
        self.assertTrue(prompts[0].startswith('Ciudad'))
        self.assertTrue(prompts[1].startswith('Ciudad'))
        self.assertTrue(prompts[2].startswith('Latitud'))

    # Clima: latitud y longitud
    def test_04_latitud_y_longitud_rechazan_letras_vacios_y_rangos(self):
        entradas = ['abc', '', '95', '-29,9', '-71.2']
        resultado, texto = correr(menu_clima.solicitar_numero, entradas, 'Latitud', -90, 90)
        self.assertEqual(resultado, -29.9)
        self.assertIn('Escribe solo un número', texto)
        self.assertIn('Este dato es obligatorio', texto)
        self.assertIn('Debe estar entre -90 y 90', texto)

    def test_05_latitud_nan_e_infinito_se_rechazan(self):
        resultado, texto = correr(menu_clima.solicitar_numero, ['nan', 'inf', '10'], 'X', -90, 90)
        self.assertEqual(resultado, 10.0)
        self.assertIn('no infinito ni vacío', texto)

    # Indicadores
    def test_06_codigo_de_indicador_invalido_se_vuelve_a_pedir(self):
        resultado, texto = correr(menu_indicadores.solicitar_codigo_indicador,
                                  ['', 'XYZ', '   ', 'uf'])
        self.assertEqual(resultado, 'UF')
        self.assertIn('Escribe el nombre del indicador', texto)
        self.assertIn('Indicador no reconocido', texto)

    # Confirmaciones S/N
    def test_07_confirmar_solo_acepta_s_o_n(self):
        resultado, texto = correr(menu_comun.confirmar, ['', 'si', 'x', 'N'], '¿Seguro?')
        self.assertFalse(resultado)
        self.assertEqual(texto.count('Responde s o n.'), 3)

    def test_08_confirmacion_de_empleado_solo_acepta_s_o_n(self):
        resultado, texto = correr(menu_empleado.confirmar_eliminacion, ['  ', 'sí', 'S'])
        self.assertTrue(resultado)
        self.assertEqual(texto.count('Responde s o n.'), 2)

    # IDs y gerente
    def test_09_id_de_empleado_rechaza_texto_cero_y_negativos(self):
        resultado, texto = correr(menu_empleado.solicitar_id, ['', 'abc', '0', '-5', '2'])
        self.assertEqual(resultado, 2)
        self.assertEqual(texto.count('Ingresa un número entero mayor que cero.'), 4)

    def test_10_gerente_con_superindice_no_cierra_el_programa(self):
        empleados = [mock.Mock(id=1, nombre='Ana')]
        with mock.patch('presentacion.menu_departamento.EmpleadoDAO.listar', return_value=empleados), \
                mock.patch('presentacion.menu_departamento.EmpleadoDAO.buscar_por_id',
                           return_value=empleados[0]):
            resultado, texto = correr(menu_departamento.seleccionar_gerente, ['²', 'abc', '-1', '1'])
        self.assertIs(resultado, empleados[0])
        self.assertIn('Escribe solo el número de ID', texto)
        self.assertIn('El ID debe ser positivo.', texto)

    # Login y cuenta
    def test_11_login_con_nombre_vacio_no_se_cae(self):
        from presentacion.menu_usuario import solicitar_login
        salida = io.StringIO()
        with mock.patch('builtins.input', return_value=''), \
                mock.patch('presentacion.menu_usuario.getpass', return_value='x'), \
                contextlib.redirect_stdout(salida):
            resultado = solicitar_login()
        self.assertIsNone(resultado)
        self.assertIn('No se pudo validar el acceso.', salida.getvalue())

    def test_12_campos_numericos_con_superindice_no_cierran_el_programa(self):
        from presentacion.menu_comun import validar_horas
        from presentacion.menu_empleado import solicitar_salario
        with self.assertRaises(ValueError):
            validar_horas('²')
        with mock.patch('builtins.input', side_effect=['²', '950000']), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(menu_empleado.solicitar('Salario', solicitar_salario), 950000.0)


if __name__ == '__main__':
    unittest.main()
