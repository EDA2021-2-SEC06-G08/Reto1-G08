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
from DISClib.Algorithms.Sorting import mergesort as ms
from time import process_time as ptime 
from datetime import date
from math import pi
import re
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def timer(func):
    def wraper(*args, **kwargs):
        start = ptime()
        result = func(*args,**kwargs)
        stop = ptime()
        print(f"La función tardo {(stop-start)*1000} ms")
        return result
    return wraper

# Construccion de modelos
def newCatalog():
    catalog = {
    "artists":{},
    "artworks":{}
    }
    catalog["artists"]["byDate"] = lt.newList("ARRAY_LIST")
    catalog["artists"]["byId"] = lt.newList("ARRAY_LIST")
    catalog["artworks"]["byAcquisitionDate"] = lt.newList("ARRAY_LIST")
    catalog["artworks"]["byDepartment"] = lt.newList("ARRAY_LIST")
    catalog["artworks"]["byDate"] = lt.newList("ARRAY_LIST")
    return catalog

# Funciones para agregar informacion al catalogo
def addArtist(catalog, artist):
    filtered = {"ConstituentID":int(artist["ConstituentID"]),
    "Gender":artist["Gender"], 
    "DisplayName":artist["DisplayName"], 
    "Nationality":parseNat(artist["Nationality"]), 
    "BeginDate":int(artist["BeginDate"]),
    "EndDate": int(artist["EndDate"])
    }
    lt.addLast(catalog["artists"]["byDate"], filtered)
    lt.addLast(catalog["artists"]["byId"], filtered)

def addArtwork(catalog, artwork):
    filtered = {"Title":artwork["Title"], 
        "ConstituentID":eval(artwork["ConstituentID"]),
        "Date":dateToInt(artwork["Date"]),
        "Medium":artwork["Medium"],
        "Dimensions":artwork["Dimensions"],
        "CreditLine":artwork["CreditLine"],
        "Department":artwork["Department"],
        "Classification":artwork["Classification"],
        "Weight (kg)":toFloat(artwork["Weight (kg)"]),
        "Width (cm)":toFloat(artwork["Width (cm)"]),
        "Length (cm)":toFloat(artwork["Length (cm)"]),
        "Height (cm)":toFloat(artwork["Height (cm)"]),
        "Depth (cm)":toFloat(artwork["Depth (cm)"]),
        "Circumference (cm)":toFloat(artwork["Circumference (cm)"]),
        "Diameter (cm)":toFloat(artwork["Diameter (cm)"]),
        "DateAcquired":toDate(artwork["DateAcquired"]),
        "Seat Height (cm)":toFloat(artwork["Seat Height (cm)"])
        }
    lt.addLast(catalog["artworks"]["byAcquisitionDate"], filtered)
    lt.addLast(catalog["artworks"]["byDepartment"], filtered)
    lt.addLast(catalog["artworks"]["byDate"], filtered)

def parseNat(nationality):
    if nationality == "" or nationality == "Nationality unknown":
        return ""
    else:
        return nationality

def toFloat(string):
    try:
        return float(string)
    except ValueError:
        return None

def toDate(string):
    try:
        return date.fromisoformat(string)
    except ValueError:
        return date(1,1,1)

def dateToInt(string):
    try:
        return int(re.search("\d{4}",string)[0])
    except TypeError:
        return 0



# Funciones para creacion de datos

# Funciones de consulta
def getLastThree(catalog):
    sizeArtists = lt.size(catalog["artists"]["byDate"])
    sizeArtworks = lt.size(catalog["artworks"]["byDate"])
    last3Artists = lt.subList(catalog["artists"]["byDate"], sizeArtists-2, 3)
    last3Artworks = lt.subList(catalog["artworks"]["byDate"], sizeArtworks-2, 3)
    return lt.iterator(last3Artists), lt.iterator(last3Artworks)
