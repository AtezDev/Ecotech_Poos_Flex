# Clase departamento
from dominio.empleado import Empleado

class Departamento:
    def __init__(self, nombre: str, gerente: str ):
            self.nombre = nombre
            self.gerente = gerente
            self._empleados: list[Empleado] = []

    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False
        
        self._empleados.append(empleado)
        return True


    def mostrar_datos(self) -> str:
        return f" nombre: {self.nombre} gerente: {self.gerente}"