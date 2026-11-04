# Clase Proyecto

class Proyecto:
    def __init__(self, nombre: str, descripcion: str ):
            self.nombre = nombre
            self.descripcion = descripcion

    def mostrar_datos(self) -> str:
        return f" nombre: {self.nombre} descripcion: {self.descripcion}"