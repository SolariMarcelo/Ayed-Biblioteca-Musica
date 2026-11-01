"""def busqueda_lineal(coleccion, clave, obtener_clave):
    #Devuelve el ítem cuya clave coincide, o None.
    raise NotImplementedError


def busqueda_binaria(coleccion_ordenada, clave, obtener_clave):
    #La colección tiene que estar ordenada por obtener_clave.
    raise NotImplementedError
"""

def busqueda_lineal(coleccion, clave, obtener_clave=None):
    """
    Busca un elemento recorriendo la colección de principio a fin.

    Devuelve el elemento encontrado o None si no existe.
    """

    for elemento in coleccion:

        if obtener_clave is None:
            if elemento == clave:
                return elemento

        elif obtener_clave(elemento) == clave:
            return elemento

    return None
"""
Prueba

from src.algoritmos.busqueda import busqueda_lineal

canciones = ["Crimen", "Persiana Americana", "De Música Ligera"]

resultado = busqueda_lineal(canciones, "Persiana Americana")

if resultado is not None:
    print("Encontrada:", resultado)
else:
    print("Canción no encontrada")

resultado = busqueda_lineal(
    canciones,
    "Crimen",
    obtener_clave=lambda cancion: cancion.titulo
)
"""
def busqueda_binaria(coleccion, clave, obtener_clave):
    """
    Busca un elemento mediante búsqueda binaria.

    IMPORTANTE: la colección debe estar ordenada
    por el mismo criterio que se utiliza para buscar.
    """

    izquierda = 0
    derecha = len(coleccion) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        valor = obtener_clave(coleccion[medio])

        if valor == clave:
            return coleccion[medio]

        elif valor < clave:
            izquierda = medio + 1

        else:
            derecha = medio - 1

    return None
"""
Prueba 
from src.algoritmos.busqueda import busqueda_binaria

canciones = [
    "Afuera",
    "Crimen",
    "De Música Ligera",
    "Persiana Americana",
    "Prófugos"
]

resultado = busqueda_binaria(
    canciones,
    "Persiana Americana",
    obtener_clave=lambda cancion: cancion
)

if resultado is not None:
    print("Encontrada:", resultado)
else:
    print("Canción no encontrada")
    """