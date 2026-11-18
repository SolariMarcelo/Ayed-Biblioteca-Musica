from src.config import TEMA
import os
from src.dominio.cancion  import CATALOGO, Cancion
from src.dominio.biblioteca  import VERSION, Biblioteca

from src.excepciones import (
    ColeccionLlenaError,
    ColeccionVaciaError,
    PilaVaciaError,
    ColaVaciaError,
    ItemNoEncontradoError,
    ArchivoInvalidoError,
)
from src.persistencia.binario import (
    guardar_binario,
    cargar_binario,
    actualizar_registro,
)

RUTA_BINARIO = os.path.join("data", "catalogo.bin")

from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.algoritmos.busqueda import (
    busqueda_lineal,
    busqueda_binaria
)

from src.algoritmos.ordenamiento import (
    ordenar_seleccion,
    ordenar_insercion
)





TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


#def pendiente():
#    print("Todavía no está implementado. Completar en la entrega que corresponde.")


def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (equipo / menú / playlist)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    
    print("0. Salir")

#SUBMENU OPCION 3 BUSCAR-------------------------------------------------------------------------------------------------------
def menu_buscar():
    print("\n--- Buscar canciones ---")
    print("1. Buscar por ID (lineal)")
    print("2. Buscar por título (lineal)")
    print("3. Buscar por artista (lineal)")
    print("4. Buscar por ID (binaria)")

    opcion = input("> ").strip()

    if opcion == "1":
        clave = input("Ingresá el ID: ").strip()

        try:
            clave = int(clave)
        except ValueError:
            print("El ID debe ser un número.")
            return

        resultado = busqueda_lineal(
            CATALOGO,
            clave,
            obtener_clave=lambda cancion: cancion["id"]
        )

    elif opcion == "2":
        clave = input("Ingresá el título: ").strip().lower()

        resultado = busqueda_lineal(
            CATALOGO,
            clave,
            obtener_clave=lambda cancion: cancion["titulo"].lower()
        )

    elif opcion == "3":
        clave = input("Ingresá el artista: ").strip().lower()

        resultado = busqueda_lineal(
            CATALOGO,
            clave,
            obtener_clave=lambda cancion: cancion["artista"].lower()
        )

    elif opcion == "4":
        clave = input("Ingresá el ID: ").strip()

        try:
            clave = int(clave)
        except ValueError:
            print("El ID debe ser un número.")
            return

        resultado = busqueda_binaria(
            CATALOGO,
            clave,
            obtener_clave=lambda cancion: cancion["id"]
        )

    else:
        print("Opción inválida.")
        return

    if resultado is None:
        print("Canción no encontrada.")
    else:
        print("\nCanción encontrada:")
        print(f"ID: {resultado['id']}")
        print(f"Título: {resultado['titulo']}")
        print(f"Artista: {resultado['artista']}")
        print(f"Álbum: {resultado['album']}")
        print(f"Género: {resultado['genero']}")
        print(f"Año: {resultado['anio']}")
        print(f"Duración: {resultado['duracion_seg']} segundos")

#SUBMENU OPCION 4 ORDENAR------------------------------------------------------------------------------------------------
def menu_ordenar():
    print("\n--- Ordenar catálogo ---")
    print("1. Selección")
    print("2. Inserción")

    algoritmo = input("Elegí el algoritmo: ").strip()

    print("\nCriterio de ordenamiento:")
    print("1. Título")
    print("2. Artista")
    print("3. Año")

    criterio = input("Elegí el criterio: ").strip()

    claves = {
        "1": lambda cancion: cancion["titulo"].lower(),
        "2": lambda cancion: cancion["artista"].lower(),
        "3": lambda cancion: cancion["anio"]
    }

    if algoritmo not in {"1", "2"}:
        print("Algoritmo inválido.")
        return

    if criterio not in claves:
        print("Criterio inválido.")
        return

    catalogo_ordenado = CATALOGO.copy()
    obtener_clave = claves[criterio]

    if algoritmo == "1":
        ordenar_seleccion(catalogo_ordenado, obtener_clave)
        nombre_algoritmo = "Selección"
    else:
        ordenar_insercion(catalogo_ordenado, obtener_clave)
        nombre_algoritmo = "Inserción"

    print(f"\nCatálogo ordenado por {nombre_algoritmo}:")
    for cancion in catalogo_ordenado:
        print(
            f"{cancion['titulo']} - "
            f"{cancion['artista']} - "
            f"{cancion['anio']}"
        )

# GESTION PERSISTENTE DEL CATALOGO (5.4) ----------------------------------------
def _guardar_catalogo_binario():
    """Guarda el catálogo actual en el archivo binario persistente."""
    guardar_binario(RUTA_BINARIO, CATALOGO)


