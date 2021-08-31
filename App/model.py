"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = {"artists":None,
    "artworks":None
    }
    catalog["artists"] = lt.newList("ARRAY_LIST")
    catalog["artworks"] = lt.newList()
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

# Funciones para creacion de datos

# Funciones de consulta
def getLastThree(catalog):
    sizeArtists = lt.size(catalog["artists"])
    sizeArtworks = lt.size(catalog["artworks"])
    last3Artists = lt.subList(catalog["artists"], sizeArtists-2, 3)
    last3Artworks = lt.subList(catalog["artworks"], sizeArtworks-2, 3)
    return lt.iterator(last3Artists), lt.iterator(last3Artworks)

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento