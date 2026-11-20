
from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, obtener_motor


class UsuarioDAO:

    @staticmethod
    def insertar(usuario):
        if usuario.id is not None:
            raise ValueError("Esta cuenta ya fue guardada.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""INSERT INTO usuario
                      (nombre_usuario, password_hash, empleado_id)
                      VALUES ({marcador}, {marcador}, {marcador})"""

            cursor.execute(sql, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.empleado_id
            ))

            usuario.id = cursor.lastrowid
            conexion.commit()
            return usuario
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id
                      FROM usuario
                      WHERE nombre_usuario = {marcador}"""

            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        id_cuenta, nombre, password_hash, empleado_id = fila
        return Usuario(nombre, password_hash, empleado_id, id=id_cuenta)

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id
                      FROM usuario
                      WHERE id = {marcador}"""

            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        id_cuenta, nombre, password_hash, empleado_id = fila
        return Usuario(nombre, password_hash, empleado_id, id=id_cuenta)

    @staticmethod
    def buscar_por_empleado_id(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id
                      FROM usuario
                      WHERE empleado_id = {marcador}"""

            cursor.execute(sql, (empleado_id,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        id_cuenta, nombre, password_hash, id_empleado = fila
        return Usuario(nombre, password_hash, id_empleado, id=id_cuenta)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT id, nombre_usuario, password_hash, empleado_id
                              FROM usuario
                              ORDER BY id""")
            filas = cursor.fetchall()
        finally:
            conexion.close()

        usuarios = []

        for id_cuenta, nombre, password_hash, empleado_id in filas:
            usuarios.append(
                Usuario(nombre, password_hash, empleado_id, id=id_cuenta)
            )

        return usuarios

    @staticmethod
    def actualizar(usuario):
        if usuario.id is None:
            raise ValueError("Primero debes guardar la cuenta.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""UPDATE usuario
                      SET nombre_usuario = {marcador},
                          password_hash = {marcador}
                      WHERE id = {marcador}"""

            cursor.execute(sql, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.id
            ))

            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"DELETE FROM usuario WHERE id = {marcador}"
            cursor.execute(sql, (id_usuario,))

            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()
