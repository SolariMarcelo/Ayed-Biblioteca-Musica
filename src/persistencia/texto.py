"""def cargar_texto(ruta):
    #Carga secuencial de un .txt: un registro por línea, separado por coma.
    #Devuelve una lista de dicts (E1 puede quedar así).
    raise NotImplementedError


def guardar_texto(ruta, filas, encabezados):
    #Escribe el catálogo en .txt con la primera línea de encabezados.
    raise NotImplementedError
"""
from src.excepciones import ArchivoInvalidoError


ENCABEZADOS = [
    "id",
    "titulo",
    "artista",
    "album",
    "anio",
    "genero",
    "duracion_seg"
]


def guardar_texto(ruta, filas, encabezados=ENCABEZADOS):
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("|".join(encabezados) + "\n")

            for fila in filas:
                valores = [str(fila[campo]) for campo in encabezados]
                archivo.write("|".join(valores) + "\n")

    except (OSError, KeyError, TypeError) as error:
        raise ArchivoInvalidoError(
            f"No se pudo guardar el archivo de texto: {error}"
        ) from error


def cargar_texto(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        if not lineas:
            raise ArchivoInvalidoError("El archivo está vacío.")

        encabezados = lineas[0].strip().split("|")

        if encabezados != ENCABEZADOS:
            raise ArchivoInvalidoError(
                "Los encabezados del archivo no son válidos."
            )

        canciones = []

        for numero, linea in enumerate(lineas[1:], start=2):
            valores = linea.rstrip("\n").split("|")

            if len(valores) != len(ENCABEZADOS):
                raise ArchivoInvalidoError(
                    f"Registro inválido en la línea {numero}."
                )

            try:
                cancion = {
                    "id": int(valores[0]),
                    "titulo": valores[1],
                    "artista": valores[2],
                    "album": valores[3],
                    "anio": int(valores[4]),
                    "genero": valores[5],
                    "duracion_seg": int(valores[6])
                }
            except ValueError as error:
                raise ArchivoInvalidoError(
                    f"Datos numéricos inválidos en la línea {numero}."
                ) from error

            canciones.append(cancion)

        return canciones

    except OSError as error:
        raise ArchivoInvalidoError(
            f"No se pudo cargar el archivo de texto: {error}"
        ) from error


#PRUEBA DEL GUARDADO
from src.dominio.cancion import CATALOGO


ruta = "data/catalogo.txt"

# Guardar el catálogo
guardar_texto(ruta, CATALOGO)
print("Catálogo guardado correctamente.")

# Cargar el catálogo
catalogo_cargado = cargar_texto(ruta)
print("Catálogo cargado correctamente.")

print("Cantidad de canciones:", len(catalogo_cargado))
print("Primera canción:", catalogo_cargado[0])