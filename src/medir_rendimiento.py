from time import perf_counter

from src.dominio.cancion import CATALOGO
from src.algoritmos.busqueda import (
    busqueda_lineal,
    busqueda_binaria
)
from src.algoritmos.ordenamiento import (
    ordenar_seleccion,
    ordenar_insercion
)


def crear_catalogo_ampliado(cantidad):
    datos = []

    for i in range(cantidad):
        cancion = CATALOGO[i % len(CATALOGO)].copy()
        cancion["id"] = i + 1
        datos.append(cancion)

    return datos


def medir_busqueda(funcion, datos, clave, obtener_clave):
    repeticiones = 1000
    inicio = perf_counter()

    for _ in range(repeticiones):
        funcion(datos, clave, obtener_clave)

    fin = perf_counter()

    return (fin - inicio) / repeticiones


def medir_ordenamiento(funcion, datos, obtener_clave):
    repeticiones = 5
    tiempo_total = 0

    for _ in range(repeticiones):
        copia = datos.copy()

        inicio = perf_counter()
        funcion(copia, obtener_clave)
        fin = perf_counter()

        tiempo_total += fin - inicio

    return tiempo_total / repeticiones


def probar_tamanio(datos, nombre):
    print(f"\n--- {nombre}: {len(datos)} canciones ---")

    clave_id = lambda cancion: cancion["id"]

    # Búsquedas: se busca un ID inexistente para recorrer
    # toda la colección o llegar al extremo del rango.
    id_inexistente = len(datos) + 100

    tiempo_lineal = medir_busqueda(
        busqueda_lineal,
        datos,
        id_inexistente,
        clave_id
    )

    tiempo_binaria = medir_busqueda(
        busqueda_binaria,
        datos,
        id_inexistente,
        clave_id
    )

    print(f"Búsqueda lineal: {tiempo_lineal:.8f} segundos")
    print(f"Búsqueda binaria: {tiempo_binaria:.8f} segundos")

    # Ordenamientos: usamos una copia invertida para que
    # ambos algoritmos reciban los mismos datos.
    datos_invertidos = datos.copy()
    datos_invertidos.reverse()

    tiempo_seleccion = medir_ordenamiento(
        ordenar_seleccion,
        datos_invertidos,
        clave_id
    )

    tiempo_insercion = medir_ordenamiento(
        ordenar_insercion,
        datos_invertidos,
        clave_id
    )

    print(f"Ordenamiento selección: {tiempo_seleccion:.8f} segundos")
    print(f"Ordenamiento inserción: {tiempo_insercion:.8f} segundos")


catalogo_grande = crear_catalogo_ampliado(500)

probar_tamanio(CATALOGO, "Catálogo original")
probar_tamanio(catalogo_grande, "Catálogo ampliado")