def _pedir_entero(mensaje, minimo=0, maximo=4294967295):
    """Solicita un entero dentro del rango permitido por el formato binario."""
    valor = input(mensaje).strip()
    try:
        numero = int(valor)
    except ValueError as error:
        raise ValueError("Ingresá un número entero válido.") from error

    if numero < minimo or numero > maximo:
        raise ValueError(f"El valor debe estar entre {minimo} y {maximo}.")
    return numero


def _buscar_posicion_por_id(id_cancion):
    """Devuelve la posición de una canción según su ID, o None si no existe."""
    for posicion, cancion in enumerate(CATALOGO):
        if cancion["id"] == id_cancion:
            return posicion
    return None


def _alta_cancion():
    """Agrega una canción y persiste el catálogo completo."""
    ids = [cancion["id"] for cancion in CATALOGO]
    nuevo_id = max(ids, default=0) + 1
    if nuevo_id > 4294967295:
        print("No se puede generar otro ID: se alcanzó el máximo permitido.")
        return

    print("\n--- Alta de canción ---")
    print(f"ID asignado automáticamente: {nuevo_id}")
    try:
        nueva = {
            "id": nuevo_id,
            "titulo": input("Título: ").strip(),
            "artista": input("Artista: ").strip(),
            "album": input("Álbum: ").strip(),
            "anio": _pedir_entero("Año: ", 0, 65535),
            "genero": input("Género: ").strip(),
            "duracion_seg": _pedir_entero("Duración en segundos: ", 0),
        }
        if not all(nueva[campo] for campo in ("titulo", "artista", "album", "genero")):
            print("Los campos de texto no pueden quedar vacíos.")
            return

        CATALOGO.append(nueva)
        try:
            _guardar_catalogo_binario()
        except ArchivoInvalidoError:
            CATALOGO.pop()
            raise
        print(f"Canción '{nueva['titulo']}' agregada y guardada correctamente.")
    except (ValueError, ArchivoInvalidoError) as error:
        print(f"No se pudo agregar la canción: {error}")


def _baja_cancion():
    """Elimina una canción por ID y persiste el catálogo completo."""
    print("\n--- Baja de canción ---")
    try:
        id_cancion = _pedir_entero("ID de la canción que querés eliminar: ", 0)
        posicion = _buscar_posicion_por_id(id_cancion)
        if posicion is None:
            print("No existe una canción con ese ID.")
            return

        eliminada = CATALOGO.pop(posicion)
        try:
            _guardar_catalogo_binario()
        except ArchivoInvalidoError:
            CATALOGO.insert(posicion, eliminada)
            raise
        print(f"Canción '{eliminada['titulo']}' eliminada y cambio guardado.")
    except (ValueError, ArchivoInvalidoError) as error:
        print(f"No se pudo eliminar la canción: {error}")


def _modificar_cancion():
    """Modifica los campos de una canción y actualiza su registro con seek()."""
    print("\n--- Modificación de canción ---")
    try:
        id_cancion = _pedir_entero("ID de la canción que querés modificar: ", 0)
        posicion = _buscar_posicion_por_id(id_cancion)
        if posicion is None:
            print("No existe una canción con ese ID.")
            return

        actual = CATALOGO[posicion]
        print("Dejá vacío un campo para conservar su valor actual.")
        modificada = actual.copy()
        for campo, etiqueta in (("titulo", "Título"), ("artista", "Artista"),
                                ("album", "Álbum"), ("genero", "Género")):
            valor = input(f"{etiqueta} [{actual[campo]}]: ").strip()
            if valor:
                modificada[campo] = valor

        anio = input(f"Año [{actual['anio']}]: ").strip()
        if anio:
            modificada["anio"] = int(anio)
            if not 0 <= modificada["anio"] <= 65535:
                raise ValueError("El año debe estar entre 0 y 65535.")

        duracion = input(
            f"Duración en segundos [{actual['duracion_seg']}]: "
        ).strip()
        if duracion:
            modificada["duracion_seg"] = int(duracion)
            if not 0 <= modificada["duracion_seg"] <= 4294967295:
                raise ValueError("La duración está fuera del rango permitido.")

        # El ID no se modifica: identifica de manera estable a la canción.
        actualizar_registro(RUTA_BINARIO, posicion, modificada)
        CATALOGO[posicion] = modificada
        print("Canción modificada y guardada correctamente.")
    except (ValueError, ArchivoInvalidoError) as error:
        print(f"No se pudo modificar la canción: {error}")


def menu_gestion_catalogo():
    """Submenú de alta, baja y modificación persistente."""
    print("\n--- Gestión persistente del catálogo ---")
    print("1. Alta de canción")
    print("2. Baja de canción")
    print("3. Modificar canción")
    print("0. Volver")
    opcion = input("> ").strip()

    if opcion == "1":
        _alta_cancion()
    elif opcion == "2":
        _baja_cancion()
    elif opcion == "3":
        _modificar_cancion()
    elif opcion != "0":
        print("Opción inválida.")


