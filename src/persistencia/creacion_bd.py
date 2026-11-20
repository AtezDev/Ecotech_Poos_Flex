from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    # Primero comprobamos el esquema: no debemos sobrescribir la base vieja.
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        motor = obtener_motor()

        # Las seis tablas representan las clases y relaciones implementadas.
        columnas_requeridas = {
            "departamento": {"id", "nombre", "gerente_id"},
            "proyecto": {"id", "nombre", "descripcion", "fecha_inicio"},
            "empleado": {"id", "nombre", "direccion", "telefono", "correo",
                         "fecha_inicio_contrato", "salario", "departamento_id"},
            "empleado_proyecto": {"empleado_id", "proyecto_id"},
            "registro_tiempo": {"id", "fecha", "horas_trabajadas", "descripcion_tarea",
                                "empleado_id", "proyecto_id"},
            "usuario": {"id", "nombre_usuario", "password_hash", "empleado_id"}
        }
        if motor == "mysql":
            cursor.execute("SHOW TABLES")
            tablas_existentes = {fila[0] for fila in cursor.fetchall()}

        for tabla, necesarias in columnas_requeridas.items():
            if motor == "sqlite":
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (tabla,))
                existe = cursor.fetchone() is not None
                if existe:
                    cursor.execute(f"PRAGMA table_info({tabla})")
                    columnas = {fila[1] for fila in cursor.fetchall()}
            else:
                existe = tabla in tablas_existentes
                if existe:
                    cursor.execute(f"SHOW COLUMNS FROM {tabla}")
                    columnas = {fila[0] for fila in cursor.fetchall()}
            if existe and not necesarias.issubset(columnas):
                faltantes = ", ".join(sorted(necesarias - columnas))
                raise ValueError(
                    f"La tabla {tabla} tiene un esquema incompatible. Faltan: {faltantes}. "
                    "Usa una base nueva o planifica una migración independiente."
                )

        # CREATE TABLE IF NOT EXISTS permite ejecutar este paso varias veces.
        if motor == "sqlite":
            tablas = [
                """CREATE TABLE IF NOT EXISTS departamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    gerente_id INTEGER,
                    FOREIGN KEY (gerente_id) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS proyecto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS empleado (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    fecha_inicio_contrato TEXT NOT NULL,
                    salario REAL NOT NULL,
                    departamento_id INTEGER,
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                )""",
                """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                    empleado_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    PRIMARY KEY (empleado_id, proyecto_id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                )""",
                """CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    horas_trabajadas REAL NOT NULL,
                    descripcion_tarea TEXT NOT NULL,
                    empleado_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    FOREIGN KEY (empleado_id, proyecto_id)
                        REFERENCES empleado_proyecto(empleado_id, proyecto_id)
                )""",
                """CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    empleado_id INTEGER NOT NULL UNIQUE,
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                )"""
            ]
        else:
            tablas = [
                """CREATE TABLE IF NOT EXISTS departamento (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    gerente_id INT,
                    FOREIGN KEY (gerente_id) REFERENCES empleado(id)
                ) ENGINE=InnoDB""",
                """CREATE TABLE IF NOT EXISTS proyecto (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio DATE NOT NULL
                ) ENGINE=InnoDB""",
                """CREATE TABLE IF NOT EXISTS empleado (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(80) NOT NULL,
                    direccion VARCHAR(200) NOT NULL,
                    telefono VARCHAR(30) NOT NULL,
                    correo VARCHAR(150) NOT NULL,
                    fecha_inicio_contrato DATE NOT NULL,
                    salario DECIMAL(12,2) NOT NULL,
                    departamento_id INT,
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id)
                ) ENGINE=InnoDB""",
                """CREATE TABLE IF NOT EXISTS empleado_proyecto (
                    empleado_id INT NOT NULL,
                    proyecto_id INT NOT NULL,
                    PRIMARY KEY (empleado_id, proyecto_id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                ) ENGINE=InnoDB""",
                """CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    fecha DATE NOT NULL,
                    horas_trabajadas FLOAT NOT NULL,
                    descripcion_tarea TEXT NOT NULL,
                    empleado_id INT NOT NULL,
                    proyecto_id INT NOT NULL,
                    FOREIGN KEY (empleado_id, proyecto_id)
                        REFERENCES empleado_proyecto(empleado_id, proyecto_id)
                ) ENGINE=InnoDB""",
                """CREATE TABLE IF NOT EXISTS usuario (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre_usuario VARCHAR(40) NOT NULL UNIQUE,
                    password_hash VARCHAR(100) NOT NULL,
                    empleado_id INT NOT NULL UNIQUE,
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                ) ENGINE=InnoDB"""
            ]

        # Ejecutamos el SQL y confirmamos la creación con commit().
        # departamento y empleado se apuntan entre sí (gerente_id y departamento_id).
        # En MySQL apagamos un momento la revisión para poder crear la primera tabla.
        if motor == "mysql":
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for sql in tablas:
            cursor.execute(sql)
        if motor == "mysql":
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        conexion.commit()
    finally:
        # finally cierra la conexión, incluso cuando algún SQL produce error.
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas preparadas.")
