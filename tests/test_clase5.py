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

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.reporte import ReporteEmpleados, ReportePorDepartamento
from persistencia.creacion_bd import crear_tablas
from persistencia.conexion import abrir_conexion
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO


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

    def departamento(self, nombre='Soporte', gerente='Javier Ahumada'):
        return DepartamentoDAO.insertar(Departamento(nombre, gerente))

    def menu(self, *lineas):
        entrada = '\n'.join(lineas) + '\n'
        return subprocess.run([sys.executable, str(ROOT / 'src/main.py')],
                              cwd=self.tmp.name, env=os.environ.copy(), input=entrada,
                              capture_output=True, text=True)

    def test_01_gerente_valido(self):
        self.assertEqual(Departamento.validar_gerente('  Javier Ahumada '), 'Javier Ahumada')
        self.assertEqual(Departamento.validar_gerente("O'Higgins"), "O'Higgins")

    def test_02_gerente_invalido(self):
        for malo in ['2', '12345', 'Juan2', '', '   ', 'J', 'Ana@', 'x' * 81, None, 5]:
            with self.assertRaises(ValueError, msg=repr(malo)):
                Departamento.validar_gerente(malo)

    def test_03_constructor_rechaza_gerente_numerico(self):
        with self.assertRaises(ValueError):
            Departamento('Soporte', '2')

    def test_04_cambiar_gerente_invalido_conserva_valor(self):
        d = Departamento('Soporte', 'Javier Ahumada')
        self.assertFalse(d.cambiarGerente('2'))
        self.assertEqual(d.gerente, 'Javier Ahumada')
        self.assertTrue(d.cambiarGerente('Marta Rojas'))
        self.assertEqual(d.gerente, 'Marta Rojas')

    def test_05_dato_antiguo_en_bd_no_rompe_la_lectura(self):
        with closing(abrir_conexion()) as c:
            c.execute("INSERT INTO departamento (nombre, gerente) VALUES ('Antiguo', '2')")
            c.commit()
        self.assertEqual(DepartamentoDAO.listar()[0].gerente, '2')
        self.assertEqual(DepartamentoDAO.buscar_por_id(1).gerente, '2')

    def test_06_menu_pide_gerente_con_mensaje_y_reintento(self):
        r = self.menu('2', '1', 'Soporte', '2', 'Juan2', 'Javier Ahumada', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('El gerente es una persona', r.stdout)
        self.assertEqual(r.stdout.count('Gerente inválido:'), 2)
        self.assertIn('Departamento registrado. ID: 1', r.stdout)
        self.assertEqual(DepartamentoDAO.listar()[0].gerente, 'Javier Ahumada')

    def test_07_menu_actualizar_gerente_rechaza_numero(self):
        d = self.departamento()
        r = self.menu('2', '5', str(d.id), '2', 'Marta Rojas', '0', '0')
        self.assertIn('Gerente inválido:', r.stdout)
        self.assertIn('Gerente actualizado correctamente.', r.stdout)
        self.assertEqual(DepartamentoDAO.buscar_por_id(d.id).gerente, 'Marta Rojas')

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
        sin_guardar = Departamento('Nuevo', 'Javier Ahumada')
        sin_guardar.agregar_empleado(e)
        with self.assertRaises(ValueError):
            EmpleadoDAO.actualizar_departamento(e)
        with self.assertRaises(ValueError):
            EmpleadoDAO.actualizar_departamento(Empleado('Luis', 'X 1', '+56911112222', 'l@ecotech.cl', self.fecha, 1))

    def test_12_departamento_inexistente_rechazado_por_fk(self):
        e = self.empleado()
        fantasma = Departamento('Fantasma', 'Javier Ahumada', id=999)
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
        b = self.departamento('Ventas', 'Karla Perez')
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
        self.assertIn('No existe ese departamento; se muestra solo el reporte general.', r.stdout)

    def _con_dep(self, empleado, departamento):
        departamento.agregar_empleado(empleado)
        return empleado


if __name__ == '__main__':
    unittest.main()
