"""def ordenar_seleccion(coleccion, clave):
   # Ordenamiento por selección. Devuelve una nueva secuencia, no usa sorted.
    raise NotImplementedError


def ordenar_insercion(coleccion, clave):
    #Ordenamiento por inserción. Devuelve una nueva secuencia, no usa sorted.
    raise NotImplementedError
"""
def ordenar_seleccion(coleccion, obtener_clave):
    n = len(coleccion)

    for i in range(n - 1):
        posicion_menor = i

        for j in range(i + 1, n):
            if obtener_clave(coleccion[j]) < obtener_clave(coleccion[posicion_menor]):
                posicion_menor = j

        coleccion[i], coleccion[posicion_menor] = (
            coleccion[posicion_menor],
            coleccion[i]
        )

    return coleccion


def ordenar_insercion(coleccion, obtener_clave):
    for i in range(1, len(coleccion)):
        actual = coleccion[i]
        j = i - 1

        while j >= 0 and obtener_clave(coleccion[j]) > obtener_clave(actual):
            coleccion[j + 1] = coleccion[j]
            j -= 1

        coleccion[j + 1] = actual

    return coleccion


"""
#prueba--------------------------------------------------------------------------------
from src.dominio.cancion import CATALOGO
from src.algoritmos.ordenamiento import (
    ordenar_seleccion,
    ordenar_insercion
)

# Creamos copias para no modificar el catálogo original.
catalogo_seleccion = CATALOGO.copy()
catalogo_insercion = CATALOGO.copy()

ordenar_seleccion(
    catalogo_seleccion,
    obtener_clave=lambda cancion: cancion["titulo"].lower()
)

ordenar_insercion(
    catalogo_insercion,
    obtener_clave=lambda cancion: cancion["anio"]
)

print("Primeras canciones ordenadas por título:")
for cancion in catalogo_seleccion[:5]:
    print(cancion["titulo"])

print("\nPrimeras canciones ordenadas por año:")
for cancion in catalogo_insercion[:5]:
    print(cancion["titulo"], "-", cancion["anio"])
    
    """