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

from dominio.indicador import Indicador
from dominio.usuario import Usuario
from persistencia.creacion_bd import crear_tablas
from persistencia.indicador_dao import IndicadorDAO
from persistencia.semillas import asegurar_admin_inicial, cargar_semillas
from persistencia.usuario_dao import UsuarioDAO
from presentacion.menu_principal import menu_principal
from servicios.api_indicadores import URL_INDICADORES, extraer_primero
from servicios.api_indicadores import consultar_api
from servicios.autenticacion import autenticar, crear_cuenta
from servicios.indicadores import actualizar_uf, consultar_uf_guardada
from servicios.permisos import exigir_admin, exigir_sesion

CLAVE_ADMIN = 'Clave admin de prueba 2026!'
CLAVE_LUIS = 'Clave de Luis para prueba 2026'
JSON_FICTICIO = {
    'status': 'success',
    'data': {
        'dolar': {'date': '2026-01-05', 'value': 900.5},
        'uf': {'date': '2026-01-05', 'value': 40000.0},
        'euro': {'date': '2026-01-05', 'value': 950.25},
        'utm': {'date': '2026-01-01', 'value': 70000},
        'ipc': {'date': '2026-01-01', 'value': 0.3},
    },
}


def ejecutar(funcion, entradas=()):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            contextlib.redirect_stdout(salida):
        funcion()
    return salida.getvalue()


