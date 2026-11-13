from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO




def menu_empleados():
    while True:
        print("\n1. Registrar\n2. Listar\n0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "0":
            break
        else:
            print("Elige 0, 1 o 2.")

def crear_empleado():
    nombre = solicitar("Nombre", Empleado.validar_nombre) #solicitar_nombre()
    direccion = solicitar("Direccion", )
    correo = solicitar("Correo",Empleado.validar_correo) #solicitar_correo()
    telefono
    empleado = Empleado(nombre=nombre, direccion=direccion, telefono=telefono, correoElectronico=correo, fechaInicioContrato=FechaContrato, salario=salario)
    EmpleadoDAO.insertar(empleado)
    print(f"Empleado registrado. ID: {empleado.id}")

"""
def solicitar_nombre():
    while True:
        valor = input("Nombre: ")
        try:
            return Empleado.validar_nombre(valor)
        except ValueError as error:
            print(f"Nombre inválido: {error}")
            

def solicitar_correo():
    while True:
        valor = input("Correo: ")
        try:
            return Empleado.validar_correo(valor)
        except ValueError as error:
            print(f"Correo Invalido: {error}")

def solicitar_id():
    while True:
        texto = input("ID del empleado: ").strip()
        try:
            id_empleado = int(texto)
            if id_empleado <= 0:
                raise ValueError("El ID debe ser positivo.")
        except ValueError:
            print("Ingresa un entero mayor que 0.")
        else:
            return id_empleado

""" 

def solicitar(text_input:str, validador):
    while True:
        valor = input(f"{text_input}: ")
        try:
            return validador(valor)
        except ValueError as error:
            print(f"{text_input} Invalido: {error}")

