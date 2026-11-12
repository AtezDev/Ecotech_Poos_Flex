from dominio.empleado import Empleado


class Departamento:
    def __init__(self, nombre: str, gerente: str, id=None):
        if not self.validarNombre(nombre):
            raise ValueError("El nombre del departamento es obligatorio.")
        if not isinstance(gerente, str) or not gerente.strip():
            raise ValueError("El gerente es obligatorio.")
        self.id = id
        self.nombre = nombre.strip()
        self.gerente = gerente.strip()
        self._empleados: list[Empleado] = []

    @staticmethod
    def validarNombre(nombre):
        return isinstance(nombre, str) and bool(nombre.strip())

    def obtenerNombre(self):
        return self.nombre

    def cambiarNombre(self, nuevoNombre):
        if not self.validarNombre(nuevoNombre):
            return False
        self.nombre = nuevoNombre.strip()
        return True

    def obtenerGerente(self):
        return self.gerente

    def cambiarGerente(self, nuevoGerente):
        if not isinstance(nuevoGerente, str) or not nuevoGerente.strip():
            return False
        self.gerente = nuevoGerente.strip()
        return True

    @property
    def empleados(self):
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado: Empleado):
        if not isinstance(empleado, Empleado) or empleado in self._empleados:
            return False
        self._empleados.append(empleado)
        return True

    def asignarEmpleado(self, empleado: Empleado):
        return self.agregar_empleado(empleado)

    def reasignarEmpleado(self, empleado: Empleado, nuevoDepartamento):
        if empleado not in self._empleados:
            return False
        if not isinstance(nuevoDepartamento, Departamento):
            return False
        if not nuevoDepartamento.agregar_empleado(empleado):
            return False
        self._empleados.remove(empleado)
        return True

    def mostrar_datos(self):
        return f"ID: {self.id} | Departamento: {self.nombre} | Gerente: {self.gerente}"