@timer
def getArtistsCronOrder(catalog, iyear, fyear):
    datos = {"NumTot":0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":None}
    artists = catalog["artists"]["byDate"]
    pos = ceilSearch(iyear, artists, "BeginDate")
    if pos[1]:
        for i in range(pos[0]-1, 1, -1):
            if lt.getElement(artists, i)["BeginDate"] < iyear:
                pos = i + 1 
                break
    else:
        pos = pos[0]
    maxi = 0
    for i in range(pos, lt.size(artists)+1):
        elem = lt.getElement(artists,i)
        if iyear <= elem["BeginDate"] <= fyear:
            datos["NumTot"] += 1
            if datos["NumTot"] <= 3:
                lt.addLast(datos["Primeros3"], elem)
            if i > maxi:
                maxi = i
        if elem["BeginDate"] > fyear:
            break
    datos["Ultimos3"] = lt.subList(artists,maxi-2, 3)
    return datos

#Obtenido de https://www.techiedelight.com/find-floor-ceil-number-sorted-array/
def ceilSearch(value, list, key):
    upper = lt.size(list)
    lower = 1
    ceil = -1
    while lower <= upper:
        mid = (upper-lower) // 2 + lower
        elem = lt.getElement(list, mid)[key]

        if elem == value:
            return mid,True
    
        elif value > elem:
            lower = mid + 1
        
        else:
            ceil = mid
            upper = mid - 1 
    return ceil, False

def binSearch(value, list, key):
    upper = lt.size(list)
    lower = 1

    while lower <= upper:
        mid = (upper-lower) // 2 + lower
        elem = lt.getElement(list, mid)[key]
        if elem == value:
            return mid
        
        elif value > elem:
            lower = mid + 1
        
        else:
            upper = mid - 1 
    
    return -1
@timer
def getArtworksCronOrder(catalog, idate,fdate):
    idate = toDate(idate)
    fdate = toDate(fdate)
    datos = catalog["artworks"]["byAcquisitionDate"]
    res = {"NumTot":0,
            "Purchase":0,
            "NumArtistas": 0,
            "Primeros3":lt.newList("ARRAY_LIST"),
            "Ultimos3":lt.newList("ARRAY_LIST")}
    pos = ceilSearch(idate, datos, "DateAcquired")
    maxi = 0
    artists = catalog["artists"]["byId"]
    if pos[1]:
        for i in range(pos[0]-1, 1, -1):
            elem = lt.getElement(datos,i)
            if elem < idate:
                pos = i + 1
                break
    else:
        pos = pos[0]
    for i in range(pos, lt.size(datos) + 1):
        elem = lt.getElement(datos, i)
        if idate <= elem["DateAcquired"] <= fdate:
            res["NumTot"] += 1
            if "purchase" in elem["CreditLine"].lower():
                res["Purchase"] += 1
            for id in elem["ConstituentID"]:
                res["NumArtistas"] += 1
            if res["NumTot"] <= 3:
                names = []
                for id in elem["ConstituentID"]:
                    index = binSearch(id, artists, "ConstituentID")
                    if index >= 1:
                        nombre = lt.getElement(artists, index)["DisplayName"]
                        names.append(nombre)
                    else:
                        names.append("Unknown")
                with_names = {key : value for key, value in elem.items() if key != "ConstituentID"}
                with_names["Artists"] = names
                lt.addLast(res["Primeros3"], with_names)
            if i > maxi:
                maxi = i
        if elem["DateAcquired"] > fdate:
            break
    for i in range(maxi-2, maxi+1):
        elem = lt.getElement(datos, i)
        names = []
        for id in elem["ConstituentID"]:
            index = binSearch(id, artists, "ConstituentID")
            if index >= 1:
                names.append(lt.getElement(artists, index)["DisplayName"])
            else:
                names.append("Unknown")
        with_names = {key : value for key, value in elem.items() if key != "ConstituentID"}
        with_names["Artists"] = names
        lt.addLast(res["Ultimos3"], with_names)
    return res


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

    
    """datos = {"TotObras": 0,
            "TotMedios": 0,
            "MedMasUsado": None,
            "constID": catalog["artists_names"][name],
            "num_mayor": 0}
    medios = {}     
    for i in lt.iterator(catalog["artworks"]):      
        if datos["constID"] in i["ConstituentID"] :
            if i["Medium"] in medios:
                dicc = {"Titulo": i["Title"], "Fecha de la obra": i["Date"], "Medio": i["Medium"], "Dimensiones": i["Dimensions"]} 
                lt.addLast(medios[i["Medium"]], dicc)
            if i["Medium"] not in medios:
                medios[i["Medium"]] = lt.newList("ARRAY_LIST")
                dicc = {"Titulo": i["Title"], "Fecha de la obra": i["Date"], "Medio": i["Medium"], "Dimensiones": i["Dimensions"]} 
                lt.addLast(medios[i["Medium"]], dicc)
                datos["TotMedios"] += 1    
            if lt.size(medios[i["Medium"]]) > datos["num_mayor"]: #que pasa si hay dos tecnicas iguales en cantidad de obras?
                datos["num_mayor"] = lt.size(medios[i["Medium"]])    
                datos["MedMasUsado"] = medios[i["Medium"]]["elements"][0]["Medio"] 
            datos["TotObras"] += 1
    datos["ObrasMedMasUsado"] = medios[datos["MedMasUsado"]]
    return datos """
@timer
def clasifyByNation(catalog):
    obras = catalog["artworks"]["byDate"]
    artists = catalog["artists"]["byId"]
    NumWorksbyNationalities = {}
    UniqueNationalities = {}

    for obra in lt.iterator(obras):
        adjust = {"Title": obra["Title"], "Date": obra["Date"], "Medium": obra["Medium"], "Dimensions" :obra["Dimensions"] }
        nations = {}
        for id in obra["ConstituentID"]:
            pos = binSearch(id, artists, "ConstituentID")
            if pos == -1:
                name = "Unknown"
                Nationality = "Unknown"
            else:
                name = lt.getElement(artists,pos)["DisplayName"]
                Nationality = lt.getElement(artists,pos)["Nationality"]
            if "Artists" not in adjust:
                adjust["Artists"] = [name]
            else:
                adjust["Artists"].append(name)
            
            if Nationality not in nations:
                nations[Nationality] = 1
            else:
                nations[Nationality] += 1
        
        for nation in nations:
            if nation not in UniqueNationalities:
                UniqueNationalities[nation]  = lt.newList("ARRAY_LIST")
                lt.addLast(UniqueNationalities[nation], adjust)
            else:

                lt.addLast(UniqueNationalities[nation], adjust)

        for nation, artist in nations.items():
            if nation not in NumWorksbyNationalities:
                NumWorksbyNationalities[nation] = artist
            else:
                NumWorksbyNationalities[nation] += artist

            
            
    size = lt.newList("ARRAY_LIST")
    for nac, v in NumWorksbyNationalities.items():
        lt.addLast(size, (nac,v))
    ms.sort(size, lambda elem1, elem2 : elem1[1] > elem2[1])

    countryMost = lt.getElement(size, 1)[0]
    country = UniqueNationalities[countryMost]

    return size, country, countryMost
@timer
def transportArtwDepartment(catalog, department):
    obras = catalog["artworks"]["byDepartment"]
    artists = catalog["artists"]["byId"]
    res = {
        "Tot":0,
        "Cost":0,
        "Weight":0,
        "5oldest": None,
        "5priciest":None
    }
    
    pos = binSearch(department, obras, "Department")

    if pos == -1:
        return False
    
    antiguas = lt.newList("ARRAY_LIST")
    precio = lt.newList("ARRAY_LIST")
    for i in range(pos-1, 1, -1):
        elem = lt.getElement(obras, i)["Department"]
        if elem != department:
            pos = i + 1
            break
    
    for i in range(pos, lt.size(obras) + 1):
        obra = lt.getElement(obras, i)
        if obra["Department"] != department:
            break
        res["Tot"] += 1
        if obra["Weight (kg)"]:
            res["Weight"] += obra["Weight (kg)"]
        cost = calculateCost(obra)
        res["Cost"] += cost
        artists2 = []
        for id in obra["ConstituentID"]:
            index = binSearch(id,artists, "ConstituentID")
            if index > 0:
                artists2.append(lt.getElement(artists, index)["DisplayName"])
            else:
                artists2.append("Unknown")
        adjust = {key:value for key,value in obra.items() if key != "ConstituentID"}
        adjust["Cost"] = cost
        adjust["Artists"] = artists2
        if obra["Date"] != 0:
            lt.addLast(antiguas, adjust)
        lt.addLast(precio, adjust)
    
    ms.sort(antiguas, lambda elem1, elem2: elem1["Date"] < elem2["Date"])
    ms.sort(precio, lambda elem1, elem2: elem1["Cost"] > elem2["Cost"])
    res["5oldest"] = lt.subList(antiguas,1, 5)
    res["5priciest"] = lt.subList(precio, 1, 5)
                    

    return res
    

def calculateCost(obra):
    costos = {"Kg":0, "M^2caj1":0,"M^2caj2":0, "M^3caj":0,"M^2cir":0, "M^3cir":0 }
    if obra["Weight (kg)"]:
        costos["Kg"] = 72*obra["Weight (kg)"]
    if obra["Length (cm)"] and obra["Height (cm)"] and obra["Width (cm)"]:
        costos["M^3caj"] = 72*((obra["Length (cm)"]/100) * (obra["Height (cm)"]/100) * (obra["Width (cm)"]/100))
    if obra["Length (cm)"] and obra["Height (cm)"]:
        costos["M^2caj1"] = 72*((obra["Length (cm)"]/100)*(obra["Height (cm)"]/100))
    if obra["Width (cm)"] and obra["Height (cm)"]:
        costos["M^2caj2"] = 72*((obra["Width (cm)"]/100) * (obra["Height (cm)"]/100))
    if obra["Width (cm)"] and obra["Length (cm)"]:
        costos["M^2caj3"] = 72*((obra["Width (cm)"]/100) * (obra["Length (cm)"]/100)) 
    if obra["Diameter (cm)"] and obra["Depth (cm)"]:
        costos["M^3cir"] = 72*(((obra["Diameter (cm)"]/100/2)**2) * pi * (obra["Depth (cm)"]/100))
    if obra["Diameter (cm)"]:
        costos["M^2cir"] = 72*(((obra["Diameter (cm)"]/100/2)**2) * pi)
    
    maxi = 0
    for valor in costos.values():
        if valor > maxi:
            maxi = valor
    if maxi == 0:
        return 48.0
    else:
        return maxi
    

# Funciones utilizadas para comparar elementos dentro de una lista
def cmpArtistsbyDate(element1, element2):
    return element1["BeginDate"] < element2["BeginDate"]

def cmpArtistsbyId(element1, element2):
    return element1["ConstituentID"] < element2["ConstituentID"] 

def cmpArtworksbyDateAcquired(element1, element2):
    return element1["DateAcquired"] < element2["DateAcquired"]

def cmpArtworksbyDepartment(element1, element2):
    return element1["Department"] < element2["Department"]

def cmpArtworksbyDate(element1, element2):
    return element1["Date"] < element2["Date"]

# Funciones de ordenamiento
def sortArtists(catalog):
    ms.sort(catalog["artists"]["byDate"],cmpArtistsbyDate)
    ms.sort(catalog["artists"]["byId"], cmpArtistsbyId)

def sortArtworks(catalog):
    ms.sort(catalog["artworks"]["byAcquisitionDate"], cmpArtworksbyDateAcquired)
    ms.sort(catalog["artworks"]["byDepartment"], cmpArtworksbyDepartment)
    ms.sort(catalog["artworks"]["byDate"], cmpArtworksbyDate)

#decorador para medir tiempo
