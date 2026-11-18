"""Persistencia binaria de canciones mediante registros de longitud fija.

Formato del archivo (little-endian, sin alineacion automatica):

Header:
    magia      4s   b"AYED"
    tema       c    b"M" (musica)
    cantidad   I    cantidad de registros

Registro de musica:
    id         I
    titulo     80s
    artista    80s
    album      80s
    anio       H
    genero     20s
    duracion   I

El header ocupa 9 bytes y cada registro ocupa 270 bytes.
Los campos de texto se codifican en UTF-8 y se completan con bytes nulos.
"""

import struct

from src.config import TEMA
from src.excepciones import ArchivoInvalidoError


MAGIA = b"AYED"
TEMAS = {
    "pokedex": b"P",
    "recetario": b"R",
    "musica": b"M",
}

FORMATO_HEADER = "<4scI"
FORMATO_REGISTRO = "<I80s80s80sH20sI"

HEADER = struct.Struct(FORMATO_HEADER)
REGISTRO = struct.Struct(FORMATO_REGISTRO)

CAMPOS_TEXTO = {
    "titulo": 80,
    "artista": 80,
    "album": 80,
    "genero": 20,
}


def _codificar_texto(valor, campo, ancho):
    """Codifica un texto UTF-8 y lo completa hasta el ancho fijo."""
    if not isinstance(valor, str):
        raise ValueError(f"El campo {campo} debe ser texto.")

    datos = valor.encode("utf-8")
    if len(datos) > ancho:
        raise ValueError(
            f"El campo {campo} supera el máximo de {ancho} bytes UTF-8."
        )

    return datos.ljust(ancho, b"\0")


def _decodificar_texto(datos):
    """Quita el relleno nulo y decodifica un campo UTF-8."""
    return datos.rstrip(b"\0").decode("utf-8")


def _empaquetar_registro(item):
    """Convierte un diccionario de canción en un registro binario."""
    try:
        return REGISTRO.pack(
            item["id"],
            _codificar_texto(item["titulo"], "titulo", 80),
            _codificar_texto(item["artista"], "artista", 80),
            _codificar_texto(item["album"], "album", 80),
            item["anio"],
            _codificar_texto(item["genero"], "genero", 20),
            item["duracion_seg"],
        )
    except (KeyError, TypeError, ValueError, struct.error) as error:
        raise ArchivoInvalidoError(
            f"No se pudo codificar el registro: {error}"
        ) from error


def _validar_header(archivo):
    """Lee y valida el header. Devuelve la cantidad de registros."""
    datos = archivo.read(HEADER.size)

    if len(datos) != HEADER.size:
        raise ArchivoInvalidoError("El archivo binario es demasiado corto (header incompleto).")

    try:
        magia, tema, cantidad = HEADER.unpack(datos)
    except struct.error as error:
        raise ArchivoInvalidoError("El header del archivo binario está corrupto o tiene un formato inválido.") from error

    # Validación de magia incorrecta (ej: archivo .txt plano o formato desconocido)
    if magia != MAGIA:
        raise ArchivoInvalidoError("Magia incorrecta: el archivo no es un binario válido de AyED (o es un archivo .txt roto/plano).")

    tema_esperado = TEMAS.get(TEMA)
    if tema_esperado is None or tema != tema_esperado:
        raise ArchivoInvalidoError("El tema del archivo binario no coincide con la configuración actual.")

    return cantidad


def guardar_binario(ruta, items):
    """Guarda una lista de canciones en formato binario."""
    if TEMA not in TEMAS:
        raise ArchivoInvalidoError(f"Tema no soportado: {TEMA}")

    try:
        registros = [_empaquetar_registro(item) for item in items]

        with open(ruta, "wb") as archivo:
            archivo.write(HEADER.pack(MAGIA, TEMAS[TEMA], len(registros)))
            for registro in registros:
                archivo.write(registro)

    except (OSError, struct.error) as error:
        raise ArchivoInvalidoError(
            f"No se pudo guardar el archivo binario: {error}"
        ) from error


def cargar_binario(ruta):
    """Carga el archivo binario y devuelve una lista de diccionarios."""
    try:
        with open(ruta, "rb") as archivo:
            cantidad = _validar_header(archivo)

            # Validación de binario corto: comprobamos el tamaño total del archivo
            archivo.seek(0, 2)
            tamanio_archivo = archivo.tell()
            tamanio_esperado = HEADER.size + cantidad * REGISTRO.size

            if tamanio_archivo < tamanio_esperado:
                raise ArchivoInvalidoError(
                    "El archivo binario es corto: su tamaño físico es menor al declarado en la cabecera."
                )

            # Volvemos al inicio de los registros después del header
            archivo.seek(HEADER.size)
            canciones = []

            for numero in range(cantidad):
                datos = archivo.read(REGISTRO.size)

                if len(datos) != REGISTRO.size:
                    raise ArchivoInvalidoError(
                        f"El registro {numero} está incompleto (binario corto o corrupto)."
                    )

                try:
                    (
                        id_cancion,
                        titulo,
                        artista,
                        album,
                        anio,
                        genero,
                        duracion_seg,
                    ) = REGISTRO.unpack(datos)

                    canciones.append({
                        "id": id_cancion,
                        "titulo": _decodificar_texto(titulo),
                        "artista": _decodificar_texto(artista),
                        "album": _decodificar_texto(album),
                        "anio": anio,
                        "genero": _decodificar_texto(genero),
                        "duracion_seg": duracion_seg,
                    })
                except (UnicodeDecodeError, struct.error) as error:
                    raise ArchivoInvalidoError(
                        f"El registro {numero} contiene datos corruptos o inválidos."
                    ) from error

            # No se permiten bytes sobrantes después del último registro.
            if archivo.read(1):
                raise ArchivoInvalidoError(
                    "El archivo contiene datos sobrantes al final."
                )

            return canciones

    except ArchivoInvalidoError:
        raise
    except OSError as error:
        raise ArchivoInvalidoError(
            f"No se pudo cargar el archivo binario: {error}"
        ) from error


def actualizar_registro(ruta, posicion, item):
    """Reemplaza un registro por su posición (base 0), sin reescribir el archivo."""
    nuevo_registro = _empaquetar_registro(item)

    if isinstance(posicion, bool) or not isinstance(posicion, int):
        raise ArchivoInvalidoError("La posición debe ser un número entero.")

    if posicion < 0:
        raise ArchivoInvalidoError("La posición no puede ser negativa.")

    try:
        with open(ruta, "r+b") as archivo:
            cantidad = _validar_header(archivo)

            if posicion >= cantidad:
                raise ArchivoInvalidoError(
                    f"La posición {posicion} está fuera del catálogo "
                    f"(hay {cantidad} registros)."
                )

            desplazamiento = HEADER.size + posicion * REGISTRO.size
            archivo.seek(desplazamiento)

            registro_actual = archivo.read(REGISTRO.size)
            if len(registro_actual) != REGISTRO.size:
                raise ArchivoInvalidoError(
                    f"El registro en la posición {posicion} está incompleto."
                )

            archivo.seek(desplazamiento)
            escritos = archivo.write(nuevo_registro)

            if escritos != REGISTRO.size:
                raise ArchivoInvalidoError(
                    "No se pudo escribir el registro completo."
                )

    except ArchivoInvalidoError:
        raise
    except OSError as error:
        raise ArchivoInvalidoError(
            f"No se pudo actualizar el archivo binario: {error}"
        ) from error