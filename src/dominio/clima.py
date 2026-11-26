import math
import re


class Clima:
    ESTADOS = {
        0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
        3: "Nublado", 45: "Niebla", 48: "Niebla con escarcha",
        51: "Llovizna", 53: "Llovizna", 55: "Llovizna", 61: "Lluvia",
        63: "Lluvia", 65: "Lluvia fuerte", 71: "Nieve", 73: "Nieve",
        75: "Nieve fuerte", 80: "Chubascos", 81: "Chubascos", 82: "Chubascos fuertes",
        95: "Tormenta", 96: "Tormenta con granizo", 99: "Tormenta con granizo",
    }

    def __init__(self, ciudad, fecha, temperatura, humedad, estado):
        self.ciudad = self.validar_ciudad(ciudad)
        self.fecha = self.validar_texto(fecha, "La fecha del dato es obligatoria.")
        self.temperatura = self.validar_numero(temperatura, -90, 60, "temperatura")
        self.humedad = self.validar_numero(humedad, 0, 100, "humedad")
        self.estado = self.validar_texto(estado, "El estado del clima es obligatorio.")

    @classmethod
    def validar_ciudad(cls, ciudad):
        if not isinstance(ciudad, str):
            raise TypeError("La ciudad debe ser texto.")
        ciudad = ciudad.strip()
        if not ciudad or not any(c.isalpha() for c in ciudad):
            raise ValueError("Escribe el nombre de la ciudad.")
        if not 2 <= len(ciudad) <= 60:
            raise ValueError("La ciudad debe tener entre 2 y 60 caracteres.")
        if not re.fullmatch(r"[A-Za-z\u00C0-\u024F .'-]+", ciudad):
            raise ValueError("La ciudad solo puede contener letras, espacios, guiones o apóstrofes.")
        return ciudad

    @staticmethod
    def validar_texto(texto, mensaje):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError(mensaje)
        return texto.strip()

    @staticmethod
    def validar_numero(valor, minimo, maximo, nombre):
        if type(valor) not in (int, float):
            raise TypeError(f"La {nombre} debe ser numérica.")
        if not math.isfinite(valor) or not minimo <= valor <= maximo:
            raise ValueError(f"La {nombre} está fuera de rango.")
        return float(valor)

    @classmethod
    def traducir_estado(cls, codigo):
        return cls.ESTADOS.get(codigo, "Estado desconocido")

    def mostrar_datos(self):
        return (f"Ciudad: {self.ciudad} | Fecha: {self.fecha} | "
                f"Temperatura: {self.temperatura} °C | Humedad: {self.humedad} % | "
                f"Estado: {self.estado}")
