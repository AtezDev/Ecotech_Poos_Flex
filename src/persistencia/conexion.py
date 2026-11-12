import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv


RAIZ = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ / ".env")


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def abrir_conexion():
    motor = obtener_motor()

    if motor == "sqlite":
        nombre = os.getenv("DB_NAME", "ecotech_practica.db")
        archivo = Path(nombre)
        if not archivo.is_absolute():
            archivo = RAIZ / archivo
        conexion = sqlite3.connect(archivo)
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

    raise ValueError(f"Motor no soportado: {motor}")
