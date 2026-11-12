from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()
    motor = obtener_motor()

    if motor == "sqlite":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='empleado'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(empleado)")
            columnas = {fila[1] for fila in cursor.fetchall()}
        else:
            columnas = None
    else:
        cursor.execute("SHOW TABLES LIKE 'empleado'")
        if cursor.fetchone():
            cursor.execute("SHOW COLUMNS FROM empleado")
            columnas = {fila[0] for fila in cursor.fetchall()}
        else:
            columnas = None

    necesarias = {"id", "nombre", "direccion", "telefono", "correo",
                  "fecha_inicio_contrato", "salario", "departamento_id"}
    if columnas is not None and not necesarias.issubset(columnas):
        conexion.close()
        faltantes = ", ".join(sorted(necesarias - columnas))
        raise ValueError(
            f"La tabla empleado tiene el esquema antiguo. Faltan: {faltantes}. "
            "No se modificaron tablas; usa una base de pruebas nueva."
        )

    if motor == "sqlite":
        tablas = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                gerente TEXT NOT NULL
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
            )"""
        ]
    else:
        tablas = [
            """CREATE TABLE IF NOT EXISTS departamento (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                gerente VARCHAR(100) NOT NULL
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
            ) ENGINE=InnoDB"""
        ]

    for sql in tablas:
        cursor.execute(sql)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas preparadas.")
