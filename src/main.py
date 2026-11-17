import sys
from datetime import date

from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from persistencia.creacion_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from presentacion.menu_empleado import listar_empleados, tipos_errores_bd
from presentacion.menu_principal import menu_principal


def demostrar_relaciones():
    # Demo de clases anteriores. Se ejecuta SOLO con --demo.
    # Conserva Departamento, Proyecto, asociación N:M y RegistroTiempo.
    departamento = Departamento("Desarrollo", "Javier Ahumada")
    DepartamentoDAO.insertar(departamento)

    proyecto = Proyecto("EcoTech", "Gestión de empleados", date(2026, 11, 10))
    ProyectoDAO.insertar(proyecto)

    empleado = Empleado("Ana Torres", "La Serena", "+56912345678",
                        "ana.torres@ecotech.cl", date(2026, 11, 10), 950000)
    departamento.agregar_empleado(empleado)
    EmpleadoDAO.insertar(empleado, departamento)
    print("Departamento:", departamento.mostrar_datos())
    print("Proyecto:", proyecto.mostrar_datos())
    print("Empleado:", empleado.mostrar_datos())

    # En objetos: referencia a Proyecto. En SQL: IDs en empleado_proyecto.
    empleado.asignarAProyecto(proyecto)
    guardada = EmpleadoProyectoDAO.asignar(empleado, proyecto)
    print("Asignación Empleado-Proyecto:", guardada)
    print("Proyectos del empleado:", EmpleadoProyectoDAO.listar_por_empleado(empleado.id))
    print("Empleados del proyecto:", EmpleadoProyectoDAO.listar_por_proyecto(proyecto.id))

    registro = RegistroTiempo(date(2026, 11, 10), 3.5, "Diseño del sistema")
    registro.registrarTiempo(registro.fecha, registro.horasTrabajadas,
                            registro.descripcionTarea, empleado, proyecto)
    RegistroTiempoDAO.insertar(registro)
    print("Registro:", registro.mostrar_datos())
    encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
    print("Buscar existente:", encontrado.mostrar_datos() if encontrado else None)
    print("Buscar inexistente:", EmpleadoDAO.buscar_por_id(-1))


def main():
    # main.py coordina: no hace validaciones de nombre ni escribe instrucciones SQL.
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] not in ("--demo", "--listar")):
        print("Uso: python src/main.py [--demo | --listar]")
        return

    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        crear_tablas()  # Primero deben existir las tablas.
    except ValueError as error:
        print("No se pudo preparar la base:", error)
        return
    except (IntegrityError, OperationalError) as error:
        print("No se pudo preparar la base de datos:", error)
        return

    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demostrar_relaciones()
    elif len(sys.argv) == 2 and sys.argv[1] == "--listar":
        listar_empleados()
    else:
        menu_principal()


if __name__ == "__main__":
    main()
