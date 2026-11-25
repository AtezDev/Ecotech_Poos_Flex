from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, obtener_motor


class IndicadorDAO:

    @staticmethod
    def guardar(indicador):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()

            # La clave (codigo, fecha) hace que una misma fecha quede con una sola fila.
            if obtener_motor() == "sqlite":
                sql = """INSERT INTO indicador (codigo, fecha, valor)
                         VALUES (?, ?, ?)
                         ON CONFLICT (codigo, fecha)
                         DO UPDATE SET valor = excluded.valor"""
            else:
                sql = """INSERT INTO indicador (codigo, fecha, valor)
                         VALUES (%s, %s, %s)
                         ON DUPLICATE KEY UPDATE valor = VALUES(valor)"""

            cursor.execute(sql, (indicador.codigo, indicador.fecha, indicador.valor))
            conexion.commit()
            return indicador
        finally:
            conexion.close()

    @staticmethod
    def ultimo(codigo):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT codigo, fecha, valor FROM indicador
                      WHERE codigo = {marcador}
                      ORDER BY fecha DESC
                      LIMIT 1"""

            cursor.execute(sql, (codigo,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        codigo_guardado, fecha, valor = fila
        return Indicador(codigo_guardado, fecha, valor)
