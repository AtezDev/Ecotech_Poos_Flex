from getpass import getpass
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_empleado import solicitar_id, tipos_errores_bd
from presentacion.menu_principal import cargar_datos_de_ejemplo
from servicios.autenticacion import autenticar, registrar_usuario

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
    print(f"La contraseña debe tener al menos {Usuario.MIN_CLAVE} caracteres.")
    clave = solicitar_clave_nueva()
    try:
        usuario = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(f"No se pudo crear la cuenta: {error}")
    except IntegrityError:
        print("No se pudo crear la cuenta: ese usuario o ese empleado ya tienen una cuenta.")
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


def menu_acceso():
    intentos = 0
    while True:
        print("\n=== ACCESO A ECOTECH ===")
        print("1. Iniciar sesión\n2. Crear cuenta")
        print("3. Cargar datos de ejemplo (semillas)\n0. Salir")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            usuario = solicitar_login()
            if usuario is not None:
                return usuario
            intentos += 1
            if intentos >= MAX_INTENTOS:
                print("Demasiados intentos. Cierra y vuelve a abrir el programa.")
                return None
        elif opcion == "2":
            registrar_cuenta()
        elif opcion == "3":
            cargar_datos_de_ejemplo()
        elif opcion == "0":
            print("Saliendo de EcoTech.")
            return None
        else:
            print("Elige una opción entre 0 y 3.")
