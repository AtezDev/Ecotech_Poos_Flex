import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

COMANDO_MENU = [sys.executable, '-c',
                "import sys; sys.path.insert(0, r'%s'); "
                "from presentacion.menu_principal import menu_principal; menu_principal()"
                % (ROOT / 'src')]

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.reporte import ReporteEmpleados, ReportePorDepartamento
from persistencia.creacion_bd import crear_tablas
from persistencia.conexion import abrir_conexion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.semillas import cargar_semillas, buscar_id_empleado, buscar_id_departamento


class TestClase5(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        crear_tablas()
        self.fecha = date(2026, 11, 17)

    def tearDown(self):
        self.tmp.cleanup()

    def empleado(self, nombre='Ana Torres', correo='ana@ecotech.cl'):
        e = Empleado(nombre, 'La Serena', '+56912345678', correo, self.fecha, 950000)
        return EmpleadoDAO.insertar(e)

    def departamento(self, nombre='Soporte', gerente=None):
        return DepartamentoDAO.insertar(Departamento(nombre, gerente))

    def menu(self, *lineas):
        entrada = '\n'.join(lineas) + '\n'
        return subprocess.run(COMANDO_MENU,
                              cwd=self.tmp.name, env=os.environ.copy(), input=entrada,
                              capture_output=True, text=True)

    def test_01_constructor_acepta_empleado_o_vacio(self):
        self.assertIsNone(Departamento('Soporte').gerente)
        self.assertIsNone(Departamento('Soporte', None).gerente)
        e = self.empleado()
        self.assertIs(Departamento('Soporte', e).gerente, e)

    def test_02_constructor_rechaza_texto_y_numeros(self):
        for malo in ['2', 'Javier Ahumada', '', 2, 2.5, ['x']]:
            with self.assertRaises(ValueError, msg=repr(malo)):
                Departamento('Soporte', malo)

    def test_03_cambiar_gerente(self):
        e = self.empleado()
        d = Departamento('Soporte')
        self.assertFalse(d.cambiarGerente('2'))
        self.assertIsNone(d.gerente)
        self.assertTrue(d.cambiarGerente(e))
        self.assertIs(d.gerente, e)
        self.assertFalse(d.cambiarGerente('Marta Rojas'))
        self.assertIs(d.gerente, e)
        self.assertTrue(d.cambiarGerente(None))
        self.assertIsNone(d.gerente)

    def test_04_gerente_sin_guardar_no_se_inserta(self):
        sin_guardar = Empleado('Luis Soto', 'X 1', '+56911112222', 'l@ecotech.cl', self.fecha, 1)
        with self.assertRaises(ValueError):
            DepartamentoDAO.insertar(Departamento('Soporte', sin_guardar))
        self.assertEqual(DepartamentoDAO.listar(), [])

    def test_05_guardar_y_recuperar_gerente(self):
        e = self.empleado()
        d = self.departamento('Soporte', e)
        g = DepartamentoDAO.buscar_por_id(d.id)
        self.assertEqual((g.gerente.id, g.gerente.nombre), (e.id, 'Ana Torres'))
        self.assertIn('Gerente: Ana Torres (ID 1)', DepartamentoDAO.listar()[0].mostrar_datos())
        sin = self.departamento('Ventas')
        self.assertIsNone(DepartamentoDAO.buscar_por_id(sin.id).gerente)
        self.assertIn('Gerente: Sin gerente', DepartamentoDAO.buscar_por_id(sin.id).mostrar_datos())

    def test_06_menu_pide_id_con_lista_y_reintento(self):
        e = self.empleado()
        r = self.menu('2', '1', 'Soporte', 'abc', '99', str(e.id), '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('El gerente es un empleado ya registrado', r.stdout)
        self.assertIn('1: Ana Torres', r.stdout)
        self.assertIn('Escribe solo el número de ID', r.stdout)
        self.assertIn('No existe ningún empleado con ese ID', r.stdout)
        self.assertIn('Departamento registrado. ID: 1', r.stdout)
        self.assertEqual(DepartamentoDAO.listar()[0].gerente.id, e.id)

    def test_07_menu_asignar_cambiar_y_quitar_gerente(self):
        e1 = self.empleado()
        e2 = self.empleado('Luis Soto', 'luis@ecotech.cl')
        d = self.departamento()
        r = self.menu('2', '5', str(d.id), str(e2.id),
                      '5', str(d.id), str(e2.id),
                      '5', str(d.id), '', '0', '0')
        self.assertEqual(r.stdout.count('Gerente actualizado correctamente.'), 2)
        self.assertIn('El valor es el mismo; no hay cambios.', r.stdout)
        self.assertIsNone(DepartamentoDAO.buscar_por_id(d.id).gerente)
        self.assertEqual(e1.id, 1)

    def test_21_sin_empleados_el_departamento_queda_sin_gerente(self):
        r = self.menu('2', '1', 'Soporte', '0', '0')
        self.assertIn('quedará sin gerente', r.stdout)
        self.assertIn('Departamento registrado. ID: 1', r.stdout)
        self.assertIsNone(DepartamentoDAO.listar()[0].gerente)

    def test_22_la_bd_rechaza_gerente_inexistente_y_empleado_gerente_no_se_borra(self):
        with closing(abrir_conexion()) as c:
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO departamento (nombre, gerente_id) VALUES ('X', 999)")
        e = self.empleado()
        self.departamento('Soporte', e)
        with self.assertRaises(sqlite3.IntegrityError):
            EmpleadoDAO.eliminar(e.id)
        r = self.menu('1', '5', str(e.id), 's', '0', '0')
        self.assertIn('No se puede eliminar', r.stdout)
        self.assertIsNotNone(EmpleadoDAO.buscar_por_id(e.id))

    def test_23_departamento_con_empleados_trae_su_gerente(self):
        g = self.empleado()
        m = self.empleado('Luis Soto', 'luis@ecotech.cl')
        d = self.departamento('Soporte', g)
        d.agregar_empleado(m)
        EmpleadoDAO.actualizar_departamento(m)
        r = DepartamentoDAO.buscar_con_empleados(d.id)
        self.assertEqual(r.gerente.nombre, 'Ana Torres')
        self.assertEqual([x.nombre for x in r.empleados], ['Luis Soto'])
        self.assertIn('Departamento: Soporte', ReportePorDepartamento(r).generar())

    def test_08_empleado_sin_departamento(self):
        e = self.empleado()
        g = EmpleadoDAO.buscar_por_id(e.id)
        self.assertIsNone(g.departamento)
        self.assertIn('Departamento: Sin departamento', g.mostrar_datos())
        self.assertIn('Departamento: Sin departamento', EmpleadoDAO.listar()[0].mostrar_datos())

    def test_09_actualizar_departamento_y_recuperar(self):
        e = self.empleado()
        d = self.departamento()
        self.assertTrue(d.agregar_empleado(e))
        self.assertEqual(EmpleadoDAO.actualizar_departamento(e), 1)
        g = EmpleadoDAO.buscar_por_id(e.id)
        self.assertEqual((g.departamento.id, g.departamento.nombre), (d.id, 'Soporte'))
        self.assertIn('Departamento: Soporte (ID 1)', g.mostrar_datos())
        self.assertIn('Departamento: Soporte (ID 1)', EmpleadoDAO.listar()[0].mostrar_datos())

    def test_10_quitar_departamento(self):
        e = self.empleado()
        d = self.departamento()
        d.agregar_empleado(e)
        EmpleadoDAO.actualizar_departamento(e)
        g = EmpleadoDAO.buscar_por_id(e.id)
        g.departamento = None
        self.assertEqual(EmpleadoDAO.actualizar_departamento(g), 1)
        self.assertIsNone(EmpleadoDAO.buscar_por_id(e.id).departamento)

    def test_11_actualizar_departamento_exige_guardados(self):
        e = self.empleado()
        sin_guardar = Departamento('Nuevo')
        sin_guardar.agregar_empleado(e)
        with self.assertRaises(ValueError):
            EmpleadoDAO.actualizar_departamento(e)
        with self.assertRaises(ValueError):
            EmpleadoDAO.actualizar_departamento(Empleado('Luis', 'X 1', '+56911112222', 'l@ecotech.cl', self.fecha, 1))

    def test_12_departamento_inexistente_rechazado_por_fk(self):
        e = self.empleado()
        fantasma = Departamento('Fantasma', id=999)
        fantasma.agregar_empleado(e)
        with self.assertRaises(sqlite3.IntegrityError):
            EmpleadoDAO.actualizar_departamento(e)

    def test_13_buscar_con_empleados(self):
        d = self.departamento()
        a = self.empleado('Ana Torres', 'ana@ecotech.cl')
        b = self.empleado('Luis Perez', 'luis@ecotech.cl')
        self.empleado('Sin Depto', 'sin@ecotech.cl')
        for e in (a, b):
            d.agregar_empleado(e)
            EmpleadoDAO.actualizar_departamento(e)
        r = DepartamentoDAO.buscar_con_empleados(d.id)
        self.assertEqual([e.nombre for e in r.empleados], ['Ana Torres', 'Luis Perez'])
        self.assertTrue(all(e.departamento is r for e in r.empleados))

    def test_14_ausente_y_vacio_son_distintos(self):
        d = self.departamento()
        self.assertIsNone(DepartamentoDAO.buscar_con_empleados(999))
        vacio = DepartamentoDAO.buscar_con_empleados(d.id)
        self.assertIsNotNone(vacio)
        self.assertEqual(vacio.empleados, ())

    def test_15_reportes_polimorfismo(self):
        d = self.departamento()
        a = self.empleado('Ana Torres', 'ana@ecotech.cl')
        self.empleado('Luis Perez', 'luis@ecotech.cl')
        d.agregar_empleado(a)
        EmpleadoDAO.actualizar_departamento(a)
        reportes = [ReporteEmpleados(EmpleadoDAO.listar()),
                    ReportePorDepartamento(DepartamentoDAO.buscar_con_empleados(d.id))]
        textos = [r.generar() for r in reportes]
        self.assertIn('Reporte general', textos[0])
        self.assertIn('Luis Perez | luis@ecotech.cl | Sin departamento', textos[0])
        self.assertIn('Ana Torres | ana@ecotech.cl | Soporte', textos[0])
        self.assertIn('Departamento: Soporte', textos[1])
        self.assertIn('Ana Torres', textos[1])
        self.assertNotIn('Luis Perez', textos[1])
        self.assertTrue(isinstance(reportes[1], ReporteEmpleados))

    def test_16_reporte_departamento_vacio(self):
        d = self.departamento()
        t = ReportePorDepartamento(DepartamentoDAO.buscar_con_empleados(d.id)).generar()
        self.assertIn('Sin empleados.', t)

    def test_17_menu_asignar_y_recuperar_tras_reiniciar(self):
        e = self.empleado()
        d = self.departamento()
        r1 = self.menu('1', '10', str(e.id), str(d.id), '0', '0')
        self.assertEqual(r1.returncode, 0, r1.stderr)
        self.assertIn('Asignación guardada.', r1.stdout)
        r2 = self.menu('1', '3', str(e.id), '11', str(d.id), '0', '0')
        self.assertIn('Departamento: Soporte (ID 1)', r2.stdout)
        self.assertIn('1: Ana Torres', r2.stdout)

    def test_18_menu_asignar_mismo_y_cambiar_de_departamento(self):
        e = self.empleado()
        a = self.departamento('Soporte')
        b = self.departamento('Ventas')
        r = self.menu('1', '10', str(e.id), str(a.id), '10', str(e.id), str(a.id),
                      '10', str(e.id), str(b.id), '0', '0')
        self.assertIn('El empleado ya pertenece a ese departamento.', r.stdout)
        self.assertEqual(r.stdout.count('Asignación guardada.'), 2)
        g = EmpleadoDAO.buscar_por_id(e.id)
        self.assertEqual(g.departamento.nombre, 'Ventas')
        self.assertEqual(DepartamentoDAO.listar_empleados(a.id), [])

    def test_19_menu_casos_borde_asignar_y_mostrar(self):
        r = self.menu('1', '10', '999', '11', '999', '0', '0')
        self.assertIn('No existe ese empleado.', r.stdout)
        self.assertIn('No existe ese departamento.', r.stdout)
        d = self.departamento()
        r = self.menu('1', '11', str(d.id), '0', '0')
        self.assertIn('Este departamento no tiene empleados.', r.stdout)
        e = self.empleado()
        r = self.menu('1', '10', str(e.id), '999', '0', '0')
        self.assertIn('No existe ese departamento.', r.stdout)

    def test_20_menu_reportes(self):
        e = self.empleado()
        d = self.departamento()
        EmpleadoDAO.actualizar_departamento(self._con_dep(e, d))
        r = self.menu('1', '12', str(d.id), '12', '999', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Reporte general', r.stdout)
        self.assertIn('Departamento: Soporte', r.stdout)
        self.assertIn('No existe ese departamento.', r.stdout)
        self.assertEqual(r.stdout.count('Reporte general'), 1)

    def _con_dep(self, empleado, departamento):
        departamento.agregar_empleado(empleado)
        return empleado

    def test_24_propiedad_departamento_valida_la_referencia(self):
        e = self.empleado()
        with self.assertRaises(ValueError):
            e.departamento = 'Soporte'
        with self.assertRaises(ValueError):
            e.departamento = 5
        d = Departamento('Soporte')
        e.departamento = d
        self.assertIs(e.departamento, d)
        e.departamento = None
        self.assertIsNone(e.departamento)

    def test_25_lab1_relacion_en_memoria(self):
        d = Departamento('Soporte')
        a = Empleado('Ana Torres', 'La Serena', '+56912345678', 'ana@ecotech.cl', self.fecha, 1)
        b = Empleado('Luis Soto', 'La Serena', '+56912345679', 'luis@ecotech.cl', self.fecha, 1)
        d.agregar_empleado(a)
        d.agregar_empleado(b)
        d.agregar_empleado(a)
        self.assertEqual([x.nombre for x in d.empleados], ['Ana Torres', 'Luis Soto'])
        self.assertEqual(d.cantidad_empleados(), 2)
        self.assertIs(a.departamento, d)

    def contar(self, tabla):
        with closing(abrir_conexion()) as c:
            return c.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]

    def test_26_semillas_dos_ejecuciones_sin_duplicados(self):
        self.assertEqual(cargar_semillas(), (2, 3))
        self.assertEqual((self.contar('departamento'), self.contar('empleado')), (2, 3))
        self.assertEqual(cargar_semillas(), (0, 0))
        self.assertEqual((self.contar('departamento'), self.contar('empleado')), (2, 3))

    def test_27_semillas_relaciones_y_recuperacion(self):
        cargar_semillas()
        soporte = DepartamentoDAO.buscar_con_empleados(buscar_id_departamento('Soporte'))
        self.assertEqual(sorted(x.nombre for x in soporte.empleados), ['Ana Torres', 'Luis Soto'])
        self.assertEqual(soporte.gerente.nombre, 'Ana Torres')
        desarrollo = DepartamentoDAO.buscar_con_empleados(buscar_id_departamento('Desarrollo'))
        self.assertEqual([x.nombre for x in desarrollo.empleados], ['María Pérez'])
        self.assertEqual(desarrollo.gerente.nombre, 'María Pérez')
        ana = EmpleadoDAO.buscar_por_id(buscar_id_empleado('ana.torres@ecotech.cl'))
        self.assertEqual(ana.departamento.nombre, 'Soporte')

    def test_28_semillas_no_pisan_cambios_posteriores(self):
        cargar_semillas()
        luis = EmpleadoDAO.buscar_por_id(buscar_id_empleado('luis.soto@ecotech.cl'))
        desarrollo = DepartamentoDAO.buscar_por_id(buscar_id_departamento('Desarrollo'))
        luis.departamento.reasignarEmpleado(luis, desarrollo)
        EmpleadoDAO.actualizar_departamento(luis)
        cargar_semillas()
        luis = EmpleadoDAO.buscar_por_id(buscar_id_empleado('luis.soto@ecotech.cl'))
        self.assertEqual(luis.departamento.nombre, 'Desarrollo')

    def test_29_semillas_completan_solo_lo_que_falta(self):
        self.empleado('Ana Torres', 'ana.torres@ecotech.cl')
        self.assertEqual(cargar_semillas(), (2, 2))
        self.assertEqual(self.contar('empleado'), 3)

    def test_30_menu_semillas_dos_veces(self):
        r = self.menu('6', '6', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Semillas cargadas: 2 departamentos y 3 empleados nuevos.', r.stdout)
        self.assertIn('Las semillas ya estaban cargadas; no se duplicó ningún dato.', r.stdout)
        self.assertEqual((self.contar('departamento'), self.contar('empleado')), (2, 3))


if __name__ == '__main__':
    unittest.main()
