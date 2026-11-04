from dominio.empleado  import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto

emp = Empleado ("juanito", "juanito@ecotech.cl", "La Serena", "+56958789625", 100.0000)

dpto = Departamento ("Recursos Humanos", "Javier Ahumada") 

proyecto = Proyecto ("Ecotech", "creando clases en python")


print(emp.mostrar_datos())
print(dpto.mostrar_datos())
print(proyecto.mostrar_datos())