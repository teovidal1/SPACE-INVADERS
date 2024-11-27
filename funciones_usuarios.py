import json


def cargar_usuarios(ruta = "data/datos_usuarios.json") -> list[dict]:
    """
    Carga una lista de usuarios desde un archivo JSON.

    Args:
        ruta (str, optional): La ruta del archivo JSON. Predefinida en "datos_usuarios.json".

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un usuario y contiene sus datos. 
    """
    with open (ruta) as contenido:
        jugadores = json.load(contenido)
    return jugadores


def guardar_usuarios (jugadores: list[dict], ruta = "data/datos_usuarios.json", ):
    """Guarda los datos de una lista de diccionarios en un json.

    Args:
        jugadores (list)
        ruta (str, optional): Defaults to "datos_usuarios.json".
    """

    with open (ruta, "w") as contenido:
        json.dump(jugadores, contenido, indent = 4)


def buscar_indice_usuario_en_lista(jugadores: list[dict], nombre_usuario :str) -> int | None:
    """Busca un nombre(str) en la clave "nombre" de todos los diccionarios de una lista y retorna la posición del diccionario si lo encuentra.

    Args:
        jugadores (list): list[dict]
        nombre_usuario (str)

    Returns:
        int: Índice del diccionario en el que encuentra el nombre
    """
    for i in range (len(jugadores)):
        if "nombre" in jugadores[i]:
            if jugadores[i]["nombre"] == nombre_usuario:
                indice_usuario_actual = i
                return indice_usuario_actual
    return None