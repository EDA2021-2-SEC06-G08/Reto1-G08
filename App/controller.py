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
 """

import config as cf
import model
import csv
from datetime import date
import re

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos
def loadData(catalog):
    loadArtists(catalog)
    loadArtworks(catalog)
    loadArtistsNames(catalog)
    sortArtists(catalog)
    sortArtworks(catalog)

def loadArtists(catalog):
    filename = cf.data_dir + "MoMa/Artists-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artist in input_file:
        model.addArtist(catalog, {"ConstituentID":int(artist["ConstituentID"]),"Gender":artist["Gender"], "DisplayName":artist["DisplayName"], "Nationality":artist["Nationality"], "BeginDate":int(artist["BeginDate"])})

def loadArtworks(catalog):
    filename= cf.data_dir + "MoMA/Artworks-utf8-small.csv"
    input_file = csv.DictReader(open(filename, encoding="utf-8"))
    for artwork in input_file:
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
        "DateAcquired":toDate(artwork["DateAcquired"])}
        model.addArtwork(catalog, filtered)

def loadArtistsNames(catalog):
    model.loadArtistsNames(catalog)

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


# Funciones de ordenamiento
def sortArtists(catalog):
    model.sortArtists(catalog)

def sortArtworks(catalog):
    model.sortArtworks(catalog)

# Funciones de consulta sobre el catálogo
def getLastThree(catalog):
    return model.getLastThree(catalog)

def getArtistsCronOrder(catalog, iyear, fyear):
    """
    Retorna los datos de los artistas que estan en el rango de años pasados por parametro
    """
    return model.getArtistsCronOrder(catalog["artists"], iyear, fyear)

def getArtworksCronOrder(catalog, idate, fdate):

    return model.getArtworksCronOrder(catalog, toDate(idate), toDate(fdate))


