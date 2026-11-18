from dominio.empleado import Empleado


class Departamento:
    def __init__(self, nombre, gerente, id=None):
        # Atributos de Departamento según el UML.
        if not self.validarNombre(nombre):
            raise ValueError("El nombre del departamento es obligatorio.")
        if id is None:
            gerente = self.validar_gerente(gerente)
        elif not isinstance(gerente, str) or not gerente.strip():
            raise ValueError("El gerente es obligatorio.")
        self.id = id
        self.nombre = nombre.strip()
        self.gerente = gerente.strip()
        self._empleados = []  # 0..*: varios objetos Empleado.

    @staticmethod
    def validarNombre(nombre):
        return isinstance(nombre, str) and bool(nombre.strip())

    @staticmethod
    def validar_gerente(gerente):
        if not isinstance(gerente, str):
            raise ValueError("El gerente debe ser texto.")
        gerente = gerente.strip()
        if not 2 <= len(gerente) <= 80:
            raise ValueError("El gerente debe tener entre 2 y 80 caracteres.")
        letras = gerente.replace(" ", "").replace("'", "")
        if not letras.isalpha():
            raise ValueError("El gerente debe ser un nombre de persona: solo letras, espacios o apóstrofes (por ejemplo: Javier Ahumada).")
        return gerente

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
        try:
            self.gerente = self.validar_gerente(nuevoGerente)
        except ValueError:
            return False
        return True

    @property
    def empleados(self):
        # Devolvemos una tupla para que no modifiquen la lista interna directamente.
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado):
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
        return f"ID: {self.id} | Departamento: {self.nombre} | Gerente: {self.gerente}"
