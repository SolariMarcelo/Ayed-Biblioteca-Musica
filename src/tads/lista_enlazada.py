"""class ListaEnlazada:
   TAD lista enlazada simple. No usar list de Python por debajo.

    def __init__(self):
        raise NotImplementedError

    def esta_vacia(self):
        raise NotImplementedError

    def tamanio(self):
        raise NotImplementedError

    def insertar_al_inicio(self, dato):
        raise NotImplementedError

    def insertar_al_final(self, dato):
        raise NotImplementedError

    def insertar_ordenado(self, dato, clave):
        raise NotImplementedError

    def eliminar(self, dato):
        raise NotImplementedError

    def buscar(self, dato):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError
"""
from src.tads.nodo import Nodo


class ListaEnlazada:
   

    def __init__(self):
        self._cabeza = None
        self._tamanio = 0

    def esta_vacia(self):
        
        return self._cabeza is None

    def tamanio(self):
    
        return self._tamanio

    def insertar_al_inicio(self, dato):
      
        nuevo = Nodo(dato, self._cabeza)
        self._cabeza = nuevo
        self._tamanio += 1

    def insertar_al_final(self, dato):
      
        nuevo = Nodo(dato)

        if self.esta_vacia():
            self._cabeza = nuevo
        else:
            actual = self._cabeza

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo

        self._tamanio += 1

    def insertar_ordenado(self, dato, clave):
        #Inserta un elemento manteniendo la lista ordenada.
        nuevo = Nodo(dato)

        # Lista vacía
        if self.esta_vacia():
            self._cabeza = nuevo
            self._tamanio += 1
            return

        # Va antes de la cabeza
        if clave(dato) <= clave(self._cabeza.dato):
            nuevo.siguiente = self._cabeza
            self._cabeza = nuevo
            self._tamanio += 1
            return

        # Buscar dónde insertar
        actual = self._cabeza

        while (
            actual.siguiente is not None
            and clave(actual.siguiente.dato) < clave(dato)
        ):
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        self._tamanio += 1

    def eliminar(self, dato):
        
        if self.esta_vacia():
            return

        # El dato está en la cabeza
        if self._cabeza.dato == dato:
            self._cabeza = self._cabeza.siguiente
            self._tamanio -= 1
            return

        # Buscar el nodo anterior
        actual = self._cabeza

        while actual.siguiente is not None:
            if actual.siguiente.dato == dato:
                actual.siguiente = actual.siguiente.siguiente
                self._tamanio -= 1
                return

            actual = actual.siguiente

    def buscar(self, dato):
       
        actual = self._cabeza

        while actual is not None:
            if actual.dato == dato:
                return actual

            actual = actual.siguiente

        return None

    def __iter__(self):
      
        actual = self._cabeza

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente