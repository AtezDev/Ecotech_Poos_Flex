import contextlib
import io
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from datetime import date
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import bcrypt
from dominio.empleado import Empleado
from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion
from persistencia.creacion_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.semillas import cargar_semillas
from persistencia.usuario_dao import UsuarioDAO
from presentacion import menu_usuario
from servicios.autenticacion import MAX_BYTES_BCRYPT, autenticar, crear_hash, registrar_usuario
import main as programa

CLAVE = 'Frase ficticia para clase'


def ejecutar(funcion, entradas, claves=()):
    salida = io.StringIO()
    with mock.patch('builtins.input', side_effect=list(entradas)), \
            mock.patch('presentacion.menu_usuario.getpass', side_effect=list(claves)), \
            contextlib.redirect_stdout(salida):
        resultado = funcion()
    return resultado, salida.getvalue()


class TestClase6(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        crear_tablas()
        self.fecha = date(2026, 11, 19)

    def tearDown(self):
        self.tmp.cleanup()

    def empleado(self, nombre='Ana Torres', correo='ana@ecotech.cl'):
        e = Empleado(nombre, 'La Serena', '+56912345678', correo, self.fecha, 950000)
        return EmpleadoDAO.insertar(e)

    def cuenta(self, nombre='ana.torres', clave=CLAVE):
        e = self.empleado()
        return e, registrar_usuario(e.id, nombre, clave)

    def contar(self, tabla):
        with closing(abrir_conexion()) as c:
            return c.execute(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]

    def test_01_usuario_normaliza_el_nombre(self):
        u = Usuario(' Ana.Torres ', 'hash', 7)
        self.assertEqual(u.nombre_usuario, 'ana.torres')
        self.assertEqual((u.empleado_id, u.id, u.password_hash), (7, None, 'hash'))
        self.assertEqual(Usuario.normalizar_usuario('ANA_1'), 'ana_1')

    def test_02_usuario_rechaza_nombres_invalidos(self):
        for malo in ['ab', 'a' * 41, 'ana torres', 'ana-torres', 'añ_1', '   ']:
            with self.assertRaises(ValueError, msg=repr(malo)):
                Usuario.normalizar_usuario(malo)
        for malo in [None, 5, ['ana']]:
            with self.assertRaises(TypeError, msg=repr(malo)):
                Usuario.normalizar_usuario(malo)

    def test_03_empleado_id_es_obligatorio_y_entero_positivo(self):
        for malo in [None, 0, -1, '1', 1.5, True]:
            with self.assertRaises(ValueError, msg=repr(malo)):
                Usuario('ana', 'hash', malo)

    def test_04_clave_conserva_espacios_y_mayusculas(self):
        clave = '  Clave Con Espacios Y MAYUSCULAS  '
        self.assertEqual(Usuario.validar_clave(clave), clave)
        with self.assertRaises(ValueError):
            Usuario.validar_clave('corta')
        with self.assertRaises(ValueError):
            Usuario.validar_clave('a' * (Usuario.MIN_CLAVE - 1))
        self.assertEqual(Usuario.validar_clave('a' * Usuario.MIN_CLAVE), 'a' * Usuario.MIN_CLAVE)
        for malo in [None, 123456789012345, b'x' * 20]:
            with self.assertRaises(TypeError, msg=repr(malo)):
                Usuario.validar_clave(malo)

    def test_05_hash_distinto_de_la_clave_y_con_sal(self):
        h1, h2 = crear_hash(CLAVE), crear_hash(CLAVE)
        self.assertNotEqual(h1, CLAVE)
        self.assertNotEqual(h1, h2)
        self.assertTrue(h1.startswith('$2'))
        self.assertTrue(bcrypt.checkpw(CLAVE.encode('utf-8'), h1.encode('utf-8')))
        self.assertTrue(bcrypt.checkpw(CLAVE.encode('utf-8'), h2.encode('utf-8')))
        self.assertFalse(bcrypt.checkpw(b'otra clave distinta', h1.encode('utf-8')))

    def test_06_limite_de_72_bytes_sin_recortar(self):
        self.assertTrue(crear_hash('a' * MAX_BYTES_BCRYPT).startswith('$2'))
        with self.assertRaises(ValueError):
            crear_hash('a' * (MAX_BYTES_BCRYPT + 1))
        acentuada = 'ñ' * 40
        self.assertEqual(len(acentuada), 40)
        self.assertGreater(len(acentuada.encode('utf-8')), MAX_BYTES_BCRYPT)
        with self.assertRaises(ValueError):
            crear_hash(acentuada)

    def test_07_registrar_guarda_el_hash_y_nunca_la_clave(self):
        e, u = self.cuenta()
        self.assertIsNotNone(u.id)
        with closing(abrir_conexion()) as c:
            fila = c.execute('SELECT * FROM usuario').fetchall()
        self.assertEqual(len(fila), 1)
        self.assertEqual((fila[0][1], fila[0][3]), ('ana.torres', e.id))
        self.assertTrue(fila[0][2].startswith('$2'))
        self.assertNotIn(CLAVE, [str(x) for x in fila[0]])
        with open(os.environ['DB_NAME'], 'rb') as f:
            self.assertNotIn(CLAVE.encode('utf-8'), f.read())

    def test_08_registrar_normaliza_y_valida(self):
        e = self.empleado()
        self.assertEqual(registrar_usuario(e.id, '  ANA.Torres ', CLAVE).nombre_usuario, 'ana.torres')
        e2 = self.empleado('Luis Soto', 'luis@ecotech.cl')
        with self.assertRaises(ValueError):
            registrar_usuario(e2.id, 'ab', CLAVE)
        with self.assertRaises(ValueError):
            registrar_usuario(e2.id, 'luis.soto', 'corta')
        with self.assertRaises(TypeError):
            registrar_usuario(e2.id, 'luis.soto', None)
        with self.assertRaises(ValueError):
            registrar_usuario(e2.id, 'luis.soto', 'a' * 73)
        self.assertEqual(self.contar('usuario'), 1)

    def test_09_registrar_exige_un_empleado_existente(self):
        for malo in [999, 0, -5, '1', None]:
            with self.assertRaises(ValueError, msg=repr(malo)):
                registrar_usuario(malo, 'ana.torres', CLAVE)
        self.assertEqual(self.contar('usuario'), 0)

    def test_10_no_se_duplican_usuario_ni_empleado(self):
        e, _ = self.cuenta()
        otro = self.empleado('Luis Soto', 'luis@ecotech.cl')
        with self.assertRaises(sqlite3.IntegrityError):
            registrar_usuario(otro.id, 'ANA.TORRES', CLAVE)
        with self.assertRaises(sqlite3.IntegrityError):
            registrar_usuario(e.id, 'otro.nombre', CLAVE)
        self.assertEqual(self.contar('usuario'), 1)

    def test_11_restricciones_de_la_bd(self):
        e = self.empleado()
        with closing(abrir_conexion()) as c:
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) VALUES ('x1x', 'h', 999)")
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) VALUES ('x1x', NULL, ?)", (e.id,))
            c.execute("INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) VALUES ('x1x', 'h', ?)", (e.id,))
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) VALUES ('x1x', 'h', ?)", (e.id,))

    def test_12_dao_buscar_por_nombre(self):
        self.assertIsNone(UsuarioDAO.buscar_por_nombre('nadie'))
        e, u = self.cuenta()
        b = UsuarioDAO.buscar_por_nombre('ana.torres')
        self.assertEqual((b.id, b.nombre_usuario, b.empleado_id), (u.id, 'ana.torres', e.id))
        self.assertIsNot(b, u)
        with self.assertRaises(ValueError):
            UsuarioDAO.insertar(b)

    def test_13_autenticar_acceso_correcto(self):
        e, u = self.cuenta()
        cuenta = autenticar('ana.torres', CLAVE)
        self.assertIsInstance(cuenta, Usuario)
        self.assertEqual((cuenta.id, cuenta.empleado_id, cuenta.nombre_usuario), (u.id, e.id, 'ana.torres'))
        self.assertIsNotNone(autenticar('  ANA.TORRES ', CLAVE))

    def test_14_autenticar_rechaza_sin_romper(self):
        self.cuenta()
        casos = [('ana.torres', 'otra clave distinta larga'), ('ana.torres', CLAVE.upper()),
                 ('ana.torres', CLAVE + ' '), ('ana.torres', ''), ('ana.torres', None),
                 ('ana.torres', 12345), ('ana.torres', 'a' * 73), ('nadie.existe', CLAVE)]
        for nombre, clave in casos:
            self.assertIsNone(autenticar(nombre, clave), msg=repr((nombre, clave)))
        for nombre in ['ab', 'ana torres']:
            with self.assertRaises(ValueError):
                autenticar(nombre, CLAVE)
        with self.assertRaises(TypeError):
            autenticar(None, CLAVE)

    def test_15_el_servicio_no_imprime_ni_pide_datos(self):
        self.cuenta()
        salida = io.StringIO()
        with mock.patch('builtins.input', side_effect=AssertionError('input no permitido')), \
                contextlib.redirect_stdout(salida):
            autenticar('ana.torres', CLAVE)
            autenticar('ana.torres', 'incorrecta incorrecta')
            autenticar('nadie.existe', CLAVE)
        self.assertEqual(salida.getvalue(), '')

    def test_16_login_correcto_incorrecto_e_inexistente(self):
        self.cuenta()
        u, texto = ejecutar(menu_usuario.solicitar_login, ['ana.torres'], [CLAVE])
        self.assertEqual(u.nombre_usuario, 'ana.torres')
        self.assertIn('Sesión iniciada correctamente.', texto)
        u, t1 = ejecutar(menu_usuario.solicitar_login, ['ana.torres'], ['clave incorrecta larga'])
        self.assertIsNone(u)
        u, t2 = ejecutar(menu_usuario.solicitar_login, ['nadie.existe'], [CLAVE])
        self.assertIsNone(u)
        self.assertEqual(t1, t2)
        self.assertIn('Usuario o contraseña incorrectos.', t1)
        self.assertNotIn('nadie.existe', t2)

    def test_17_login_con_dato_invalido(self):
        u, texto = ejecutar(menu_usuario.solicitar_login, ['ab'], [CLAVE])
        self.assertIsNone(u)
        self.assertIn('No se pudo validar el acceso.', texto)

    def test_18_fallo_de_la_bd_no_da_acceso(self):
        self.cuenta()
        with closing(abrir_conexion()) as c:
            c.execute('DROP TABLE usuario')
            c.commit()
        with self.assertRaises(sqlite3.OperationalError):
            autenticar('ana.torres', CLAVE)
        u, texto = ejecutar(menu_usuario.solicitar_login, ['ana.torres'], [CLAVE])
        self.assertIsNone(u)
        self.assertIn('No se pudo verificar el acceso.', texto)
        self.assertNotIn('Sesión iniciada', texto)
        u, texto = ejecutar(menu_usuario.menu_acceso, ['1', 'ana.torres', '0'], [CLAVE])
        self.assertIsNone(u)

    def test_19_tres_intentos_y_se_cierra(self):
        self.cuenta()
        u, texto = ejecutar(menu_usuario.menu_acceso, ['1', 'ana.torres'] * 3 + ['1', 'ana.torres'],
                            ['mala mala mala mala'] * 3 + [CLAVE])
        self.assertIsNone(u)
        self.assertEqual(texto.count('Usuario o contraseña incorrectos.'), 3)
        self.assertIn('Demasiados intentos', texto)

    def test_20_acceso_correcto_tras_un_error(self):
        self.cuenta()
        u, texto = ejecutar(menu_usuario.menu_acceso, ['1', 'ana.torres', '1', 'ana.torres'],
                            ['mala mala mala mala', CLAVE])
        self.assertEqual(u.nombre_usuario, 'ana.torres')

    def test_21_opciones_del_menu_de_acceso(self):
        u, texto = ejecutar(menu_usuario.menu_acceso, ['9', '0'])
        self.assertIsNone(u)
        self.assertIn('Elige una opción entre 0 y 3.', texto)
        self.assertIn('Saliendo de EcoTech.', texto)

    def test_22_crear_cuenta_desde_el_menu(self):
        e = self.empleado()
        u, texto = ejecutar(menu_usuario.registrar_cuenta,
                            [str(e.id), ' Ana.Torres '], ['corta', CLAVE, 'distinta distinta distinta', CLAVE, CLAVE])
        self.assertIn('Contraseña inválida:', texto)
        self.assertIn('Las contraseñas no coinciden.', texto)
        self.assertIn('Cuenta creada para el usuario: ana.torres', texto)
        self.assertIsNotNone(autenticar('ana.torres', CLAVE))
        self.assertNotIn(CLAVE, texto)

    def test_23_crear_cuenta_rechazos_con_mensaje(self):
        e = self.empleado()
        otro = self.empleado('Luis Soto', 'luis@ecotech.cl')
        ejecutar(menu_usuario.registrar_cuenta, [str(e.id), 'ana.torres'], [CLAVE, CLAVE])
        _, t = ejecutar(menu_usuario.registrar_cuenta, [str(otro.id), 'ana.torres'], [CLAVE, CLAVE])
        self.assertIn('ya tienen una cuenta', t)
        _, t = ejecutar(menu_usuario.registrar_cuenta, [str(e.id), 'otra.cuenta'], [CLAVE, CLAVE])
        self.assertIn('ya tienen una cuenta', t)
        _, t = ejecutar(menu_usuario.registrar_cuenta, ['999', 'fantasma'], [CLAVE, CLAVE])
        self.assertIn('No existe un empleado con ese ID.', t)
        _, t = ejecutar(menu_usuario.registrar_cuenta, [str(otro.id), 'ab'], [CLAVE, CLAVE])
        self.assertIn('Usuario fuera del largo permitido.', t)
        _, t = ejecutar(menu_usuario.registrar_cuenta, [str(otro.id), 'luis.soto'], ['a' * 80, 'a' * 80])
        self.assertIn('Máximo 72 bytes UTF-8 para bcrypt.', t)
        self.assertEqual(self.contar('usuario'), 1)

    def test_24_semillas_desde_el_menu_de_acceso(self):
        _, texto = ejecutar(menu_usuario.menu_acceso, ['3', '3', '0'])
        self.assertIn('Semillas cargadas: 2 departamentos y 3 empleados nuevos.', texto)
        self.assertIn('ya estaban cargadas', texto)
        self.assertEqual((self.contar('departamento'), self.contar('empleado')), (2, 3))

    def test_25_semillas_no_tocan_las_cuentas(self):
        cargar_semillas()
        ana = EmpleadoDAO.listar()[0]
        registrar_usuario(ana.id, 'ana.torres', CLAVE)
        cargar_semillas()
        self.assertEqual(self.contar('usuario'), 1)
        self.assertIsNotNone(autenticar('ana.torres', CLAVE))

    def test_26_empleado_vinculado_sin_mostrar_el_hash(self):
        e, u = self.cuenta()
        ok, texto = ejecutar(lambda: menu_usuario.mostrar_empleado_vinculado(u), [])
        self.assertTrue(ok)
        self.assertIn('Empleado: Ana Torres | ana@ecotech.cl', texto)
        self.assertNotIn(u.password_hash, texto)
        self.assertNotIn('$2', texto)

    def test_27_empleado_vinculado_irrecuperable(self):
        e, u = self.cuenta()
        with mock.patch('presentacion.menu_usuario.EmpleadoDAO.buscar_por_id', return_value=None):
            ok, texto = ejecutar(lambda: menu_usuario.mostrar_empleado_vinculado(u), [])
        self.assertFalse(ok)
        self.assertIn('No se pudo recuperar el empleado vinculado', texto)

    def correr_main(self, entradas, claves=(), argv=('main.py',)):
        with mock.patch.object(sys, 'argv', list(argv)):
            return ejecutar(programa.main, entradas, claves)

    def test_28_main_no_abre_el_menu_sin_cuenta_valida(self):
        self.cuenta()
        _, texto = self.correr_main(['1', 'ana.torres'] * 3, ['mala mala mala mala'] * 3)
        self.assertNotIn('ECOTECH SOLUTIONS', texto)
        self.assertNotIn('Sesión:', texto)

    def test_29_main_abre_el_menu_con_cuenta_valida(self):
        self.cuenta()
        _, texto = self.correr_main(['1', 'ana.torres', '0'], [CLAVE])
        self.assertIn('Sesión: ana.torres', texto)
        self.assertIn('Empleado: Ana Torres | ana@ecotech.cl', texto)
        self.assertIn('=== ECOTECH SOLUTIONS ===', texto)
        self.assertNotIn(CLAVE, texto)

    def test_30_main_con_fallo_de_la_bd_no_abre_el_menu(self):
        self.cuenta()
        with closing(abrir_conexion()) as c:
            c.execute('DROP TABLE usuario')
            c.commit()
        with mock.patch('persistencia.creacion_bd.crear_tablas'), \
                mock.patch('main.crear_tablas'):
            _, texto = self.correr_main(['1', 'ana.torres', '0'], [CLAVE])
        self.assertIn('No se pudo verificar el acceso.', texto)
        self.assertNotIn('ECOTECH SOLUTIONS', texto)

    def test_31_main_no_abre_el_menu_si_falta_el_empleado_vinculado(self):
        self.cuenta()
        with mock.patch('presentacion.menu_usuario.EmpleadoDAO.buscar_por_id', return_value=None):
            _, texto = self.correr_main(['1', 'ana.torres', '0'], [CLAVE])
        self.assertIn('Sesión: ana.torres', texto)
        self.assertIn('No se pudo recuperar el empleado vinculado', texto)
        self.assertNotIn('ECOTECH SOLUTIONS', texto)

    def test_32_flujo_completo_semillas_cuenta_login_y_reportes(self):
        entradas = ['3', '2', '2', 'luis.soto', '1', 'luis.soto', '1', '12', '1', '0', '0']
        claves = [CLAVE, CLAVE, CLAVE]
        _, texto = self.correr_main(entradas, claves)
        self.assertIn('Cuenta creada para el usuario: luis.soto', texto)
        self.assertIn('Sesión: luis.soto', texto)
        self.assertIn('Empleado: Luis Soto | luis.soto@ecotech.cl', texto)
        self.assertIn('Reporte general', texto)
        self.assertIn('Departamento: Soporte', texto)

    def test_33_cuenta_persistida_tras_reiniciar_otro_proceso(self):
        self.cuenta()
        codigo = ("import sys; sys.path.insert(0, r'%s');"
                  "from servicios.autenticacion import autenticar;"
                  "a = autenticar('ana.torres', %r); b = autenticar('ana.torres', 'clave mala mala mala');"
                  "print(a.nombre_usuario, b)" % (ROOT / 'src', CLAVE))
        r = subprocess.run([sys.executable, '-c', codigo], cwd=self.tmp.name,
                           env=os.environ.copy(), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), 'ana.torres None')

    def test_34_la_tabla_usuario_se_agrega_a_una_base_anterior(self):
        with closing(abrir_conexion()) as c:
            c.execute('DROP TABLE usuario')
            c.commit()
        crear_tablas()
        crear_tablas()
        self.cuenta()
        self.assertEqual(self.contar('usuario'), 1)

    def test_35_requirements_conserva_las_librerias_y_agrega_bcrypt(self):
        lineas = (ROOT / 'requirements.txt').read_text(encoding='utf-8').split()
        for libreria in ['PyMySQL', 'python-dotenv', 'bcrypt']:
            self.assertIn(libreria, lineas)

    def test_36_el_empleado_con_cuenta_no_se_puede_borrar(self):
        e, _ = self.cuenta()
        with self.assertRaises(sqlite3.IntegrityError):
            EmpleadoDAO.eliminar(e.id)


if __name__ == '__main__':
    unittest.main()
