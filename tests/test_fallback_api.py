import contextlib
import io
import os
import sqlite3
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest import mock

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from dominio.clima import Clima
from dominio.indicador import Indicador
from persistencia.clima_dao import ClimaDAO
from persistencia.creacion_bd import crear_tablas
from persistencia.indicador_dao import IndicadorDAO
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from servicios.autenticacion import autenticar, crear_cuenta
from servicios.clima import consultar_clima
from servicios.indicadores import actualizar_indicadores

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_LUIS = 'Clave de Luis para prueba 2026'


def json_valido():
    return {'status': 'success', 'data': {
        'dolar': {'date': '2026-01-05', 'value': 900.5},
        'uf': {'date': '2026-01-05', 'value': 40000.0},
        'euro': {'date': '2026-01-05', 'value': 950.25}}}


def json_clima():
    return {'current': {'time': '2026-01-05T12:00', 'temperature_2m': 18.4,
                        'relative_humidity_2m': 62, 'weather_code': 2}}


def respuesta(codigo=200, datos=None, error_json=None):
    r = mock.Mock(status_code=codigo)
    if error_json is not None:
        r.json.side_effect = error_json
    else:
        r.json.return_value = datos
    return r


class TestFallbackApi(unittest.TestCase):
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
        IndicadorDAO.guardar(Indicador('UF', '2026-01-02', 39900.0))
        IndicadorDAO.guardar(Indicador('DOLAR', '2026-01-02', 890.0))
        IndicadorDAO.guardar(Indicador('EURO', '2026-01-02', 940.0))
        ClimaDAO.guardar(Clima('La Serena', '2026-01-02T12:00', 17.0, 70, 'Nublado'))

    def tearDown(self):
        if self.clave_previa is None:
            os.environ.pop('ADMIN_PASSWORD', None)
        else:
            os.environ['ADMIN_PASSWORD'] = self.clave_previa
        self.tmp.cleanup()

    def filas(self):
        with closing(sqlite3.connect(os.environ['DB_NAME'])) as c:
            return c.execute('SELECT codigo, fecha, valor FROM indicador ORDER BY codigo').fetchall()

    def cambiar_api(self, datos_mock):
        with mock.patch('servicios.indicadores.consultar_api', **datos_mock):
            return actualizar_indicadores(self.admin)

    def test_01_fallas_de_red_usan_respaldo_sin_escribir(self):
        antes = self.filas()
        casos = {
            'timeout': {'side_effect': requests.Timeout('lento')},
            'sin conexion': {'side_effect': requests.ConnectionError('sin red')},
        }
        for nombre, cfg in casos.items():
            with self.subTest(falla=nombre):
                indicadores, origen = self.cambiar_api(cfg)
                self.assertEqual(origen, 'respaldo')
                self.assertEqual(self.filas(), antes)

    def test_02_errores_http_usan_respaldo(self):
        antes = self.filas()
        for codigo in (404, 500, 503, 418):
            with self.subTest(http=codigo):
                with mock.patch('servicios.api_indicadores.requests.get', return_value=respuesta(codigo)):
                    indicadores, origen = actualizar_indicadores(self.admin)
                self.assertEqual(origen, 'respaldo')
                self.assertEqual(self.filas(), antes)

    def test_03_json_invalido_usa_respaldo(self):
        antes = self.filas()
        with mock.patch('servicios.api_indicadores.requests.get',
                        return_value=respuesta(200, error_json=ValueError('no es JSON'))):
            indicadores, origen = actualizar_indicadores(self.admin)
        self.assertEqual(origen, 'respaldo')
        self.assertEqual(self.filas(), antes)

    def test_04_cambios_en_el_formato_de_la_api_usan_respaldo(self):
        antes = self.filas()
        cambios = {
            'estado de error': {'status': 'error'},
            'sin bloque data': {'status': 'success'},
            'falta la UF': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
            'valor como texto': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'uf': {'date': '2026-01-05', 'value': '40000'},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
            'valor cero': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'uf': {'date': '2026-01-05', 'value': 0},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
            'valor negativo': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'uf': {'date': '2026-01-05', 'value': -40000},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
            'fecha con otro formato': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'uf': {'date': '05/01/2026', 'value': 40000.0},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
            'valor booleano': {'status': 'success', 'data': {
                'dolar': {'date': '2026-01-05', 'value': 900.5},
                'uf': {'date': '2026-01-05', 'value': True},
                'euro': {'date': '2026-01-05', 'value': 950.25}}},
        }
        for nombre, datos in cambios.items():
            with self.subTest(cambio=nombre):
                with mock.patch('servicios.api_indicadores.requests.get',
                                return_value=respuesta(200, datos)):
                    indicadores, origen = actualizar_indicadores(self.admin)
                self.assertEqual(origen, 'respaldo')
                self.assertEqual(self.filas(), antes)

    def test_05_respaldo_muestra_el_ultimo_dato_con_su_fecha(self):
        with mock.patch('servicios.api_indicadores.requests.get',
                        return_value=respuesta(500)):
            indicadores, origen = actualizar_indicadores(self.admin)
        uf = [i for i in indicadores if i is not None and i.codigo == 'UF'][0]
        self.assertEqual((uf.fecha, uf.valor), ('2026-01-02', 39900.0))

    def test_06_sin_respaldo_informa_sin_dato(self):
        with closing(sqlite3.connect(os.environ['DB_NAME'])) as c:
            c.execute('DELETE FROM indicador')
            c.commit()
        with mock.patch('servicios.api_indicadores.requests.get', return_value=respuesta(500)):
            indicadores, origen = actualizar_indicadores(self.admin)
        self.assertEqual(origen, 'respaldo')
        self.assertTrue(all(i is None for i in indicadores))

    def test_07_clima_con_fallas_usa_respaldo(self):
        cambios = {
            'http 500': respuesta(500),
            'json invalido': respuesta(200, error_json=ValueError('x')),
            'sin bloque current': respuesta(200, {'otro': 1}),
            'temperatura texto': respuesta(200, {'current': {'time': 'x', 'temperature_2m': 'x',
                                                              'relative_humidity_2m': 60, 'weather_code': 1}}),
            'humedad fuera de rango': respuesta(200, {'current': {'time': '2026-01-05T12:00',
                                                                    'temperature_2m': 18,
                                                                    'relative_humidity_2m': 150,
                                                                    'weather_code': 1}}),
            'codigo de clima no entero': respuesta(200, {'current': {'time': '2026-01-05T12:00',
                                                                       'temperature_2m': 18,
                                                                       'relative_humidity_2m': 60,
                                                                       'weather_code': 'x'}}),
        }
        for nombre, r in cambios.items():
            with self.subTest(cambio=nombre):
                with mock.patch('servicios.api_clima.requests.get', return_value=r):
                    clima, origen = consultar_clima(self.luis, 'La Serena', -29.9, -71.2)
                self.assertEqual(origen, 'respaldo')
                self.assertEqual(clima.temperatura, 17.0)

    def test_08_clima_con_red_caida_usa_respaldo(self):
        with mock.patch('servicios.api_clima.requests.get',
                        side_effect=requests.ConnectionError('sin red')):
            clima, origen = consultar_clima(self.luis, 'La Serena', -29.9, -71.2)
        self.assertEqual(origen, 'respaldo')
        self.assertEqual(clima.fecha, '2026-01-02T12:00')


if __name__ == '__main__':
    unittest.main()
