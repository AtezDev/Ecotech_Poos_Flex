import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Clase de persistencia: esta carpeta conoce la base de datos, el dominio no.
# RAIZ apunta a la carpeta del proyecto aunque ejecutes Python desde otra ubicación.
RAIZ = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ / ".env")


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        nombre = os.getenv("DB_NAME", "ecotech_practica.db")
        ruta = Path(nombre)
        if not ruta.is_absolute():
            ruta = RAIZ / ruta
        conexion = sqlite3.connect(ruta)
        # Sin esta línea, SQLite no obliga a cumplir las claves foráneas.
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    if motor == "mysql":
        import pymysql
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "ecotech_practica"),
            charset="utf8mb4"
        )

    raise ValueError("Motor de base de datos no reconocido: " + motor)
