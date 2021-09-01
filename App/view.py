"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar cronológicamente los artistas")
    print("3- Listar cronológicamente las adquisiciones")
    print("4- Clasificar las obras de un artista por técnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("6- Transportar obras de un departamento")
    print("0- Salir")

def initCatalog():
    """
    Incializa el catalogo del museo
    """
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

def printLastThree(lastThree):
    l3Art, l3Aworks = lastThree
    position = {3:"Antepenultimo", 2:"Penultimo", 1:"Ultimo"}
    positionArt = {3:"Antepenultima", 2:"Penultima", 1:"Ultima"}
    i = 3
    for artist, artwork in zip(l3Art, l3Aworks):
        print(f"{position[i]} artista:\n {artist}")
        print(f"{positionArt[i]} obra:\n {artwork}")
        print("-"*102)
        i -= 1
    
catalog = None
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print(f"Artistas cargados: {lt.size(catalog['artists'])}")
        print(f"Obras cargadas: {lt.size(catalog['artworks'])}")
        lastThree = controller.getLastThree(catalog)
        printLastThree(lastThree)

    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
