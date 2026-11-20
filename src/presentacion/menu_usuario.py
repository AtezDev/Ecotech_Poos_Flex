
from getpass import getpass

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_empleado import solicitar_id, tipos_errores_bd
from presentacion.menu_principal import cargar_datos_de_ejemplo

from servicios.autenticacion import (
    autenticar,
    registrar_usuario,
    listar_usuarios,
    buscar_usuario_por_id,
    buscar_usuario_por_nombre,
    actualizar_usuario,
    eliminar_usuario
)

MAX_INTENTOS = 3


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    _, OperationalError = tipos_errores_bd()

    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    except OperationalError:
        print("No se pudo verificar el acceso. Intenta de nuevo más tarde.")
        return None

    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")

    return usuario


def solicitar_clave_nueva():
    while True:
        clave = getpass("Contraseña nueva: ")

        try:
            Usuario.validar_clave(clave)
        except (TypeError, ValueError) as error:
            print(f"Contraseña inválida: {error}")
        else:
            repetida = getpass("Repite la contraseña: ")

            if clave == repetida:
                return clave

            print("Las contraseñas no coinciden.")


def registrar_cuenta():
    IntegrityError, OperationalError = tipos_errores_bd()
    empleado_id = solicitar_id()
    nombre = input("Usuario nuevo: ")

    print(
        f"La contraseña debe tener al menos "
        f"{Usuario.MIN_CLAVE} caracteres."
    )

    clave = solicitar_clave_nueva()

    try:
        usuario = registrar_usuario(empleado_id, nombre, clave)

    except (TypeError, ValueError) as error:
        print(f"No se pudo crear la cuenta: {error}")

    except IntegrityError:
        print(
            "No se pudo crear la cuenta: ese usuario "
            "o ese empleado ya tienen una cuenta."
        )

    except OperationalError:
        print("No se pudo completar el registro de la cuenta.")

    else:
        print(f"Cuenta creada para el usuario: {usuario.nombre_usuario}")


def mostrar_empleado_vinculado(usuario):
    _, OperationalError = tipos_errores_bd()

    try:
        empleado = EmpleadoDAO.buscar_por_id(usuario.empleado_id)
    except OperationalError:
        empleado = None

    if empleado is None:
        print("No se pudo recuperar el empleado vinculado a la cuenta.")
        return False

    print(f"Empleado: {empleado.nombre} | {empleado.correoElectronico}")
    return True


def mostrar_usuarios():
    _, OperationalError = tipos_errores_bd()

    try:
        usuarios = listar_usuarios()
    except OperationalError:
        print("No se pudieron recuperar las cuentas.")
        return

    if not usuarios:
        print("No existen cuentas registradas.")
        return

    print("\n=== CUENTAS REGISTRADAS ===")

    for usuario in usuarios:
        print(
            f"ID: {usuario.id} | "
            f"Usuario: {usuario.nombre_usuario} | "
            f"Empleado ID: {usuario.empleado_id}"
        )


def buscar_cuenta():
    print("\n=== BUSCAR CUENTA ===")
    print("1. Buscar por ID")
    print("2. Buscar por nombre de usuario")

    opcion = input("Opción: ").strip()

    try:
        if opcion == "1":
            id_usuario = solicitar_id_usuario()
            usuario = buscar_usuario_por_id(id_usuario)

        elif opcion == "2":
            nombre = input("Nombre de usuario: ").strip()
            usuario = buscar_usuario_por_nombre(nombre)

        else:
            print("Opción inválida.")
            return

    except (TypeError, ValueError) as error:
        print(f"No se pudo realizar la búsqueda: {error}")
        return

    except tipos_errores_bd()[1]:
        print("No se pudo consultar la cuenta.")
        return

    if usuario is None:
        print("No se encontró la cuenta.")
    else:
        print(
            f"ID: {usuario.id} | "
            f"Usuario: {usuario.nombre_usuario} | "
            f"Empleado ID: {usuario.empleado_id}"
        )


def solicitar_id_usuario():
    while True:
        try:
            id_usuario = int(input("ID de la cuenta: "))

            if id_usuario > 0:
                return id_usuario

            print("El ID debe ser positivo.")

        except ValueError:
            print("Ingresa un número entero válido.")


