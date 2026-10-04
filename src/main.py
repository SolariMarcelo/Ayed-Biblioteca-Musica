from src.config import TEMA
from src.dominio.cancion  import CATALOGO, Cancion
from src.dominio.biblioteca  import VERSION, Biblioteca
# 1. Importamos las excepciones propias y las clases de TADs / Dominio
from src.excepciones import (
    ColeccionLlenaError,
    ColeccionVaciaError,
    PilaVaciaError,
    ColaVaciaError,
    ItemNoEncontradoError,
)
from src.dominio.playlist import Playlist
from src.tads.pila import Pila
from src.tads.cola import Cola





TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}


def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")


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


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return
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
        elif opcion == "6":
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
                    print(f"✅ Canción agregada con éxito.")
                except ColeccionLlenaError as e:
                    # Ítem 3.6: Captura específica de ColeccionLlenaError
                    print(f"❌ {e}")
            elif sub == "2":
                print("\n[Contenido de la Playlist]:")
                playlist.listar()
            elif sub == "3":
                # Prueba automática del caso P05 (llenar hasta el tope)
                try:
                    for i in range(1, 7):
                        playlist.agregar(f"Tema de prueba {i}")
                except ColeccionLlenaError as e:
                    print(f"❌ {e} (Caso P05 superado con éxito)")

        elif opcion == "7":
            # Opción 7: Historial / Deshacer (Pila)
            print("\n--- Historial de Acciones (Pila) ---")
            try:
                accion_deshecha = historial.desapilar()
                print(f"↩️ Acción deshecha: {accion_deshecha}")
            except PilaVaciaError as e:
                # Ítem 3.6: Captura estricta de PilaVaciaError (Nunca except pelado)
                print(f"❌ {e}")

        elif opcion == "8":
            # Opción 8: Cola de reproducción (Cola)
            print("\n--- Cola de Reproducción ---")
            print("1. Encolar tema")
            print("2. Reproducir siguiente (Desencolar)")
            sub = input("> ").strip()

            if sub == "1":
                tema = input("Tema a encolar: ").strip()
                cola_reproduccion.encolar(tema)
                print(f"▶️ Tema encolado en la cola de reproducción.")
            elif sub == "2":
                try:
                    siguiente = cola_reproduccion.desencolar()
                    print(f"🎶 Reproduciendo ahora: {siguiente}")
                except ColaVaciaError as e:
                    # Ítem 3.6: Captura estricta de ColaVaciaError
                    print(f"❌ {e}")       
                
        elif opcion == "0":
            print("Chau.")
        elif opcion in { "2","3",  "4", "6", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