class TestUnidad3(unittest.TestCase):
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

    def filas_indicador(self):
        with closing(sqlite3.connect(os.environ['DB_NAME'])) as conexion:
            return conexion.execute('SELECT COUNT(*) FROM indicador').fetchone()[0]

    # Roles
    def test_01_rol_por_defecto_es_empleado(self):
        usuario = Usuario('ana.torres', 'hash', 1)
        self.assertEqual(usuario.rol, 'empleado')
        self.assertFalse(usuario.es_admin)

    def test_02_rol_invalido_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, 'Rol de usuario no válido.'):
            Usuario('ana.torres', 'hash', 1, rol='gerente')

    def test_03_rol_se_guarda_y_se_lee(self):
        leido = UsuarioDAO.buscar_por_nombre('luis.soto')
        self.assertEqual(leido.rol, 'empleado')
        self.assertEqual(self.admin.rol, 'admin')
        self.assertTrue(self.admin.es_admin)

    def test_04_cambio_de_rol_persiste(self):
        leido = UsuarioDAO.buscar_por_nombre('luis.soto')
        leido.rol = 'admin'
        UsuarioDAO.actualizar(leido)
        self.assertEqual(UsuarioDAO.buscar_por_id(leido.id).rol, 'admin')

    def test_05_permisos_por_rol(self):
        with self.assertRaisesRegex(PermissionError, 'Inicie sesión.'):
            exigir_sesion(None)
        with self.assertRaisesRegex(PermissionError, 'Acción solo para administrador.'):
            exigir_admin(self.luis)
        exigir_admin(self.admin)

    def test_06_migracion_agrega_rol_a_base_antigua(self):
        ruta = Path(self.tmp.name) / 'antigua.db'
        with closing(sqlite3.connect(ruta)) as conexion:
            conexion.execute("""CREATE TABLE usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                empleado_id INTEGER NOT NULL UNIQUE)""")
            conexion.execute("INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) "
                             "VALUES ('admin', 'h', 1), ('luis.soto', 'h', 2)")
            conexion.commit()
        os.environ['DB_NAME'] = str(ruta)
        crear_tablas()
        crear_tablas()
        with closing(sqlite3.connect(ruta)) as conexion:
            columnas = {fila[1] for fila in conexion.execute('PRAGMA table_info(usuario)')}
            roles = dict(conexion.execute('SELECT nombre_usuario, rol FROM usuario'))
        self.assertIn('rol', columnas)
        self.assertEqual(roles, {'admin': 'admin', 'luis.soto': 'empleado'})

    # Adaptador JSON -> Indicador
    def test_07_indicador_valida_datos(self):
        indicador = Indicador('uf', '2026-01-05', 40000)
        self.assertEqual((indicador.codigo, indicador.fecha, indicador.valor),
                         ('UF', '2026-01-05', 40000.0))
        with self.assertRaises(ValueError):
            Indicador('xyz', '2026-01-05', 1)
        with self.assertRaises(ValueError):
            Indicador('UF', '05-01-2026', 1)
        with self.assertRaises(ValueError):
            Indicador('UF', '2026-01-05', 0)
        with self.assertRaises(TypeError):
            Indicador('UF', '2026-01-05', 'abc')
        with self.assertRaises(TypeError):
            Indicador('UF', '2026-01-05', True)

    def test_08_extraer_primero_con_json_ficticio(self):
        indicador = extraer_primero(JSON_FICTICIO)
        self.assertEqual(indicador.codigo, 'UF')
        self.assertEqual(indicador.fecha, '2026-01-05')
        self.assertEqual(indicador.valor, 40000.0)

    def test_09_extraer_primero_rechaza_estructura_incompleta(self):
        for datos in ({}, {'status': 'error'}, {'status': 'success', 'data': {'uf': {'date': '2026-01-05'}}}):
            with self.subTest(datos=datos):
                with self.assertRaises((ValueError, TypeError)):
                    extraer_primero(datos)

    # Cliente HTTP con espera acotada y fallas simuladas
    def test_10_consulta_usa_espera_acotada(self):
        respuesta = mock.Mock()
        respuesta.json.return_value = JSON_FICTICIO
        with mock.patch('servicios.api_indicadores.requests.get', return_value=respuesta) as get:
            self.assertEqual(consultar_api(), JSON_FICTICIO)
        get.assert_called_once_with(URL_INDICADORES, timeout=(3, 5))
        respuesta.raise_for_status.assert_called_once()

    def test_11_error_http_se_propaga_al_servicio(self):
        respuesta = mock.Mock()
        respuesta.raise_for_status.side_effect = requests.HTTPError('503')
        with mock.patch('servicios.api_indicadores.requests.get', return_value=respuesta):
            with self.assertRaises(requests.HTTPError):
                consultar_api()

    # Servicio: API, respaldo y permisos
    def test_12_admin_actualiza_uf_y_queda_persistida(self):
        with mock.patch('servicios.indicadores.consultar_api', return_value=JSON_FICTICIO):
            indicador, origen = actualizar_uf(self.admin)
        self.assertEqual(origen, 'api')
        self.assertEqual(indicador.fecha, '2026-01-05')
        guardado = consultar_uf_guardada(self.luis)
        self.assertEqual((guardado.codigo, guardado.fecha, guardado.valor),
                         ('UF', '2026-01-05', 40000.0))

    def test_13_empleado_no_actualiza_y_no_escribe(self):
        antes = self.filas_indicador()
        with mock.patch('servicios.indicadores.consultar_api') as api:
            with self.assertRaisesRegex(PermissionError, 'Acción solo para administrador.'):
                actualizar_uf(self.luis)
        api.assert_not_called()
        self.assertEqual(self.filas_indicador(), antes)

    def test_14_falla_api_usa_respaldo_guardado(self):
        IndicadorDAO.guardar(Indicador('UF', '2026-01-02', 39900))
        with mock.patch('servicios.indicadores.consultar_api',
                        side_effect=requests.ConnectionError('sin red')):
            indicador, origen = actualizar_uf(self.admin)
        self.assertEqual(origen, 'respaldo')
        self.assertEqual((indicador.fecha, indicador.valor), ('2026-01-02', 39900.0))

    def test_15_falla_api_sin_respaldo_no_inventa_dato(self):
        with mock.patch('servicios.indicadores.consultar_api',
                        side_effect=requests.Timeout('lento')):
            indicador, origen = actualizar_uf(self.admin)
        self.assertIsNone(indicador)
        self.assertEqual(origen, 'respaldo')
        self.assertEqual(self.filas_indicador(), 0)

    def test_16_mismo_codigo_y_fecha_una_sola_fila(self):
        IndicadorDAO.guardar(Indicador('UF', '2026-01-05', 40000))
        IndicadorDAO.guardar(Indicador('UF', '2026-01-05', 40100))
        self.assertEqual(self.filas_indicador(), 1)
        self.assertEqual(IndicadorDAO.ultimo('UF').valor, 40100.0)

    # Menús según rol
    def test_17_menu_empleado_ficha_y_sin_actualizar(self):
        salida = ejecutar(lambda: menu_principal(self.luis), ['1', '2', '2', '0', '0'])
        self.assertIn('Luis Soto', salida)
        self.assertIn('Acción solo para administrador.', salida)
        self.assertNotIn('Administrar usuarios', salida)

    def test_18_menu_admin_actualiza_con_api_simulada(self):
        with mock.patch('servicios.indicadores.consultar_api', return_value=JSON_FICTICIO):
            salida = ejecutar(lambda: menu_principal(self.admin), ['9', '2', '0', '0'])
        self.assertIn('Código: UF | Fecha: 2026-01-05 | Valor: 40000.0', salida)
        self.assertIn('Origen: API', salida)

    def test_19_menu_admin_sin_api_ni_respaldo_informa(self):
        with mock.patch('servicios.indicadores.consultar_api',
                        side_effect=requests.ConnectionError('sin red')):
            salida = ejecutar(lambda: menu_principal(self.admin), ['9', '2', '0', '0'])
        self.assertIn('No hay información disponible para UF.', salida)


if __name__ == '__main__':
    unittest.main()
