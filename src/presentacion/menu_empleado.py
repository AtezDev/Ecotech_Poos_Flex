import sqlite3
from datetime import date
from dominio.empleado import Empleado
from persistencia.conexion import obtener_motor
from persistencia.empleado_dao import EmpleadoDAO


def tipos_errores_bd():
    # Las excepciones de SQLite y MySQL tienen nombres iguales, pero clases distintas.
    if obtener_motor() == "mysql":
        from pymysql.err import IntegrityError, OperationalError
        return IntegrityError, OperationalError
    return sqlite3.IntegrityError, sqlite3.OperationalError


def solicitar(campo, validador):
    # Una sola función reutiliza TODOS los validadores del Empleado.
    # 'validador' es una función, no un booleano.
    while True:
        valor = input(f"{campo}: ")
        try:
            return validador(valor)
        except ValueError as error:
            print(f"{campo} inválido: {error}")
            # Volvemos al comienzo del while; no se pierden los campos anteriores.


def solicitar_fecha(texto):
    # input() devuelve str. Convertimos ese texto en un objeto date real.
    try:
        texto = texto.strip()
        if len(texto) != 10 or texto[4] != "-" or texto[7] != "-":
            raise ValueError("Formato incorrecto.")
        fecha = date.fromisoformat(texto)
    except ValueError:
        raise ValueError("Usa una fecha real en formato AAAA-MM-DD.")
    return Empleado.validar_fecha_contrato(fecha)


def solicitar_salario(texto):
    texto = texto.strip()
    # Técnica de Banco Inacapino: isdigit() comprueba los dígitos escritos.
    if not texto.replace(".", "", 1).isdigit():
        raise ValueError("Escribe solo números: 950000 o 950000.50.")
    return Empleado.validar_salario(float(texto))


def solicitar_id():
    while True:
        texto = input("ID del empleado: ").strip()
        try:
            id_empleado = int(texto)
            if id_empleado <= 0:
                raise ValueError("El ID debe ser positivo.")
        except ValueError:
            print("Ingresa un número entero mayor que cero.")
        else:
            return id_empleado


def crear_empleado():
    nombre = solicitar("Nombre", Empleado.validar_nombre)
    direccion = solicitar("Dirección", Empleado.validar_direccion)
    telefono = solicitar("Teléfono", Empleado.validar_telefono)
    correo = solicitar("Correo", Empleado.validar_correo)
    fecha = solicitar("Fecha contrato (AAAA-MM-DD)", solicitar_fecha)
    salario = solicitar("Salario", solicitar_salario)

    empleado = Empleado(nombre, direccion, telefono, correo, fecha, salario)
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        EmpleadoDAO.insertar(empleado)
    except IntegrityError:
        print("No se pudo registrar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo conectar o completar el registro.")
    else:
        # Solo decimos 'registrado' si el INSERT y el commit terminaron bien.
        print(f"Empleado registrado. ID: {empleado.id}")


def listar_empleados():
    _, OperationalError = tipos_errores_bd()
    try:
        empleados = EmpleadoDAO.listar()
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not empleados:
            print("Todavía no hay empleados registrados.")
        for empleado in empleados:
            print(empleado.mostrar_datos())


def buscar_empleado():
    id_empleado = solicitar_id()
    _, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if empleado is None:
            print("No existe un empleado con ese ID.")
        else:
            print(empleado.mostrar_datos())


def actualizar_empleado():
    id_empleado = solicitar_id()
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe un empleado con ese ID.")
            return
        nuevo_correo = solicitar("Nuevo correo", Empleado.validar_correo)
        if nuevo_correo == empleado.correoElectronico:
            print("El correo es el mismo; no hay cambios.")
            return
        empleado.correoElectronico = nuevo_correo
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Correo actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def confirmar_eliminacion():
    # Otra técnica que conoces del Banco Inacapino: responder S o N.
    while True:
        respuesta = input("¿Eliminar empleado? (s/n): ").strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("Responde s o n.")


def eliminar_empleado():
    id_empleado = solicitar_id()
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe un empleado con ese ID.")
            return
        print(empleado.mostrar_datos())
        if not confirmar_eliminacion():
            print("Eliminación cancelada.")
            return
        filas = EmpleadoDAO.eliminar(id_empleado)
    except IntegrityError:
        print("No se puede eliminar: el empleado tiene relaciones o hay otra restricción.")
    except OperationalError:
        print("No se pudo completar la eliminación.")
    else:
        if filas == 1:
            print("Empleado eliminado correctamente.")
        else:
            print("No se eliminó: vuelve a consultar el ID.")


def solicitar_id_de(entidad):
    while True:
        texto = input(f"ID de {entidad}: ").strip()
        try:
            numero = int(texto)
            if numero <= 0:
                raise ValueError("El ID debe ser positivo.")
        except ValueError:
            print("Ingresa un número entero mayor que cero.")
        else:
            return numero


def actualizar_nombre():
    id_empleado = solicitar_id_de("empleado")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe empleado con ese ID.")
            return
        nuevo = solicitar("Nombre", Empleado.validar_nombre)
        if nuevo == empleado.obtenerNombre():
            print("El valor es el mismo; no hay cambios.")
            return
        empleado.cambiarNombre(nuevo)
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Nombre actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_direccion():
    id_empleado = solicitar_id_de("empleado")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe empleado con ese ID.")
            return
        nuevo = solicitar("Dirección", Empleado.validar_direccion)
        if nuevo == empleado.obtenerDireccion():
            print("El valor es el mismo; no hay cambios.")
            return
        empleado.cambiarDireccion(nuevo)
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Dirección actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_telefono():
    id_empleado = solicitar_id_de("empleado")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe empleado con ese ID.")
            return
        nuevo = solicitar("Teléfono", Empleado.validar_telefono)
        if nuevo == empleado.obtenerTelefono():
            print("El valor es el mismo; no hay cambios.")
            return
        empleado.cambiarTelefono(nuevo)
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Teléfono actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_salario():
    id_empleado = solicitar_id_de("empleado")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        if empleado is None:
            print("No existe empleado con ese ID.")
            return
        nuevo = solicitar("Salario", solicitar_salario)
        if nuevo == empleado.obtenerSalario():
            print("El valor es el mismo; no hay cambios.")
            return
        empleado.cambiarSalario(nuevo)
        filas = EmpleadoDAO.actualizar(empleado)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Salario actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def menu_empleados():
    # Menú del docente: while True mantiene viva la aplicación hasta la opción 0.
    while True:
        print("\n--- ECOTECH: EMPLEADOS ---")
        print("1. Registrar\n2. Listar\n3. Buscar por ID")
        print("4. Actualizar correo\n5. Eliminar")
        print("6. Actualizar dirección\n7. Actualizar teléfono")
        print("8. Actualizar nombre\n9. Actualizar salario\n0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_empleado()
        elif opcion == "2":
            listar_empleados()
        elif opcion == "3":
            buscar_empleado()
        elif opcion == "4":
            actualizar_empleado()
        elif opcion == "5":
            eliminar_empleado()
        elif opcion == "6":
            actualizar_direccion()
        elif opcion == "7":
            actualizar_telefono()
        elif opcion == "8":
            actualizar_nombre()
        elif opcion == "9":
            actualizar_salario()
        elif opcion == "0":
            print("Saliendo de EcoTech.")
            break  # Sale del while, no de toda la computadora.
        else:
            print("Elige una opción entre 0 y 9.")
