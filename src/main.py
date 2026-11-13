from datetime import date
import sys

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from persistencia.creacion_bd import crear_tablas
from persistencia.conexion import obtener_motor
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from presentacion.menu_empleado import menu_empleados


def main():
    try:
        crear_tablas()
    except ValueError as error:
        print("No se pudo preparar la base:", error)
        return
    menu_empleados()
"""
    print("Motor:", obtener_motor())

    if len(sys.argv) > 1 and sys.argv[1] not in ("--listar",):
        print("Uso: python src/main.py [--listar]")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--listar":
        empleados = EmpleadoDAO.listar()
        if not empleados:
            print("Todavía no hay empleados registrados.")
        for empleado in empleados:
            print(empleado.mostrar_datos())
        return

    departamento = Departamento("Desarrollo", "Javier Ahumada")
    DepartamentoDAO.insertar(departamento)
    print("Departamento:", departamento.mostrar_datos())

    proyecto = Proyecto("EcoTech", "Gestión de empleados", date(2026, 11, 10))
    ProyectoDAO.insertar(proyecto)
    print("Proyecto:", proyecto.mostrar_datos())

    empleado = Empleado(
        nombre="Ana Torres",
        direccion="La Serena",
        telefono="+56912345678",
        correoElectronico=" ana.torres@ecotech.cl ",
        fechaInicioContrato=date(2026, 11, 10),
        salario=950000.0
    )

    print("Empleado antes:", empleado.id)
    departamento.agregar_empleado(empleado)
    EmpleadoDAO.insertar(empleado, departamento)
    print("Empleado después:", empleado.id)

    empleado.asignarAProyecto(proyecto)
    asignacion_guardada = EmpleadoProyectoDAO.asignar(empleado, proyecto)
    print("Asignación Empleado-Proyecto:", asignacion_guardada)
    print("Proyectos del empleado:", EmpleadoProyectoDAO.listar_por_empleado(empleado.id))
    print("Empleados del proyecto:", EmpleadoProyectoDAO.listar_por_proyecto(proyecto.id))

    registro = RegistroTiempo(date(2026, 11, 10), 3.5, "Diseño del sistema")
    registro.registrarTiempo(registro.fecha, registro.horasTrabajadas,
                            registro.descripcionTarea, empleado, proyecto)
    RegistroTiempoDAO.insertar(registro)
    print("Registro:", registro.mostrar_datos())

    print("\nListado de empleados:")
    for item in EmpleadoDAO.listar():
        print(item.id, item.nombre, item.correoElectronico)

    encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
    print("\nBuscar existente:", encontrado.mostrar_datos() if encontrado else None)
    print("Buscar inexistente:", EmpleadoDAO.buscar_por_id(-1))

    print("\nPruebas de validación:")
    for nombre, correo in [(" ", "ana@ecotech.cl"), ("Ana Torres", "ana@")]:
        try:
            Empleado(nombre, "La Serena", "+56912345678", correo,
                     date(2026, 11, 10), 950000.0)
        except ValueError as error:
            print("Dato rechazado:", error)
"""

if __name__ == "__main__":
    main()
    
