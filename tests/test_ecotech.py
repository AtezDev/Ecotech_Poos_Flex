import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from persistencia.creacion_bd import crear_tablas
from persistencia.conexion import abrir_conexion, obtener_motor
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


class TestEcoTech(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['DB_ENGINE'] = 'sqlite'
        os.environ['DB_NAME'] = str(Path(self.tmp.name) / 'ecotech.db')
        crear_tablas()
        self.fecha = date(2026, 11, 11)

    def tearDown(self):
        self.tmp.cleanup()

    def empleado(self, nombre='Ana Torres', correo='ana@ecotech.cl'):
        return Empleado(nombre, 'La Serena', '+56912345678', correo, self.fecha, 950000)

    def proyecto(self):
        return Proyecto('EcoTech', 'Gestión de empleados', self.fecha)

    def test_01_motor_sqlite(self):
        self.assertEqual(obtener_motor(), 'sqlite')

    def test_02_tables_created(self):
        with closing(abrir_conexion()) as c:
            tables = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({'empleado', 'departamento', 'proyecto', 'empleado_proyecto', 'registro_tiempo'} <= tables)

    def test_03_valid_employee(self):
        e=self.empleado('  Ana Torres  ',' ana@ecotech.cl ')
        self.assertEqual((e.nombre,e.correoElectronico,e.id),('Ana Torres','ana@ecotech.cl',None))
        self.assertEqual(e.obtenerFechaInicioContrato(),self.fecha)

    def test_04_name_apostrophe(self):
        self.assertEqual(self.empleado("D'Ávila").nombre,"D'Ávila")

    def test_05_name_boundaries(self):
        self.assertEqual(len(self.empleado('A'*80).nombre),80)
        self.assertEqual(self.empleado('Ab').nombre,'Ab')
        for name in (' ','A','B'*81,34):
            with self.subTest(name=name), self.assertRaises(ValueError):self.empleado(name)

    def test_06_email_invalid(self):
        for email in ('ana@','ana @ecotech.cl','ana@@ecotech.cl','@example.com','ana@site.','ana@.site','ana@example..com','xx',42):
            with self.subTest(email=email),self.assertRaises(ValueError):self.empleado(correo=email)

    def test_07_email_valid_boundary(self):
        self.assertEqual(self.empleado(correo='a@b.c').correoElectronico,'a@b.c')
        long_email='a'*(150-len('@site.cl'))+'@site.cl'
        self.assertEqual(len(self.empleado(correo=long_email).correoElectronico),150)
        with self.assertRaises(ValueError):self.empleado(correo=long_email+'a')

    def test_08_invalid_setter_preserves_value(self):
        e=self.empleado()
        for val in (' ','A'):
            with self.assertRaises(ValueError):e.nombre=val
        with self.assertRaises(ValueError):e.correoElectronico='ana@'
        self.assertEqual((e.nombre,e.correoElectronico),('Ana Torres','ana@ecotech.cl'))
        self.assertFalse(e.cambiarNombre(' '))
        self.assertFalse(e.cambiarCorreoElectronico('ana@'))

    def test_09_date_types(self):
        for value in ('2026-11-11', datetime(2026,11,11),None):
            with self.subTest(value=value),self.assertRaises(ValueError):
                Empleado('Ana','La Serena','123','ana@site.cl',value,10)
        with self.assertRaises(ValueError): Proyecto('Eco','ok',datetime(2026,11,11))
        with self.assertRaises(ValueError): RegistroTiempo(datetime(2026,11,11),1,'Tarea')

    def test_10_salary_validation(self):
        for bad in (-1,'100',True,float('nan'),float('inf'),float('-inf')):
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                Empleado('Ana','La Serena','123','ana@site.cl',self.fecha,bad)
        self.assertEqual(self.empleado().salario,950000.0)

    def test_11_department_unique(self):
        d1=Departamento('Desarrollo','Javier')
        d2=Departamento('RRHH','Karla')
        e=self.empleado()
        self.assertTrue(d1.asignarEmpleado(e))
        self.assertFalse(d1.asignarEmpleado(e))
        self.assertFalse(d2.asignarEmpleado(e))
        self.assertIs(e.departamento,d1)
        self.assertEqual(d1.cantidad_empleados(),1)

    def test_12_department_transfer(self):
        d1=Departamento('Desarrollo','Javier')
        d2=Departamento('RRHH','Karla')
        e=self.empleado()
        d1.asignarEmpleado(e)
        self.assertTrue(d1.reasignarEmpleado(e,d2))
        self.assertEqual(d1.cantidad_empleados(),0)
        self.assertEqual(d2.cantidad_empleados(),1)
        self.assertIs(e.departamento,d2)

    def test_13_departments_and_projects_validate(self):
        with self.assertRaises(ValueError):Departamento('  ','J')
        with self.assertRaises(ValueError):Proyecto(' ','Desc',self.fecha)
        d=Departamento('Ventas','Javier')
        self.assertFalse(d.cambiarNombre(''))
        p=self.proyecto()
        self.assertTrue(p.cambiarDescripcion('Mejorada'))
        self.assertFalse(p.cambiarFechaInicio('2026-11-11'))

    def test_14_record_validates(self):
        for h in (0,-2,True,'dos'):
            with self.subTest(h=h),self.assertRaises(ValueError):RegistroTiempo(self.fecha,h,'Tarea')
        self.assertFalse(RegistroTiempo(self.fecha,1,'Tarea').registrarTiempo(self.fecha,1,'Tarea','No es Empleado',self.proyecto()))

    def test_15_insert_ids(self):
        d=Departamento('Desarrollo','Javier')
        p=self.proyecto()
        e=self.empleado()
        self.assertIsNone(e.id)
        DepartamentoDAO.insertar(d);ProyectoDAO.insertar(p);EmpleadoDAO.insertar(e,d)
        self.assertTrue(all(isinstance(x.id,int) and x.id>0 for x in (d,p,e)))
        with closing(abrir_conexion()) as conn:
            self.assertEqual(conn.execute('SELECT departamento_id FROM empleado WHERE id=?',(e.id,)).fetchone()[0],d.id)

    def test_16_id_immutable_after_insert(self):
        e=self.empleado();EmpleadoDAO.insertar(e)
        with self.assertRaises(ValueError):e.id=e.id+1
        self.assertEqual(e.obtenerIdEmpleado(),1)

    def test_17_reinsert_rejected(self):
        e=self.empleado();EmpleadoDAO.insertar(e)
        with self.assertRaises(ValueError):EmpleadoDAO.insertar(e)
        self.assertEqual(len(EmpleadoDAO.listar()),1)

    def test_18_list_empty(self):
        self.assertEqual(EmpleadoDAO.listar(),[])

    def test_19_list_reconstitutes(self):
        e=self.empleado();EmpleadoDAO.insertar(e)
        vals=EmpleadoDAO.listar()
        self.assertEqual(len(vals),1)
        self.assertEqual(vals[0].fechaInicioContrato,self.fecha)
        self.assertEqual(vals[0].id,e.id)
        self.assertIsInstance(vals[0],Empleado)

    def test_20_search_found_absent(self):
        e=self.empleado();EmpleadoDAO.insertar(e)
        self.assertEqual(EmpleadoDAO.buscar_por_id(e.id).nombre,e.nombre)
        self.assertIsNone(EmpleadoDAO.buscar_por_id(-1))
        self.assertIsNone(EmpleadoDAO.buscar_por_id('1 OR 1=1'))

    def test_21_relation_multiple_projects(self):
        e=self.empleado();EmpleadoDAO.insertar(e)
        p1=self.proyecto();p2=Proyecto('Proyecto 2','Otro',self.fecha)
        ProyectoDAO.insertar(p1);ProyectoDAO.insertar(p2)
        self.assertTrue(e.asignarAProyecto(p1))
        self.assertFalse(e.asignarAProyecto(p1))
        self.assertFalse(e.asignarAProyecto('un proyecto'))
        self.assertTrue(EmpleadoProyectoDAO.asignar(e,p1))
        self.assertTrue(EmpleadoProyectoDAO.asignar(e,p2))
        self.assertFalse(EmpleadoProyectoDAO.asignar(e,p1))
        self.assertEqual(EmpleadoProyectoDAO.listar_por_empleado(e.id),[p1.id,p2.id])
        self.assertEqual(EmpleadoProyectoDAO.listar_por_proyecto(p1.id),[e.id])

    def test_22_relation_multiple_employees(self):
        p=self.proyecto();ProyectoDAO.insertar(p)
        e1=self.empleado();e2=self.empleado('Ana B','b@site.cl')
        EmpleadoDAO.insertar(e1);EmpleadoDAO.insertar(e2)
        EmpleadoProyectoDAO.asignar(e1,p);EmpleadoProyectoDAO.asignar(e2,p)
        self.assertEqual(EmpleadoProyectoDAO.listar_por_proyecto(p.id),[e1.id,e2.id])

    def test_23_record_persisted_with_relation(self):
        e=self.empleado();p=self.proyecto()
        EmpleadoDAO.insertar(e);ProyectoDAO.insertar(p)
        EmpleadoProyectoDAO.asignar(e,p)
        r=RegistroTiempo(self.fecha,3.5,'Diseño')
        self.assertTrue(r.registrarTiempo(self.fecha,3.5,'Diseño',e,p))
        RegistroTiempoDAO.insertar(r)
        self.assertIsInstance(r.id,int)
        with closing(abrir_conexion()) as conn:
            row=conn.execute('SELECT fecha, horas_trabajadas, empleado_id, proyecto_id FROM registro_tiempo WHERE id=?',(r.id,)).fetchone()
        self.assertEqual(row,(self.fecha.isoformat(),3.5,e.id,p.id))

    def test_24_record_unassigned_rejected(self):
        e=self.empleado();p=self.proyecto()
        EmpleadoDAO.insertar(e);ProyectoDAO.insertar(p)
        r=RegistroTiempo(self.fecha,2,'Testing')
        r.registrarTiempo(self.fecha,2,'Testing',e,p)
        with self.assertRaises(ValueError):RegistroTiempoDAO.insertar(r)

    def test_25_fk_active(self):
        with closing(abrir_conexion()) as conn:
            self.assertEqual(conn.execute('PRAGMA foreign_keys').fetchone()[0],1)
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute('INSERT INTO empleado_proyecto (empleado_id, proyecto_id) VALUES (?,?)',(999,999))

    def test_26_composite_fk(self):
        e=self.empleado();p=self.proyecto();EmpleadoDAO.insertar(e);ProyectoDAO.insertar(p)
        with closing(abrir_conexion()) as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute('INSERT INTO registro_tiempo (fecha,horas_trabajadas,descripcion_tarea,empleado_id,proyecto_id) VALUES (?,?,?,?,?)',(self.fecha.isoformat(),2,'Tarea',e.id,p.id))

    def test_27_existing_old_employee_schema_guard(self):
        other=Path(self.tmp.name)/'old.db'
        with closing(sqlite3.connect(other)) as c:
            c.execute('CREATE TABLE empleado (id INTEGER PRIMARY KEY, nombre TEXT, correo TEXT)')
            c.execute("INSERT INTO empleado VALUES (1,'Juanito','juanito@ecotech.cl')")
            c.commit()
        os.environ['DB_NAME']=str(other)
        with self.assertRaisesRegex(ValueError,'esquema incompatible'):crear_tablas()
        with closing(sqlite3.connect(other)) as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM empleado').fetchone()[0],1)
            self.assertEqual(c.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='proyecto'").fetchone()[0],0)

    def test_28_existing_other_table_guard(self):
        other=Path(self.tmp.name)/'old2.db'
        with closing(sqlite3.connect(other)) as c:
            c.execute('CREATE TABLE proyecto (id INTEGER PRIMARY KEY,nombre TEXT)')
            c.commit()
        os.environ['DB_NAME']=str(other)
        with self.assertRaisesRegex(ValueError,'proyecto tiene un esquema incompatible'):crear_tablas()

    def test_29_repeat_create_tables(self):
        crear_tablas();crear_tablas()
        with closing(abrir_conexion()) as c:
            self.assertEqual(c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='empleado'").fetchone()[0],1)

    def test_30_run_main_and_read_only(self):
        env=os.environ.copy()
        a=subprocess.run([sys.executable,str(ROOT/'src/main.py')],cwd=self.tmp.name,env=env,capture_output=True,text=True)
        self.assertEqual(a.returncode,0,a.stderr)
        self.assertIn('Buscar inexistente: None',a.stdout)
        self.assertIn('Proyectos del empleado',a.stdout)
        b=subprocess.run([sys.executable,str(ROOT/'src/main.py'),'--listar'],cwd=self.tmp.name,env=env,capture_output=True,text=True)
        self.assertEqual(b.returncode,0,b.stderr)
        self.assertIn('Ana Torres',b.stdout)
        with closing(abrir_conexion()) as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM empleado').fetchone()[0],1)


if __name__=='__main__':unittest.main(verbosity=2)
