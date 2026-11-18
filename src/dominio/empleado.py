from datetime import date
from math import isfinite
from dominio.proyecto import Proyecto
from dominio.departamento import departamento


class Empleado:
    # Estos atributos vienen de las vistas 1 y 3 del UML final.
    # El ID comienza en None: la base de datos lo crea con INSERT.
    def __init__(self, nombre, direccion, telefono,
                 correoElectronico, fechaInicioContrato, salario, id=None):
        self._id = None
        self.id = id
        self.nombre = nombre
        self.direccion = self.validar_direccion(direccion)
        self.telefono = self.validar_telefono(telefono)
        self.correoElectronico = correoElectronico
        self.fechaInicioContrato = self.validar_fecha_contrato(fechaInicioContrato)
        self.salario = self.validar_salario(salario)
        self.departamento = None
        self._proyectos = []
        self.departamento = None

    # @staticmethod: no necesita usar self, porque valida un valor aislado.
    # raise ValueError avisa qué dato es incorrecto; el menú usa except para repetirlo.
    @staticmethod
    def validar_nombre(nombre):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto.")
        nombre = nombre.strip()
        if not 2 <= len(nombre) <= 80:
            raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
        letras = nombre.replace(" ", "").replace("'", "")
        if not letras.isalpha():
            raise ValueError("El nombre debe tener letras, espacios o apóstrofes.")
        return nombre

    @staticmethod
    def validar_direccion(direccion):
        if not isinstance(direccion, str):
            raise ValueError("La dirección debe ser texto.")
        direccion = direccion.strip()
        if not 1 <= len(direccion) <= 200:
            raise ValueError("La dirección es obligatoria (máximo 200 caracteres).")
        return direccion

    @staticmethod
    def validar_telefono(telefono):
        if not isinstance(telefono, str):
            raise ValueError("El teléfono debe ser texto.")
        telefono = telefono.strip()
        digitos = telefono[1:] if telefono.startswith("+") else telefono
        # Regla propuesta para EcoTech: 8 a 15 dígitos y un + inicial opcional.
        if not digitos.isascii() or not digitos.isdigit() or not 8 <= len(digitos) <= 15:
            raise ValueError("Usa entre 8 y 15 dígitos, con + inicial opcional.")
        return telefono

    @staticmethod
    def validar_fecha_contrato(fecha):
        # En los objetos usamos date; convertir texto a date le corresponde al menú.
        if type(fecha) is not date:
            raise ValueError("La fecha de contrato debe ser un date válido.")
        return fecha

    @staticmethod
    def validarCorreo(correo):
        # Este método del UML devuelve Boolean: True si cumple y False si no.
        if not isinstance(correo, str):
            return False
        correo = correo.strip()
        if not 5 <= len(correo) <= 150 or any(x.isspace() for x in correo):
            return False
        if correo.count("@") != 1:
            return False
        usuario, dominio = correo.split("@")
        partes = dominio.split(".")
        return bool(usuario) and len(partes) >= 2 and all(partes)

    @staticmethod
    def validar_correo(correo):
        # Adaptación a Clase 3/4: convertir el resultado booleano en ValueError.
        if not Empleado.validarCorreo(correo):
            raise ValueError("Usa usuario@dominio.cl, sin espacios.")
        return correo.strip()

    @staticmethod
    def validarSalario(salario):
        # Es una regla de negocio básica. isfinite descarta infinito y NaN.
        return (isinstance(salario, (int, float))
                and not isinstance(salario, bool)
                and isfinite(salario) and salario >= 0)

    @staticmethod
    def validar_salario(salario):
        if not Empleado.validarSalario(salario):
            raise ValueError("El salario debe ser numérico y no negativo.")
        return float(salario)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, nuevo_id):
        # El UML indica que idEmpleado es inmutable una vez generado.
        if self._id is not None and nuevo_id != self._id:
            raise ValueError("El ID de un empleado guardado no se modifica.")
        self._id = nuevo_id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        # El setter se ejecuta incluso al usar self.nombre = nombre en __init__.
        self._nombre = self.validar_nombre(nuevo_nombre)

    @property
    def correoElectronico(self):
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, nuevo_correo):
        self._correoElectronico = self.validar_correo(nuevo_correo)

    @property
    def correo(self):
        return self.correoElectronico

    @correo.setter
    def correo(self, valor):
        self.correoElectronico = valor

    # Métodos de la vista 3: obtener no cambia datos; cambiar devuelve Boolean.
    def obtenerIdEmpleado(self):
        return self.id

    def obtenerNombre(self):
        return self.nombre

    def cambiarNombre(self, nuevoNombre):
        try:
            self.nombre = nuevoNombre
        except ValueError:
            return False
        return True

    def obtenerDireccion(self):
        return self.direccion

    def cambiarDireccion(self, nuevaDireccion):
        try:
            self.direccion = self.validar_direccion(nuevaDireccion)
        except ValueError:
            return False
        return True

    def obtenerTelefono(self):
        return self.telefono

    def cambiarTelefono(self, nuevoTelefono):
        try:
            self.telefono = self.validar_telefono(nuevoTelefono)
        except ValueError:
            return False
        return True

    def obtenerCorreoElectronico(self):
        return self.correoElectronico

    def cambiarCorreoElectronico(self, nuevoCorreo):
        try:
            self.correoElectronico = nuevoCorreo
        except ValueError:
            return False
        return True

    def obtenerFechaInicioContrato(self):
        return self.fechaInicioContrato

    def obtenerSalario(self):
        return self.salario

    def cambiarSalario(self, nuevoSalario):
        try:
            self.salario = self.validar_salario(nuevoSalario)
        except ValueError:
            return False
        return True

    def registrarEmpleado(self, nombre, direccion, telefono, correoElectronico,
                         fechaInicioContrato, salario):
        # Comprobamos primero todos los valores: si alguno falla, no cambiamos ninguno.
        try:
            nombre = self.validar_nombre(nombre)
            direccion = self.validar_direccion(direccion)
            telefono = self.validar_telefono(telefono)
            correoElectronico = self.validar_correo(correoElectronico)
            fechaInicioContrato = self.validar_fecha_contrato(fechaInicioContrato)
            salario = self.validar_salario(salario)
        except ValueError:
            return False
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.fechaInicioContrato = fechaInicioContrato
        self.salario = salario
        return True

    # Relación UML N:M. La lista guarda objetos; el DAO guarda los IDs en SQL.
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
        return (f"ID: {self.id} | Nombre: {self.nombre} | "
                f"Dirección: {self.direccion} | Teléfono: {self.telefono} | "
                f"Correo: {self.correoElectronico} | "
                f"Contrato: {self.fechaInicioContrato} | Salario: {self.salario}")
