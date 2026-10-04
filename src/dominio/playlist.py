"""class Playlist:
    def __init__(self , id  ):
        self.id = id
   """
from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError


class Playlist:
    """Colección principal de la biblioteca musical con un tope máximo."""

    def __init__(self, tope=10):
        self._canciones = ListaEnlazada()
        self._tope = tope

    def agregar(self, cancion):
        """Agrega una canción a la playlist si no supera el tope."""
        if self._canciones.tamanio() >= self._tope:
            raise ColeccionLlenaError(
                f"La playlist está llena (máximo {self._tope} canciones)."
            )
        self._canciones.insertar_al_final(cancion)

    def eliminar(self, cancion):
        """Elimina una canción de la playlist."""
        self._canciones.eliminar(cancion)

    def listar(self):
        """Devuelve o recorre las canciones usando el iterador de la lista enlazada."""
        for cancion in self._canciones:
            print(f"🎵 {cancion}")

    def esta_vacia(self):
        return self._canciones.esta_vacia()

    def tamanio(self):
        return self._canciones.tamanio()    