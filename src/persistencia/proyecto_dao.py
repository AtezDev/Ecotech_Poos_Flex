from datetime import date
from dominio.proyecto import Proyecto
from persistencia.conexion import abrir_conexion, obtener_motor


class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        if proyecto.id is not None:
            raise ValueError("Este proyecto ya fue guardado.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = ("INSERT INTO proyecto (nombre, descripcion, fecha_inicio) "
                   f"VALUES ({marcador}, {marcador}, {marcador})")
            valores = (proyecto.nombre, proyecto.descripcion, proyecto.fechaInicio.isoformat())
            cursor.execute(sql, valores)
            nuevo_id = cursor.lastrowid
            conexion.commit()
            proyecto.id = nuevo_id
            return proyecto
        finally:
            conexion.close()

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyecto ORDER BY id")
            filas = cursor.fetchall()
        finally:
            conexion.close()
        proyectos = []
        for id_proyecto, nombre, descripcion, fecha in filas:
            proyectos.append(Proyecto(nombre, descripcion,
                                      date.fromisoformat(str(fecha)), id=id_proyecto))
        return proyectos

    @staticmethod
    def buscar_id_por_nombre(nombre):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"SELECT id FROM proyecto WHERE nombre = {marcador}",
                (nombre,)
            )
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return fila[0]

    @staticmethod
    def buscar_por_id(id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"SELECT id, nombre, descripcion, fecha_inicio FROM proyecto WHERE id = {marcador}"
            cursor.execute(sql, (id_proyecto,))
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return Proyecto(fila[1], fila[2], date.fromisoformat(str(fila[3])), id=fila[0])

    @staticmethod
    def actualizar(proyecto):
        if proyecto.id is None:
            raise ValueError("Primero debes guardar el proyecto.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = (f"UPDATE proyecto SET nombre = {marcador}, descripcion = {marcador}, "
                   f"fecha_inicio = {marcador} WHERE id = {marcador}")
            valores = (proyecto.nombre, proyecto.descripcion,
                       proyecto.fechaInicio.isoformat(), proyecto.id)
            cursor.execute(sql, valores)
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_proyecto):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"DELETE FROM proyecto WHERE id = {marcador}", (id_proyecto,))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()
