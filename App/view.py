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
import sys
assert cf
sys.setrecursionlimit(100000000)

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
    print("7- Proponer nueva exposición")
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

def printArtistsCronOrder(data, iyear, fyear):
    print(f"Artistas en orden cronologico desde {iyear} hasta {fyear}")
    print(f"Numero total de artistas en el rango de años: {data['NumTot']}")
    print("\n")
    print("Primeros 3 artistas rango:")
    for artista in lt.iterator(data["Primeros3"]):
        print(f"{artista['DisplayName']} is a {artista['Gender']} {artista['Nationality']} artist borned in the year {artista['BeginDate']}", end=" ")
        print(f"and died in {artista['EndDate']}" if artista["EndDate"] != 0 else "and hasn't died.")
    print("-"*100)
    print("Ultimos 3 artistas del rango:")
    for artista in lt.iterator(data["Ultimos3"]):
        print(f"{artista['DisplayName']} is a {artista['Gender']} {artista['Nationality']} artist borned in the year {artista['BeginDate']}", end=" ")
        print(f"and died in {artista['EndDate']}" if artista["EndDate"] != 0 else "and hasn't died.")
    print("\n")

def printArtworksCronOrder(data, idate, fdate):
    print(f"Obras adquiridas en orden cronologico desde la fecha {idate} hasta {fdate}")
    print(f"Numero total de obras en el rango de fechas: {data['NumTot']} por {data['NumArtistas']} artistas diferentes")
    print(f"De las cuales se adquirieron {data['Purchase']} por modo de compra (Purchase)")
    print("-"*100)
    print("Primeras 3 obras del rango:")
    print("")
    for obra in lt.iterator(data["Primeros3"]):
        nombres = ", ".join(name for name in obra['Artists'])
        print(f"{obra['Title']} por {nombres}, fecha: {obra['Date']}, Medio: {obra['Medium']}, Dimensiones: {obra['Dimensions']}")
        print("")
    print("-"*100)
    print("Ultimas 3 obras del rango")
    print("")
    for obra in lt.iterator(data["Ultimos3"]):
        nombres = ", ".join(name for name in obra['Artists'])
        print(f"{obra['Title']} por {nombres}, fecha: {obra['Date']}, Medio: {obra['Medium']}, Dimensiones: {obra['Dimensions']}")
        print("")


def printArtworksByMedium (data, name):
    print(f"{41*'='} Req. No.3 Inputs {41*'='}")
    print(f"Examine the work of the artist named: {name}")
    print(f"{41*'='} Req. No.3 Answer {41*'='}")
    print(f"{name} with MoMA ID {data['constID']} has {data['TotObras']} pieces in his/her name at the museum.")
    print(f"There are {data['TotMedios']} different mediums/techniques in his/her work.\n")
    print(f"His/her most used Medium/Technique is {data['MedMasUsado']} with {lt.size(data['ObrasMedMasUsado'])} pieces.")
    print(f"These pieces are:")
    print(100*"=")
    for artwork in lt.iterator(data["ObrasMedMasUsado"]): 
        print(artwork) 
    print(100*"=")
    print("\n")


def printClasificationByNation(data):
    print(f"{'='*16} Req No. 4 Inputs {'='*16}")
    print(f"Ranking countries by their number of artworks in the MoMa. . .")
    print("\n")
    print(f"{'='*16} Req No. 4 Answer {'='*16}")
    print("The TOP 10 Countries in the MoMA are:")
    print("\n")
    print("-"*24)
    print(f" Nationality | Artworks ")
    for i, vals in enumerate(lt.iterator(data[0])):
        if i > 9:
            break
        print("-"*24)
        print(f"{(vals[0].strip() if vals[0] != '' else 'Unknown').center(13,' ')}|{str(vals[1]).center(10, ' ')}")
    print("-"*24)
    print("\n")
    print(f"The TOP nacionality in the museum is: {data[2]} with {lt.size(data[1])} unique pieces.")
    print("-"*100)
    print("the first and last 3 objects in the american list are:")
    for j in range(1,4):
        i = lt.getElement(data[1],j)
        print(f" Title: {i['Title']}, Artists: {', '.join(i['Artists'])}, Date: {i['Date'] if i['Date'] != 0 else 'Unknown'}, Dimensions: {i['Dimensions'] if i['Dimensions'] != None and i['Dimensions'] != '' else 'Unknown' } ")
    for j in range(lt.size(data[1])-2, lt.size(data[1])+1):
        i = lt.getElement(data[1], j)
        print(f" Title: {i['Title']}, Artists: {', '.join(i['Artists'])}, Date: {i['Date'] if i['Date'] != 0 else 'Unknown'}, Dimensions: {i['Dimensions'] if i['Dimensions'] != None and i['Dimensions'] != '' else 'Unknown' } ")
    print("\n")

