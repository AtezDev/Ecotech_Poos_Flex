# Clase departamento


class Departamento:
    def __init__(self, nombre: str, gerente: str ):
            self.nombre = nombre
            self.gerente = gerente

    def mostrar_datos(self) -> str:
        return f" nombre: {self.nombre} gerente: {self.gerente}"