def modificar_cuenta():
    IntegrityError, OperationalError = tipos_errores_bd()

    id_usuario = solicitar_id_usuario()

    try:
        usuario = buscar_usuario_por_id(id_usuario)
    except (TypeError, ValueError):
        print("ID inválido.")
        return
    except OperationalError:
        print("No se pudo consultar la cuenta.")
        return

    if usuario is None:
        print("No existe una cuenta con ese ID.")
        return

    print(f"\nCuenta seleccionada: {usuario.nombre_usuario}")
    print("1. Cambiar nombre de usuario")
    print("2. Cambiar contraseña")
    print("3. Cambiar ambos datos")
    print("0. Volver")

    opcion = input("Opción: ").strip()

    nuevo_nombre = None
    nueva_clave = None

    if opcion in ("1", "3"):
        nuevo_nombre = input("Nuevo nombre de usuario: ").strip()

    if opcion in ("2", "3"):
        print(
            f"La contraseña debe tener al menos "
            f"{Usuario.MIN_CLAVE} caracteres."
        )
        nueva_clave = solicitar_clave_nueva()

    if opcion == "0":
        return

    if opcion not in ("1", "2", "3"):
        print("Opción inválida.")
        return

    try:
        filas = actualizar_usuario(
            id_usuario,
            nuevo_nombre=nuevo_nombre,
            nueva_clave=nueva_clave
        )

    except (TypeError, ValueError) as error:
        print(f"No se pudo actualizar la cuenta: {error}")

    except IntegrityError:
        print("Ese nombre de usuario ya está registrado.")

    except OperationalError:
        print("No se pudo actualizar la cuenta.")

    else:
        if filas:
            print("Cuenta actualizada correctamente.")
        else:
            print("No se realizaron cambios.")


def eliminar_cuenta(usuario_actual):
    _, OperationalError = tipos_errores_bd()

    id_usuario = solicitar_id_usuario()

    if id_usuario == usuario_actual.id:
        print("No puedes eliminar la cuenta con la que iniciaste sesión.")
        return

    try:
        usuario = buscar_usuario_por_id(id_usuario)
    except (TypeError, ValueError):
        print("ID inválido.")
        return
    except OperationalError:
        print("No se pudo consultar la cuenta.")
        return

    if usuario is None:
        print("No existe una cuenta con ese ID.")
        return

    print(f"Cuenta seleccionada: {usuario.nombre_usuario}")
    confirmacion = input("¿Confirmas su eliminación? (S/N): ").strip().lower()

    if confirmacion != "s":
        print("Eliminación cancelada.")
        return

    try:
        filas = eliminar_usuario(id_usuario)
    except (TypeError, ValueError) as error:
        print(f"No se pudo eliminar la cuenta: {error}")
    except OperationalError:
        print("No se pudo eliminar la cuenta.")
    else:
        if filas:
            print("Cuenta eliminada correctamente.")
        else:
            print("No se encontró la cuenta para eliminar.")


def menu_administrar_usuarios(usuario_actual):
    if usuario_actual is None or usuario_actual.nombre_usuario != "admin":
        print("Acceso denegado. Solo el administrador puede gestionar cuentas.")
        return

    while True:
        print("\n=== ADMINISTRACIÓN DE USUARIOS ===")
        print("1. Listar cuentas")
        print("2. Buscar cuenta")
        print("3. Modificar cuenta")
        print("4. Eliminar cuenta")
        print("0. Volver")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            mostrar_usuarios()
        elif opcion == "2":
            buscar_cuenta()
        elif opcion == "3":
            modificar_cuenta()
        elif opcion == "4":
            eliminar_cuenta(usuario_actual)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_acceso():
    intentos = 0

    while True:
        print("\n=== ACCESO A ECOTECH ===")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Cargar datos de ejemplo (semillas)")
        print("0. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            usuario = solicitar_login()

            if usuario is not None:
                return usuario

            intentos += 1

            if intentos >= MAX_INTENTOS:
                print(
                    "Demasiados intentos. "
                    "Cierra y vuelve a abrir el programa."
                )
                return None

        elif opcion == "2":
            registrar_cuenta()

        
        elif opcion == "3":
            cargar_datos_de_ejemplo()

            from persistencia.semillas import asegurar_admin_inicial

            try:
                asegurar_admin_inicial()
            except (TypeError, ValueError) as error:
                print(f"No se pudo crear el administrador inicial: {error}")
            except tipos_errores_bd()[1]:
                print("No se pudo crear el administrador inicial.")

        elif opcion == "0":
            print("Saliendo de EcoTech.")
            return None

        else:
            print("Elige una opción entre 0 y 3.")
