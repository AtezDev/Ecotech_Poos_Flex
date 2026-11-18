import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from persistencia.creacion_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


class TestCrud(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        crear_tablas()
        self.fecha = date(2026, 11, 17)

    def tearDown(self):
        self.tmp.cleanup()

    def empleado(self):
        e = Empleado('Ana Torres', 'La Serena', '+56912345678', 'ana@ecotech.cl', self.fecha, 950000)
        return EmpleadoDAO.insertar(e)

    def proyecto(self, nombre='EcoTech'):
        return ProyectoDAO.insertar(Proyecto(nombre, 'Gestión de empleados', self.fecha))

    def departamento(self, nombre='Desarrollo'):
        return DepartamentoDAO.insertar(Departamento(nombre, 'Javier Ahumada'))

    def gestion(self, *lineas):
        entrada = '\n'.join(lineas) + '\n'
        return subprocess.run([sys.executable, str(ROOT / 'src/main.py')],
                              cwd=self.tmp.name, env=os.environ.copy(), input=entrada,
                              capture_output=True, text=True)

    def test_01_empleado_actualiza_todos_los_datos(self):
        e = self.empleado()
        self.assertTrue(e.cambiarNombre('Ana María Torres'))
        self.assertTrue(e.cambiarDireccion('Coquimbo 123'))
        self.assertTrue(e.cambiarTelefono('987654321'))
        self.assertTrue(e.cambiarSalario(1200000))
        self.assertEqual(EmpleadoDAO.actualizar(e), 1)
        g = EmpleadoDAO.buscar_por_id(e.id)
        self.assertEqual((g.nombre, g.direccion, g.telefono, g.salario),
                         ('Ana María Torres', 'Coquimbo 123', '987654321', 1200000.0))
        self.assertEqual(g.correoElectronico, 'ana@ecotech.cl')

    def test_02_empleado_actualizar_inexistente(self):
        e = self.empleado()
        e.id = e.id
        otro = Empleado('Luis', 'Calle 1', '+56911112222', 'l@ecotech.cl', self.fecha, 1, id=999)
        self.assertEqual(EmpleadoDAO.actualizar(otro), 0)

    def test_03_menu_empleado_actualiza_direccion_telefono_nombre_salario(self):
        e = self.empleado()
        r = self.gestion('1', '6', str(e.id), 'Coquimbo 123',
                         '7', str(e.id), 'abc', '987654321',
                         '8', str(e.id), 'Ana Perez',
                         '9', str(e.id), 'xx', '1200000.50', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Teléfono inválido:', r.stdout)
        self.assertIn('Salario inválido:', r.stdout)
        g = EmpleadoDAO.buscar_por_id(e.id)
        self.assertEqual((g.nombre, g.direccion, g.telefono, g.salario),
                         ('Ana Perez', 'Coquimbo 123', '987654321', 1200000.5))

    def test_04_menu_valor_igual_no_cambia(self):
        e = self.empleado()
        r = self.gestion('1', '6', str(e.id), 'La Serena', '0', '0')
        self.assertIn('El valor es el mismo; no hay cambios.', r.stdout)

    def test_05_menu_id_inexistente(self):
        r = self.gestion('1', '7', '999', '0', '0')
        self.assertIn('No existe empleado con ese ID.', r.stdout)

    def test_06_departamento_crud_dao(self):
        self.assertEqual(DepartamentoDAO.listar(), [])
        d = self.departamento()
        self.assertEqual(DepartamentoDAO.buscar_por_id(d.id).nombre, 'Desarrollo')
        self.assertIsNone(DepartamentoDAO.buscar_por_id(999))
        d.cambiarNombre('Operaciones')
        d.cambiarGerente('Marta Rojas')
        self.assertEqual(DepartamentoDAO.actualizar(d), 1)
        g = DepartamentoDAO.buscar_por_id(d.id)
        self.assertEqual((g.nombre, g.gerente), ('Operaciones', 'Marta Rojas'))
        self.assertEqual(DepartamentoDAO.eliminar(d.id), 1)
        self.assertEqual(DepartamentoDAO.eliminar(d.id), 0)

    def test_07_departamento_con_empleados_no_se_elimina(self):
        d = self.departamento()
        e = self.empleado()
        DepartamentoDAO.asignar_empleado(e.id, d.id)
        with self.assertRaises(sqlite3.IntegrityError):
            DepartamentoDAO.eliminar(d.id)
        self.assertIsNotNone(DepartamentoDAO.buscar_por_id(d.id))

    def test_08_empleado_cambia_de_departamento(self):
        a = self.departamento('A')
        b = self.departamento('B')
        e = self.empleado()
        self.assertEqual(DepartamentoDAO.asignar_empleado(e.id, a.id), 1)
        self.assertEqual(DepartamentoDAO.listar_empleados(a.id), [e.id])
        DepartamentoDAO.asignar_empleado(e.id, b.id)
        self.assertEqual(DepartamentoDAO.listar_empleados(a.id), [])
        self.assertEqual(DepartamentoDAO.listar_empleados(b.id), [e.id])
        self.assertEqual(DepartamentoDAO.quitar_empleado(e.id), 1)
        self.assertEqual(DepartamentoDAO.listar_empleados(b.id), [])

    def test_09_departamento_inexistente_rechazado_por_fk(self):
        e = self.empleado()
        with self.assertRaises(sqlite3.IntegrityError):
            DepartamentoDAO.asignar_empleado(e.id, 999)

    def test_10_proyecto_crud_dao(self):
        self.assertEqual(ProyectoDAO.listar(), [])
        p = self.proyecto()
        self.assertEqual(ProyectoDAO.buscar_por_id(p.id).fechaInicio, self.fecha)
        self.assertIsNone(ProyectoDAO.buscar_por_id(999))
        p.cambiarNombre('EcoTech 2')
        p.cambiarDescripcion('Nueva descripción')
        p.cambiarFechaInicio(date(2026, 12, 1))
        self.assertEqual(ProyectoDAO.actualizar(p), 1)
        g = ProyectoDAO.buscar_por_id(p.id)
        self.assertEqual((g.nombre, g.descripcion, g.fechaInicio),
                         ('EcoTech 2', 'Nueva descripción', date(2026, 12, 1)))
        self.assertEqual(len(ProyectoDAO.listar()), 1)
        self.assertEqual(ProyectoDAO.eliminar(p.id), 1)
        self.assertEqual(ProyectoDAO.eliminar(p.id), 0)

    def test_11_proyecto_asignado_no_se_elimina(self):
        e = self.empleado()
        p = self.proyecto()
        EmpleadoProyectoDAO.asignar(e, p)
        with self.assertRaises(sqlite3.IntegrityError):
            ProyectoDAO.eliminar(p.id)

    def test_12_desasignar_y_asignar_otro_proyecto(self):
        e = self.empleado()
        p1 = self.proyecto('Uno')
        p2 = self.proyecto('Dos')
        EmpleadoProyectoDAO.asignar(e, p1)
        self.assertTrue(EmpleadoProyectoDAO.desasignar(e, p1))
        self.assertFalse(EmpleadoProyectoDAO.desasignar(e, p1))
        self.assertTrue(EmpleadoProyectoDAO.asignar(e, p2))
        self.assertEqual(EmpleadoProyectoDAO.listar_por_empleado(e.id), [p2.id])
        self.assertEqual(ProyectoDAO.eliminar(p1.id), 1)

    def test_13_desasignar_con_registro_de_tiempo_rechazado(self):
        e = self.empleado()
        p = self.proyecto()
        EmpleadoProyectoDAO.asignar(e, p)
        r = RegistroTiempo(self.fecha, 2, 'Diseño')
        r.registrarTiempo(self.fecha, 2, 'Diseño', e, p)
        RegistroTiempoDAO.insertar(r)
        with self.assertRaises(sqlite3.IntegrityError):
            EmpleadoProyectoDAO.desasignar(e, p)

    def test_14_registro_crud_dao(self):
        e = self.empleado()
        p = self.proyecto()
        EmpleadoProyectoDAO.asignar(e, p)
        r = RegistroTiempo(self.fecha, 3.5, 'Diseño')
        r.registrarTiempo(self.fecha, 3.5, 'Diseño', e, p)
        RegistroTiempoDAO.insertar(r)
        g = RegistroTiempoDAO.buscar_por_id(r.id)
        self.assertEqual((g.horasTrabajadas, g.empleado.id, g.proyecto.id), (3.5, e.id, p.id))
        g.cambiarFecha(date(2026, 11, 18))
        g.cambiarHorasTrabajadas(4)
        g.cambiarDescripcionTarea('Pruebas')
        self.assertEqual(RegistroTiempoDAO.actualizar(g), 1)
        h = RegistroTiempoDAO.listar()[0]
        self.assertEqual((h.fecha, h.horasTrabajadas, h.descripcionTarea),
                         (date(2026, 11, 18), 4.0, 'Pruebas'))
        self.assertEqual(RegistroTiempoDAO.eliminar(r.id), 1)
        self.assertEqual(RegistroTiempoDAO.listar(), [])
        self.assertIsNone(RegistroTiempoDAO.buscar_por_id(r.id))

    def test_15_menu_departamentos_flujo_completo(self):
        r = self.gestion('2', '1', 'Desarrollo', '', 'Javier Ahumada',
                         '2', '3', '1', '4', '1', 'Operaciones', '5', '1', 'Marta Rojas',
                         '6', '1', 'n', '6', '1', 's', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Gerente inválido:', r.stdout)
        self.assertIn('Departamento registrado. ID: 1', r.stdout)
        self.assertIn('Nombre actualizado correctamente.', r.stdout)
        self.assertIn('Gerente actualizado correctamente.', r.stdout)
        self.assertIn('Eliminación cancelada.', r.stdout)
        self.assertIn('Eliminado correctamente.', r.stdout)
        self.assertEqual(DepartamentoDAO.listar(), [])

    def test_16_menu_proyectos_flujo_completo(self):
        r = self.gestion('3', '1', 'EcoTech', 'Gestión', '2026-02-30', '2026-11-17',
                         '2', '4', '1', 'EcoTech 2', '5', '1', 'Otra descripción',
                         '6', '1', '2026-12-01', '7', '1', 's', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Fecha de inicio (AAAA-MM-DD) inválido:', r.stdout)
        self.assertIn('Proyecto registrado. ID: 1', r.stdout)
        self.assertIn('Fecha de inicio (AAAA-MM-DD) actualizado correctamente.', r.stdout)
        self.assertEqual(ProyectoDAO.listar(), [])

    def test_17_menu_asignaciones_y_cambio_de_proyecto(self):
        e = self.empleado()
        p1 = self.proyecto('Uno')
        p2 = self.proyecto('Dos')
        d = self.departamento()
        r = self.gestion('4', '1', str(e.id), str(p1.id), '1', str(e.id), str(p1.id),
                         '3', str(e.id), '2', str(e.id), str(p1.id),
                         '1', str(e.id), str(p2.id), '4', str(p2.id),
                         '5', str(e.id), str(d.id), '5', str(e.id), str(d.id),
                         '7', str(d.id), '6', str(e.id), '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Empleado asignado al proyecto.', r.stdout)
        self.assertIn('El empleado ya estaba asignado a ese proyecto.', r.stdout)
        self.assertIn('Empleado quitado del proyecto.', r.stdout)
        self.assertIn('Empleado asignado al departamento.', r.stdout)
        self.assertIn('El empleado ya pertenece a ese departamento.', r.stdout)
        self.assertIn('Empleado sin departamento.', r.stdout)
        self.assertEqual(EmpleadoProyectoDAO.listar_por_empleado(e.id), [p2.id])
        self.assertEqual(DepartamentoDAO.listar_empleados(d.id), [])

    def test_18_menu_quitar_con_registros_muestra_error(self):
        e = self.empleado()
        p = self.proyecto()
        EmpleadoProyectoDAO.asignar(e, p)
        r = self.gestion('5', '1', str(e.id), str(p.id), '2026-11-17', '2', 'Diseño',
                         '0', '4', '2', str(e.id), str(p.id), '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Registro de tiempo guardado. ID: 1', r.stdout)
        self.assertIn('tiene registros de tiempo', r.stdout)
        self.assertEqual(EmpleadoProyectoDAO.listar_por_empleado(e.id), [p.id])

    def test_19_menu_registro_sin_asignacion_rechazado(self):
        e = self.empleado()
        p = self.proyecto()
        r = self.gestion('5', '1', str(e.id), str(p.id), '2026-11-17', '2', 'Diseño', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('El empleado no está asignado al proyecto.', r.stdout)
        self.assertEqual(RegistroTiempoDAO.listar(), [])

    def test_20_menu_registros_actualizar_y_eliminar(self):
        e = self.empleado()
        p = self.proyecto()
        EmpleadoProyectoDAO.asignar(e, p)
        r = self.gestion('5', '1', str(e.id), str(p.id), '2026-11-17', '0', '2', 'Diseño',
                         '5', '1', 'abc', '4', '6', '1', 'Pruebas',
                         '4', '1', '2026-11-18', '7', '1', 's', '0', '0')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('Horas inválido:', r.stdout)
        self.assertIn('Horas actualizado correctamente.', r.stdout)
        self.assertIn('Tarea actualizado correctamente.', r.stdout)
        self.assertIn('Fecha (AAAA-MM-DD) actualizado correctamente.', r.stdout)
        self.assertEqual(RegistroTiempoDAO.listar(), [])


if __name__ == '__main__':
    unittest.main()
