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

from dominio.clima import Clima
from persistencia.clima_dao import ClimaDAO
from persistencia.creacion_bd import crear_tablas
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from presentacion.menu_principal import menu_principal
from servicios.api_clima import URL_CLIMA, extraer_clima
from servicios.api_clima import consultar_api_clima
from servicios.autenticacion import autenticar, crear_cuenta
from servicios.clima import consultar_clima

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_LUIS = 'Clave de Luis para prueba 2026'
JSON_CLIMA = {'current': {'time': '2026-11-26T00:00', 'temperature_2m': 18.4,
                          'relative_humidity_2m': 62, 'weather_code': 2}}


class TestClima(unittest.TestCase):
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

    def test_01_ciudad_y_rangos_se_validan(self):
        with self.assertRaises(ValueError):
            Clima.validar_ciudad('A')
        with self.assertRaises(ValueError):
            Clima.validar_ciudad('La Serena; DROP')
        with self.assertRaises(ValueError):
            Clima('La Serena', '2026-11-26T00:00', 18, 120, 'Nublado')
        with self.assertRaises(TypeError):
            Clima('La Serena', '2026-11-26T00:00', '18', 60, 'Nublado')

    def test_02_extraer_clima_con_json_ficticio(self):
        clima = extraer_clima(JSON_CLIMA, 'La Serena')
        self.assertEqual(clima.temperatura, 18.4)
        self.assertEqual(clima.humedad, 62.0)
        self.assertEqual(clima.estado, 'Parcialmente nublado')

    def test_03_extraer_rechaza_respuesta_incompleta(self):
        with self.assertRaises(ValueError):
            extraer_clima({}, 'La Serena')
        with self.assertRaises(ValueError):
            extraer_clima({'current': {'time': 'x', 'weather_code': 'x'}}, 'La Serena')

    def test_04_consulta_usa_espera_acotada(self):
        respuesta = mock.Mock(status_code=200)
        respuesta.json.return_value = JSON_CLIMA
        with mock.patch('servicios.api_clima.requests.get', return_value=respuesta) as get:
            consultar_api_clima(-29.9, -71.2)
        self.assertEqual(get.call_args.args[0], URL_CLIMA)
        self.assertEqual(get.call_args.kwargs['timeout'], (3, 5))

    def test_05_consulta_guarda_y_respalda(self):
        with mock.patch('servicios.clima.consultar_api_clima', return_value=JSON_CLIMA):
            clima, origen = consultar_clima(self.luis, 'La Serena', -29.9, -71.2)
        self.assertEqual(origen, 'api')
        with mock.patch('servicios.clima.consultar_api_clima',
                        side_effect=requests.ConnectionError('sin red')):
            respaldo, origen = consultar_clima(self.luis, 'La Serena', -29.9, -71.2)
        self.assertEqual(origen, 'respaldo')
        self.assertEqual(respaldo.temperatura, 18.4)

    def test_06_sin_sesion_no_consulta(self):
        with mock.patch('servicios.clima.consultar_api_clima') as api:
            with self.assertRaises(PermissionError):
                consultar_clima(None, 'La Serena', -29.9, -71.2)
        api.assert_not_called()

    def test_07_coordenadas_fuera_de_rango_no_llaman_a_la_api(self):
        with mock.patch('servicios.clima.consultar_api_clima') as api:
            with self.assertRaises(ValueError):
                consultar_clima(self.luis, 'La Serena', 95, -71.2)
        api.assert_not_called()

    def test_08_menu_empleado_consulta_clima_con_respaldo_vacio(self):
        salida = io.StringIO()
        entradas = ['2', '3', 'La Serena', '-29.9', '-71.2', '0', '0']
        with mock.patch('builtins.input', side_effect=entradas), \
                mock.patch('servicios.clima.consultar_api_clima',
                           side_effect=requests.ConnectionError('sin red')), \
                contextlib.redirect_stdout(salida):
            menu_principal(self.luis)
        texto = salida.getvalue()
        self.assertIn('No hay información de clima disponible', texto)


if __name__ == '__main__':
    unittest.main()
