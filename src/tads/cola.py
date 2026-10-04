"""class Cola:
    TAD cola implementado sobre ListaEnlazada.

    def __init__(self):
        raise NotImplementedError

    def encolar(self, dato):
        raise NotImplementedError

    def desencolar(self):
        raise NotImplementedError

    def ver_frente(self):
        raise NotImplementedError

    def esta_vacia(self):
        raise NotImplementedError
"""
from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColaVaciaError


class Cola:
    """TAD cola implementado sobre ListaEnlazada."""

    def __init__(self):
        self._items = ListaEnlazada()

    def encolar(self, dato):
        
        self._items.insertar_al_final(dato)

    def desencolar(self):
     
        if self.esta_vacia():
            raise ColaVaciaError(
                "La cola está vacía."
            )

        frente = self._items._cabeza.dato
        self._items.eliminar(frente)
        return frente

    def ver_frente(self):
        
        if self.esta_vacia():
            raise ColaVaciaError(
                "La cola está vacía."
            )

        return self._items._cabeza.dato

    def esta_vacia(self):
        
        return self._items.esta_vacia()