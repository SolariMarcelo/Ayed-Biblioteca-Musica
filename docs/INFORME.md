# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: Biblioteca musical
- Por qué lo eligieron (5–8 líneas): Elegimos la biblioteca musical porque es algo que nos apasiona y siempre en nuestras reuiones charlamos sobre artistas y sus obras.

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.

Un item del catalogo es un registro de cada elemento. En nuestro catalogo un item serian los datos de una cancion. Mutable quiere decir que puede ser cambiado, en nuestro caso en nombre ocategoria si estan mal escrito por ejemplo. Inmutable son los que no pueden cambiar, por ejemplo el ID.

```text
(pueden pegar un diagrama ASCII o una lista de clases)
```

## 3. Recursión (E2)

- Función: es la funcion llamada "versiones_de()"
- Caso base: si no encuentra devuelve vacia 
       if not directas:
            return []
- Caso recursivo: aplica recursivo cuando encuentra el id
     for version in directas:
            resultado += self.versiones_de(
                version["cancion_id"]
            )
- Traza de un ejemplo real del dataset: el progrma es hecho con el ejemplo de id 1  y devuelve Versión ID: 62 - Tipo: live

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |


--- Catálogo original: 67 canciones ---
Búsqueda lineal: 0.00001261 segundos
Búsqueda binaria: 0.00000342 segundos
Ordenamiento selección: 0.00112136 segundos
Ordenamiento inserción: 0.00144788 segundos

--- Catálogo ampliado: 500 canciones ---
Búsqueda lineal: 0.00011024 segundos
Búsqueda binaria: 0.00000528 segundos
Ordenamiento selección: 0.04692904 segundos
Ordenamiento inserción: 0.06195496 segundos

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
