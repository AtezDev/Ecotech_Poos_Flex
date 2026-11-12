from datetime import date
from math import isfinite
from dominio.proyecto import Proyecto


class Empleado:
    MIN_NOMBRE = 2
    MAX_NOMBRE = 80
    MIN_CORREO = 5
    MAX_CORREO = 150

    def __init__(self, nombre: str, direccion: str, telefono: str,
                 correoElectronico: str, fechaInicioContrato: date,
                 salario: float, id=None):
        self._id = None
        self.id = id
        self.nombre = nombre
        if not isinstance(direccion, str) or not direccion.strip():
            raise ValueError("La dirección es obligatoria.")
        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El teléfono es obligatorio.")
        self.direccion = direccion.strip()
        self.telefono = telefono.strip()
        self.correoElectronico = correoElectronico
        if type(fechaInicioContrato) is not date:
            raise ValueError("La fecha de contrato debe ser una fecha válida.")
        self.fechaInicioContrato = fechaInicioContrato
        if not self.validarSalario(salario):
            raise ValueError("El salario debe ser un número mayor o igual a cero.")
        self.salario = float(salario)
        self.departamento = None
        self._proyectos = []

    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not (Empleado.MIN_NOMBRE <= len(nombre) <= Empleado.MAX_NOMBRE):
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
        return nombre

    @staticmethod
    def validarCorreo(correo):
        if not isinstance(correo, str):
            return False
        correo = correo.strip()
        if not (Empleado.MIN_CORREO <= len(correo) <= Empleado.MAX_CORREO):
            return False
        if any(caracter.isspace() for caracter in correo) or correo.count("@") != 1:
            return False
        usuario, dominio = correo.split("@")
        partes = dominio.split(".")
        return bool(usuario) and len(partes) >= 2 and all(partes)

    @staticmethod
    def validar_correo(correo):
        if not Empleado.validarCorreo(correo):
            raise ValueError("El correo debe tener usuario, un @ y dominio con punto, sin espacios.")
        return correo.strip()

    @staticmethod
    def validarSalario(salario):
        return (isinstance(salario, (int, float))
                and not isinstance(salario, bool)
                and isfinite(salario) and salario >= 0)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if self._id is not None and valor != self._id:
            raise ValueError("No se puede modificar el ID de un empleado guardado.")
        if valor is not None and (not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0):
            raise ValueError("El ID debe ser un entero positivo.")
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = self.validar_nombre(valor)

    @property
    def correoElectronico(self):
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, valor):
        self._correoElectronico = self.validar_correo(valor)

    @property
    def correo(self):
        return self.correoElectronico

    @correo.setter
    def correo(self, valor):
        self.correoElectronico = valor

    def obtenerIdEmpleado(self):
        return self.id

    def obtenerNombre(self):
        return self.nombre

    def cambiarNombre(self, nuevoNombre):
        if not isinstance(nuevoNombre, str):
            return False
        if not (self.MIN_NOMBRE <= len(nuevoNombre.strip()) <= self.MAX_NOMBRE):
            return False
        self.nombre = nuevoNombre
        return True

    def obtenerDireccion(self):
        return self.direccion

    def cambiarDireccion(self, nuevaDireccion):
        if not isinstance(nuevaDireccion, str) or not nuevaDireccion.strip():
            return False
        self.direccion = nuevaDireccion.strip()
        return True

    def obtenerTelefono(self):
        return self.telefono

    def cambiarTelefono(self, nuevoTelefono):
        if not isinstance(nuevoTelefono, str) or not nuevoTelefono.strip():
            return False
        self.telefono = nuevoTelefono.strip()
        return True

    def obtenerCorreoElectronico(self):
        return self.correoElectronico

    def cambiarCorreoElectronico(self, nuevoCorreo):
        if not self.validarCorreo(nuevoCorreo):
            return False
        self.correoElectronico = nuevoCorreo
        return True

    def obtenerFechaInicioContrato(self):
        return self.fechaInicioContrato

    def obtenerSalario(self):
        return self.salario

    def cambiarSalario(self, nuevoSalario):
        if not self.validarSalario(nuevoSalario):
            return False
        self.salario = float(nuevoSalario)
        return True

    def registrarEmpleado(self, nombre, direccion, telefono, correoElectronico,
                         fechaInicioContrato, salario):
        if not isinstance(nombre, str) or not 2 <= len(nombre.strip()) <= 80:
            return False
        if not self.validarCorreo(correoElectronico):
            return False
        if not isinstance(direccion, str) or not direccion.strip():
            return False
        if not isinstance(telefono, str) or not telefono.strip():
            return False
        if type(fechaInicioContrato) is not date or not self.validarSalario(salario):
            return False
        self.nombre = nombre
        self.direccion = direccion.strip()
        self.telefono = telefono.strip()
        self.correoElectronico = correoElectronico
        self.fechaInicioContrato = fechaInicioContrato
        self.salario = float(salario)
        return True

    def asignarAProyecto(self, proyecto):
        if not isinstance(proyecto, Proyecto) or proyecto in self._proyectos:
            return False
        self._proyectos.append(proyecto)
        return True

    def desasignarDeProyecto(self, proyecto):
        if proyecto not in self._proyectos:
            return False
        self._proyectos.remove(proyecto)
        return True

    def mostrar_datos(self):
        return (f"ID: {self.id} | Nombre: {self.nombre} | Correo: {self.correoElectronico} | "
                f"Dirección: {self.direccion} | Teléfono: {self.telefono} | "
                f"Contrato: {self.fechaInicioContrato} | Salario: {self.salario}")
