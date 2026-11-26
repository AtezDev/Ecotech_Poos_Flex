import math
from datetime import date


class Indicador:
    CODIGOS_VALIDOS = ("UF", "DOLAR", "EURO")

    def __init__(self, codigo, fecha, valor):
        self.codigo = self.validar_codigo(codigo)
        self.fecha = self.validar_fecha(fecha)
        self.valor = self.validar_valor(valor)

    @classmethod
    def validar_codigo(cls, codigo):
        if not isinstance(codigo, str):
            raise TypeError("El código del indicador debe ser texto.")
        codigo = codigo.strip().upper()
        if codigo not in cls.CODIGOS_VALIDOS:
            raise ValueError("Código de indicador no reconocido.")
        return codigo

    @classmethod
    def validar_fecha(cls, fecha):
        if not isinstance(fecha, str):
            raise TypeError("La fecha debe ser texto AAAA-MM-DD.")
        try:
            date.fromisoformat(fecha)
        except ValueError:
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.")
        return fecha

    @classmethod
    def validar_valor(cls, valor):
        if type(valor) not in (int, float):
            raise TypeError("El valor del indicador debe ser numérico.")
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador debe ser mayor que cero.")
        return float(valor)

    def mostrar_datos(self):
        return (f"Código: {self.codigo} | Fecha: {self.fecha} | "
                f"Valor: {self.valor}")
