from datetime import date
from dominio.empleado import Empleado
from dominio.proyecto import Proyecto


class RegistroTiempo:
    def __init__(self, fecha, horasTrabajadas, descripcionTarea, id=None):
        # El UML exige una fecha, horas y descripción de tarea.
        if type(fecha) is not date:
            raise ValueError("La fecha del registro debe ser un date válido.")
        if not self.validarHoras(horasTrabajadas):
            raise ValueError("Las horas deben ser mayores que cero.")
        if not isinstance(descripcionTarea, str) or not descripcionTarea.strip():
            raise ValueError("La tarea es obligatoria.")
        self.id = id
        self.fecha = fecha
        self.horasTrabajadas = float(horasTrabajadas)
        self.descripcionTarea = descripcionTarea.strip()
        self.empleado = None
        self.proyecto = None

    @staticmethod
    def validarHoras(horas):
        return (isinstance(horas, (int, float))
                and not isinstance(horas, bool) and 0 < horas < float("inf"))

    def obtenerFecha(self):
        return self.fecha

    def cambiarFecha(self, nuevaFecha):
        if type(nuevaFecha) is not date:
            return False
        self.fecha = nuevaFecha
        return True

    def obtenerHorasTrabajadas(self):
        return self.horasTrabajadas

    def cambiarHorasTrabajadas(self, nuevasHoras):
        if not self.validarHoras(nuevasHoras):
            return False
        self.horasTrabajadas = float(nuevasHoras)
        return True

    def obtenerDescripcionTarea(self):
        return self.descripcionTarea

    def cambiarDescripcionTarea(self, nuevaDescripcion):
        if not isinstance(nuevaDescripcion, str) or not nuevaDescripcion.strip():
            return False
        self.descripcionTarea = nuevaDescripcion.strip()
        return True

    def registrarTiempo(self, fecha, horasTrabajadas, descripcionTarea,
                        empleado, proyecto):
        if type(fecha) is not date or not self.validarHoras(horasTrabajadas):
            return False
        if not isinstance(descripcionTarea, str) or not descripcionTarea.strip():
            return False
        if not isinstance(empleado, Empleado) or not isinstance(proyecto, Proyecto):
            return False
        self.fecha = fecha
        self.horasTrabajadas = float(horasTrabajadas)
        self.descripcionTarea = descripcionTarea.strip()
        self.empleado = empleado
        self.proyecto = proyecto
        return True

    def mostrar_datos(self):
        return (f"ID: {self.id} | Fecha: {self.fecha} | "
                f"Horas: {self.horasTrabajadas} | Tarea: {self.descripcionTarea}")