def printTransportArtwDepartment(data, department):
    print(f"The MoMA is going to transport {data['Tot']} desde {department}")
    print(f"Estimated cargo weight (kg): {data['Weight']}")
    print(f"Estimated cargo cost (USD): {data['Cost']}")
    print("")
    print("The TOP 5 most expensive items to transport are:")
    print("")
    for i in lt.iterator(data["5priciest"]):
        print(f'Title: {i["Title"]}, Artists: {", ".join(i["Artists"])}, Classification: {i["Classification"]}, Date: {i["Date"]}, Medium: {i["Medium"]}, Dimensions: {i["Dimensions"]}, Cost: {i["Cost"]}')
        print("")
    for i in lt.iterator(data["5oldest"]):
        print(f'Title: {i["Title"]}, Artists: {", ".join(i["Artists"])}, Classification: {i["Classification"]}, Date: {i["Date"]}, Medium: {i["Medium"]}, Dimensions: {i["Dimensions"]}, Cost: {i["Cost"]}')
        print("")

def printNewExposition(data, añoi, añof, area):
    print(f"{35*'='} Req. No.6 (BONUS) Inputs {35*'='}")
    print(f"Searching artworks between {añoi} to {añof}")
    print(f"With an available area of {area} m^2")
    print(f"{35*'='} Req. No.6 (BONUS) Answer {35*'='}")
    print(f"The MoMA is going to exhibit pieces from {añoi} to {añof}")
    print(f"There are {data['totObras']} pieces in the possible exhibit")
    print(f"Fillin {data['areaprox']} of the {area} m^2 available")
    print("\n")
    print("The first 5 artworks are:")
    for i in lt.iterator(data["5primeras"]):
        print(100*"-")
        print(i)
    print(100*"-")
    print("\n")
    print("The last 5 artworks are:")
    for j in lt.iterator(data["5ultimas"]):
        print(100*"-")
        print(j)
    print(100*"-")
    print("\n")


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
        print(f"Artistas cargados: {lt.size(catalog['artists']['byDate'])}")
        print(f"Obras cargadas: {lt.size(catalog['artworks']['byDate'])}")
        lastThree = controller.getLastThree(catalog)
        printLastThree(lastThree)

    elif int(inputs[0]) == 2:
        iyear = int(input("Ingrese el año inicial: "))
        fyear = int(input("Ingrese el año final: "))
        artis_co = controller.getArtistsCronOrder(catalog, iyear, fyear)
        printArtistsCronOrder(artis_co, iyear, fyear)

    elif int(inputs[0]) == 3:
        idate = input("Ingrese la fecha inicial (AAAA-MM-DD): ")
        fdate = input("Ingrese la fecha final (AAAA-MM-DD): ")
        adquis_co = controller.getArtworksCronOrder(catalog, idate, fdate)
        printArtworksCronOrder(adquis_co, idate, fdate)

    elif int(inputs[0]) == 4:
        name = input("Ingrese el nombre del artista: ")
        artworks_co = controller.getArtworksByMedium(catalog, name)
        if artworks_co:
            printArtworksByMedium(artworks_co, name)
        else:
            print("El artista especificado no esta en la base de datos")  
            print("\n")      

    elif int(inputs[0]) == 5:
        by_nation = controller.clasifyByNation(catalog)
        printClasificationByNation(by_nation)
    
    elif int(inputs[0]) == 6:
        department = input("Ingrese el departamento: ")
        transport = controller.transportArtwDepartment(catalog, department)
        if transport:
            printTransportArtwDepartment(transport, department)
        else:
            print("No ingreso un departamento del museo")
    
    elif int(inputs[0]) == 7:
        añoi = int(input("Ingrese el año inicial de las obras: "))
        añof = int(input("Ingrese el año final de las obras: "))
        area = float(input("Ingrese el área disponible en m^2: "))
        exposition = controller.NewExposition(catalog, añoi, añof, area)
        printNewExposition(exposition, añoi, añof, area)

    else:
        sys.exit(0)
sys.exit(0)
