from dominio.clima import Clima
from persistencia.conexion import abrir_conexion, obtener_motor


class ClimaDAO:

    @staticmethod
    def guardar(clima):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()

            if obtener_motor() == "sqlite":
                sql = """INSERT INTO clima (ciudad, fecha, temperatura, humedad, estado)
                         VALUES (?, ?, ?, ?, ?)
                         ON CONFLICT (ciudad, fecha) DO UPDATE SET
                         temperatura = excluded.temperatura,
                         humedad = excluded.humedad,
                         estado = excluded.estado"""
            else:
                sql = """INSERT INTO clima (ciudad, fecha, temperatura, humedad, estado)
                         VALUES (%s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE
                         temperatura = VALUES(temperatura),
                         humedad = VALUES(humedad),
                         estado = VALUES(estado)"""

            cursor.execute(sql, (clima.ciudad, clima.fecha, clima.temperatura,
                                 clima.humedad, clima.estado))
            conexion.commit()
            return clima
        finally:
            conexion.close()

    @staticmethod
    def ultimo(ciudad):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""SELECT ciudad, fecha, temperatura, humedad, estado FROM clima
                      WHERE ciudad = {marcador}
                      ORDER BY fecha DESC
                      LIMIT 1"""
            cursor.execute(sql, (ciudad,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        ciudad_guardada, fecha, temperatura, humedad, estado = fila
        return Clima(ciudad_guardada, fecha, temperatura, humedad, estado)