#MAIN----------------------------------------------------------------------------------------------------------------------
def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return
    # Si ya existe un catálogo binario, lo usamos como fuente persistente.
    # Si todavía no existe, se conserva el catálogo inicial del proyecto.
    if os.path.exists(RUTA_BINARIO):
        try:
            catalogo_guardado = cargar_binario(RUTA_BINARIO)
            CATALOGO[:] = catalogo_guardado
            print(f"Catálogo binario cargado: {len(CATALOGO)} canciones.")
        except ArchivoInvalidoError as error:
            print(f"No se pudo cargar el catálogo binario: {error}")
            print("Se mantiene el catálogo inicial en memoria; no se sobrescribe el archivo.")
    else:
        # Primera ejecución: se crea el binario a partir del catálogo inicial.
        try:
            guardar_binario(RUTA_BINARIO, CATALOGO)
            print("Se creó el archivo binario inicial del catálogo.")
        except ArchivoInvalidoError as error:
            print(f"No se pudo crear el catálogo binario: {error}")

    playlist = Playlist(tope=5)      # Colección principal con límite de 5 canciones
    historial = Pila()               # Historial de acciones / deshacer (Pila)
    cola_reproduccion = Cola()       # Cola de reproducción de temas (Cola)

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "1":
            #Cancion.listar_catalogo()
            print("\n--- Catálogo de Canciones ---")
            try:
                for cancion in CATALOGO:
                    print(cancion)
            except Exception as e:
                print(f"Error al listar: {e}")
        
        
        if opcion == "3":
            menu_buscar()

        
        if opcion == "4":
            menu_ordenar()

        if opcion == "5":
            biblioteca = Biblioteca()

            id_cancion = 1 #prueba con la id 1

            resultado = biblioteca.versiones_de(id_cancion)

            for version in resultado:
                print(
                    "Versión ID:",
                    version["cancion_id"],
                    "- Tipo:",
                    version["tipo"]
                )
        if opcion == "6":
            # Opción 6: Colección principal con tope
            print("\n--- Gestión de Playlist ---")
            print("1. Agregar canción")
            print("2. Ver playlist")
            print("3. Simular llenado (Prueba P05)")
            sub = input("> ").strip()

            if sub == "1":
                titulo = input("Nombre de la canción: ").strip()
                try:
                    playlist.agregar(titulo)
                    # Apilamos en el historial como acción realizada
                    historial.apilar(f"Agregó '{titulo}'")
                    print(f" Canción agregada con éxito.")
                except ColeccionLlenaError as e:
                    # Ítem 3.6: Captura específica de ColeccionLlenaError
                    print(f"error {e}")
            elif sub == "2":
                print("\n[Contenido de la Playlist]:")
                playlist.listar()
            elif sub == "3":
                # Prueba automática del caso P05 (llenar hasta el tope)
                try:
                    for i in range(1, 7):
                        playlist.agregar(f"Tema de prueba {i}")
                except ColeccionLlenaError as e:
                    print(f"error {e} (Caso P05 superado con éxito)")

        if opcion == "7":
            # Opción 7: Historial / Deshacer (Pila)
            print("\n--- Historial de Acciones (Pila) ---")
            try:
                accion_deshecha = historial.desapilar()
                print(f" Acción deshecha: {accion_deshecha}")
            except PilaVaciaError as e:
                # Ítem 3.6: Captura estricta de PilaVaciaError (Nunca except pelado)
                print(f"❌ {e}")

        if opcion == "8":
            # Opción 8: Cola de reproducción (Cola)
            print("\n--- Cola de Reproducción ---")
            print("1. Encolar tema")
            print("2. Reproducir siguiente (Desencolar)")
            sub = input("> ").strip()

            if sub == "1":
                tema = input("Tema a encolar: ").strip()
                cola_reproduccion.encolar(tema)
                print(f"Tema encolado en la cola de reproducción.")
            elif sub == "2":
                try:
                    siguiente = cola_reproduccion.desencolar()
                    print(f" Reproduciendo ahora: {siguiente}")
                except ColaVaciaError as e:
                    # Ítem 3.6: Captura estricta de ColaVaciaError
                    print(f"Error {e}")       
                
       

        elif opcion == "9":
            print("\n--- Guardar / cargar archivos ---")
            print("1. Guardar catálogo binario")
            print("2. Cargar catálogo binario")
            print("3. Gestion persistente del catalogo")
            sub = input("> ").strip()
            try:
                if sub == "1":
                    _guardar_catalogo_binario()
                    print("Catálogo guardado correctamente.")
                elif sub == "2":
                    CATALOGO[:] = cargar_binario(RUTA_BINARIO)
                    print(f"Catálogo cargado: {len(CATALOGO)} canciones.")
                elif sub == "3":
                            menu_gestion_catalogo()
                elif sub != "":
                    print("Opción inválida.")
            except ArchivoInvalidoError as error:
                print(f"Error de persistencia: {error}")

        elif opcion == "0":
            print("Chau.")
        
        elif opcion == "2":
            print("")

        elif opcion not in {"1", "3", "4", "5", "6", "7"}:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
