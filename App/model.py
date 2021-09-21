﻿"""
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


from typing import Counter
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
    "artworks":None,
    "artists_names":{}
    }
    catalog["artists"] = lt.newList("ARRAY_LIST", key="BeginDate")
    catalog["artworks"] = lt.newList("ARRAY_LIST")
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

def loadArtistsNames(catalog):
    for artist in lt.iterator(catalog["artists"]):
        name, constituentId = artist["DisplayName"], artist["ConstituentID"]
        catalog["artists_names"][name] = constituentId
        catalog["artists_names"][constituentId] = name

# Funciones para creacion de datos

# Funciones de consulta
def getLastThree(catalog):
    sizeArtists = lt.size(catalog["artists"])
    sizeArtworks = lt.size(catalog["artworks"])
    last3Artists = lt.subList(catalog["artists"], sizeArtists-2, 3)
    last3Artworks = lt.subList(catalog["artworks"], sizeArtworks-2, 3)
    return lt.iterator(last3Artists), lt.iterator(last3Artworks)

def getArtistsCronOrder(ArtistLt, iyear, fyear):
    #Mirar si hacer busqueda binaria para encontrar donde empezar
    datos = {"NumTot":0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":None}
    maxi = 0
    for i, artists in enumerate(lt.iterator(ArtistLt),1):
        if iyear <= artists["BeginDate"] <= fyear:
            datos["NumTot"] += 1
            if datos["NumTot"] <= 3:
                lt.addLast(datos["Primeros3"],artists)
            if i > maxi:
                maxi = i
        if artists["BeginDate"] > fyear:
            break
    datos["Ultimos3"] = lt.subList(ArtistLt,maxi-2, 3)
    return datos

def get_names(constituentdIds, dictNames):
    ls = []
    if constituentdIds:
        for id in constituentdIds:
            try:
                ls.append(dictNames[id])
            except KeyError:
                ls.append("Name not listed")
        return ls
    else:
        return ["No name listed"]



def getArtworksCronOrder(catalog, idate, fdate):
    #Mirar si hacer busqueda binaria para encontrar donde empezar
    datos = {"NumTot":0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":lt.newList("ARRAY_LIST")}
    maxi = 0
    for i, artworks in enumerate(lt.iterator(catalog["artworks"]),1):
        if idate <= artworks["DateAcquired"] <= fdate:
            datos["NumTot"] += 1
            if datos["NumTot"] <= 3:
                names = get_names(artworks["ConstituentID"], catalog["artists_names"])
                with_names = {key : value for key, value in artworks.items() if key != "ConstituentID"}
                with_names["Artists"] = names
                lt.addLast(datos["Primeros3"],with_names)
            if i > maxi:
                maxi = i
        if artworks["DateAcquired"] > fdate:
            break      
    for artwork in lt.iterator(lt.subList(catalog["artworks"],maxi-2, 3)):
        names = get_names(artwork["ConstituentID"], catalog["artists_names"])
        with_names = {key : value for key, value in artwork.items() if key != "ConstituentID"}
        with_names["Artists"] = names
        lt.addLast(datos["Ultimos3"],with_names)
    return datos



def getArtworksByMedium(catalog, name):   #qué pasa si el nombre no tiene un constituend id porque no existe
    constID = None                        #eliminar ["elements"] si se puede
    medios = lt.newList("ARRAY_LIST")
    obras = lt.newList("ARRAY_LIST")
    num_obras = 0
    for artist in lt.iterator(catalog["artists"]):   # peor caso O(n)) n: num arstistas
        if artist["DisplayName"] == name:
            constID = artist["ConstituentID"] 
            break
    if constID is not None:       
        for obra in lt.iterator(catalog["artworks"]):     # O(m) m: num obras
            if constID in obra["ConstituentID"]:        # O(m)
                num_obras += 1
                if obra["Medium"] in medios["elements"]:      #   O(z) z: cantidad de obras del artista <= m 
                    dicc = {"Titulo": obra["Title"], "Fecha de la obra": obra["Date"], "Medio": obra["Medium"], "Dimensiones": obra["Dimensions"]} 
                    pos = lt.isPresent(medios, obra["Medium"]) -1
                    lt.addLast(obras["elements"][pos], dicc)
                else:
                    dicc = {"Titulo": obra["Title"], "Fecha de la obra": obra["Date"], "Medio": obra["Medium"], "Dimensiones": obra["Dimensions"]}
                    lt.addLast(medios, obra["Medium"])
                    lt.addLast(obras, lt.newList("ARRAY_LIST"))
                    lt.addLast(obras["elements"][lt.size(obras)-1], dicc) 
    MedRecurrente= None
    mayor = 0
    ObrasMedMasUsado = None
    for medio in lt.iterator(medios):  #  O(y) y: cantidad de medios <= m  
        pos = lt.isPresent(medios, medio) -1
        tamaño = lt.size(obras["elements"][pos])     
        if tamaño > mayor:     # O(y)
            MedRecurrente = medio
            mayor = tamaño 
            ObrasMedMasUsado = obras["elements"][pos]
    dict_respuestas = {"TotObras": num_obras,
            "TotMedios": lt.size(medios),
            "MedMasUsado": MedRecurrente,
            "constID": constID,
            "num_mayor": mayor,
            "ObrasMedMasUsado": ObrasMedMasUsado}
    return dict_respuestas



# Funciones utilizadas para comparar elementos dentro de una lista
def compareArtistsbyDate(element1, element2):
    return element1["BeginDate"] < element2["BeginDate"]

def compareArtworksbyAcquired(element1, element2):
    return element1["DateAcquired"] < element2["DateAcquired"]

# Funciones de ordenamiento
def sortArtists(catalog):
    sa.sort(catalog["artists"],compareArtistsbyDate)

def sortArtworks(catalog):
    sa.sort(catalog["artworks"], compareArtworksbyAcquired)
