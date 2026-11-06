from dominio.empleado  import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo

# emp = Empleado ("juanito", "juanito@ecotech.cl", "La Serena", "+56958789625", 100.0000, )

# dpto = Departamento ("Recursos Humanos", "Javier Ahumada") 

# proyecto = Proyecto ("Ecotech", "creando clases en python")

# registro = RegistroTiempo ("2026-11-05", )


# print(emp.mostrar_datos())
# print(dpto.mostrar_datos())
# print(proyecto.mostrar_datos())

from persistencia.creacion_bd import  crear_tablas
crear_tablas()