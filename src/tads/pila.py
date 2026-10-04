"""class Pila:
   TAD pila implementado sobre ListaEnlazada.

    def __init__(self):
        raise NotImplementedError

    def apilar(self, dato):
        raise NotImplementedError

    def desapilar(self):
        raise NotImplementedError

    def ver_tope(self):
        raise NotImplementedError

    def esta_vacia(self):
        raise NotImplementedError
"""
from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import PilaVaciaError


class Pila:
    """TAD pila implementado sobre ListaEnlazada."""

    def __init__(self):
        self._items = ListaEnlazada()

    def apilar(self, dato):
        """Agrega un elemento al tope de la pila."""
        self._items.insertar_al_inicio(dato)

    def desapilar(self):
        """Saca y devuelve el elemento que está en el tope."""
        if self.esta_vacia():
            raise PilaVaciaError(
                "No hay acciones en el historial para deshacer."
            )

        tope = self._items._cabeza.dato
        self._items.eliminar(tope)

        return tope

    def ver_tope(self):
        """Devuelve el elemento del tope sin sacarlo."""
        if self.esta_vacia():
            raise PilaVaciaError(
                "La pila del historial está vacía."
            )

        return self._items._cabeza.dato

    def esta_vacia(self):
        """Devuelve True si la pila está vacía."""
        return self._items.esta_vacia()