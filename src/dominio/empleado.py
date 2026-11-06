# Clase Empleado

class Empleado:
    def __init__(self, nombre: str, correo: str, direccion: str, telefono: str, salario: float, id = None):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.salario = salario
        self.id = id

    def mostrar_datos(self) -> str:
        return f" nombre: {self.nombre} correo: {self.correo} direccion: {self.direccion} telefono: {self.telefono} salario: {self.salario} id: {self.id}"
    
