# Clase Registro tiempo
import datetime


class RegistroTiempo:
    def __init__(self, Fecha: datetime.date, horas_trabajadas: float, descripcion_Tarea: str):
        self.Fecha = Fecha
        self.horasT = horas_trabajadas
        self.descripcionT = descripcion_Tarea

    def mostrar_datos(self) -> str:
        return f" Fecha: {self.Fecha} Horas trabajadas: {self.horasT} Descripcion Tarea: {self.descripcionT}"