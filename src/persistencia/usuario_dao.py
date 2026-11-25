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
                      (nombre_usuario, password_hash, empleado_id, rol)
                      VALUES ({marcador}, {marcador}, {marcador}, {marcador})"""

            cursor.execute(sql, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.empleado_id,
                usuario.rol
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

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id, rol
                      FROM usuario
                      WHERE nombre_usuario = {marcador}"""

            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return UsuarioDAO._desde_fila(fila)

    @staticmethod
    def buscar_por_id(id_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id, rol
                      FROM usuario
                      WHERE id = {marcador}"""

            cursor.execute(sql, (id_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return UsuarioDAO._desde_fila(fila)

    @staticmethod
    def buscar_por_empleado_id(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"

            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id, rol
                      FROM usuario
                      WHERE empleado_id = {marcador}"""

            cursor.execute(sql, (empleado_id,))
            fila = cursor.fetchone()
        finally:
            conexion.close()

        if fila is None:
            return None

        return UsuarioDAO._desde_fila(fila)

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT id, nombre_usuario, password_hash, empleado_id, rol
                              FROM usuario
                              ORDER BY id""")
            filas = cursor.fetchall()
        finally:
            conexion.close()

        return [UsuarioDAO._desde_fila(fila) for fila in filas]

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
                          password_hash = {marcador},
                          rol = {marcador}
                      WHERE id = {marcador}"""

            cursor.execute(sql, (
                usuario.nombre_usuario,
                usuario.password_hash,
                usuario.rol,
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

    @staticmethod
    def _desde_fila(fila):
        id_cuenta, nombre, password_hash, empleado_id, rol = fila
        return Usuario(nombre, password_hash, empleado_id, id=id_cuenta, rol=rol)
