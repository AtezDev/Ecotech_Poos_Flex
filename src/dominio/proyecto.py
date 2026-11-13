from datetime import date


class Proyecto:
    def __init__(self, nombre, descripcion, fechaInicio, id=None):
        # Vista UML: nombre, descripción y fecha de inicio de tipo date.
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del proyecto es obligatorio.")
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripción es obligatoria.")
        if type(fechaInicio) is not date:
            raise ValueError("La fecha del proyecto debe ser un date válido.")
        self.id = id
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.fechaInicio = fechaInicio

    def obtenerNombre(self):
        return self.nombre

    def cambiarNombre(self, nuevoNombre):
        if not isinstance(nuevoNombre, str) or not nuevoNombre.strip():
            return False
        self.nombre = nuevoNombre.strip()
        return True

    def obtenerDescripcion(self):
        return self.descripcion

    def cambiarDescripcion(self, nuevaDescripcion):
        if not isinstance(nuevaDescripcion, str) or not nuevaDescripcion.strip():
            return False
        self.descripcion = nuevaDescripcion.strip()
        return True

    def obtenerFechaInicio(self):
        return self.fechaInicio

    def cambiarFechaInicio(self, nuevaFecha):
        if type(nuevaFecha) is not date:
            return False
        self.fechaInicio = nuevaFecha
        return True

    def mostrar_datos(self):
        return (f"ID: {self.id} | Proyecto: {self.nombre} | "
                f"Descripción: {self.descripcion} | Inicio: {self.fechaInicio}")
