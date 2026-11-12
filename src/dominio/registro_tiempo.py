from datetime import date


class RegistroTiempo:
    def __init__(self, fecha: date, horasTrabajadas: float,
                 descripcionTarea: str, id=None):
        if not isinstance(fecha, date):
            raise ValueError("La fecha debe ser una fecha válida.")
        if not self.validarHoras(horasTrabajadas):
            raise ValueError("Las horas deben ser mayores que cero.")
        if not isinstance(descripcionTarea, str) or not descripcionTarea.strip():
            raise ValueError("La descripción de la tarea es obligatoria.")
        self.id = id
        self.fecha = fecha
        self.horasTrabajadas = float(horasTrabajadas)
        self.descripcionTarea = descripcionTarea.strip()
        self.empleado = None
        self.proyecto = None

    @staticmethod
    def validarHoras(horas):
        return (isinstance(horas, (int, float))
                and not isinstance(horas, bool)
                and 0 < horas)

    def obtenerFecha(self):
        return self.fecha

    def cambiarFecha(self, nuevaFecha):
        if not isinstance(nuevaFecha, date):
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
        if not isinstance(fecha, date) or not self.validarHoras(horasTrabajadas):
            return False
        if not isinstance(descripcionTarea, str) or not descripcionTarea.strip():
            return False
        if empleado is None or proyecto is None:
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
