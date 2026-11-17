from dominio.registro_tiempo import RegistroTiempo
from presentacion.menu_empleado import solicitar_id_de, tipos_errores_bd


def validar_texto_obligatorio(texto):
    texto = texto.strip()
    if not texto:
        raise ValueError("Este dato es obligatorio.")
    return texto


def validar_horas(texto):
    texto = texto.strip()
    if not texto.replace(".", "", 1).isdigit():
        raise ValueError("Escribe solo números: 3 o 3.5.")
    horas = float(texto)
    if not RegistroTiempo.validarHoras(horas):
        raise ValueError("Las horas deben ser mayores que cero.")
    return horas


def confirmar(pregunta):
    while True:
        respuesta = input(f"{pregunta} (s/n): ").strip().lower()
        if respuesta == "s":
            return True
        if respuesta == "n":
            return False
        print("Responde s o n.")


def listar_todo(listar, texto_vacio):
    _, OperationalError = tipos_errores_bd()
    try:
        objetos = listar()
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not objetos:
            print(texto_vacio)
        for objeto in objetos:
            print(objeto.mostrar_datos())


def buscar_uno(entidad, buscar):
    id_entidad = solicitar_id_de(entidad)
    _, OperationalError = tipos_errores_bd()
    try:
        objeto = buscar(id_entidad)
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if objeto is None:
            print(f"No existe {entidad} con ese ID.")
        else:
            print(objeto.mostrar_datos())


def eliminar_con_confirmacion(entidad, buscar, eliminar):
    id_entidad = solicitar_id_de(entidad)
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        objeto = buscar(id_entidad)
        if objeto is None:
            print(f"No existe {entidad} con ese ID.")
            return
        print(objeto.mostrar_datos())
        if not confirmar(f"¿Eliminar {entidad}?"):
            print("Eliminación cancelada.")
            return
        filas = eliminar(id_entidad)
    except IntegrityError:
        print("No se puede eliminar: tiene relaciones u otra restricción.")
    except OperationalError:
        print("No se pudo completar la eliminación.")
    else:
        if filas == 1:
            print("Eliminado correctamente.")
        else:
            print("No se eliminó: vuelve a consultar el ID.")
