
class Departamento:
    def __init__(self, nombre, gerente=None, id=None):
        # Atributos de Departamento según el UML.
        if not self.validarNombre(nombre):
            raise ValueError("El nombre del departamento es obligatorio.")
        if not self.validarGerente(gerente):
            raise ValueError("El gerente debe ser un empleado o quedar vacío.")
        self.id = id
        self.nombre = nombre.strip()
        self.gerente = gerente  # Un objeto Empleado, o None si aún no tiene gerente.
        self._empleados = []  # 0..*: varios objetos Empleado.

    @staticmethod
    def validarNombre(nombre):
        return isinstance(nombre, str) and bool(nombre.strip())

    @staticmethod
    def validarGerente(gerente):
        from dominio.empleado import Empleado
        return gerente is None or isinstance(gerente, Empleado)

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
        if not self.validarGerente(nuevoGerente):
            return False
        self.gerente = nuevoGerente
        return True

    @property
    def empleados(self):
        # Devolvemos una tupla para que no modifiquen la lista interna directamente.
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado):
        from dominio.empleado import Empleado
        # Un empleado puede pertenecer como máximo a un Departamento.
        if not isinstance(empleado, Empleado) or empleado in self._empleados:
            return False
        if empleado.departamento is not None and empleado.departamento is not self:
            return False
        self._empleados.append(empleado)
        empleado.departamento = self
        return True

    def asignarEmpleado(self, empleado):
        return self.agregar_empleado(empleado)

    def reasignarEmpleado(self, empleado, nuevoDepartamento):
        if empleado not in self._empleados or not isinstance(nuevoDepartamento, Departamento):
            return False
        if nuevoDepartamento is self:
            return False
        self._empleados.remove(empleado)
        empleado.departamento = None
        if nuevoDepartamento.agregar_empleado(empleado):
            return True
        # Si falla el cambio, dejamos al empleado en el departamento original.
        self._empleados.append(empleado)
        empleado.departamento = self
        return False

    def mostrar_datos(self):
        if self.gerente is None:
            texto_gerente = "Sin gerente"
        else:
            texto_gerente = f"{self.gerente.nombre} (ID {self.gerente.id})"
        return f"ID: {self.id} | Departamento: {self.nombre} | Gerente: {texto_gerente}"
