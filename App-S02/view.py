"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along withthis program.If not, see <http://www.gnu.org/licenses/>.
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
    print("0- Cargar información en el catálogo")
    print("1- Comprar bicicletas para las estaciones con más viajes de origen")
    print("2- Planear paseos turísticos por la ciudad")
    print("3- Reconocer los componentes fuertemente conectados del sistema")
    print("4- Planear una ruta rápida para el usuario")
    print("5- Reportar rutas en un rango de fechas para los usuarios anuales")
    print("6- Planear el mantenimiento preventivo de bicicletas")
    print("7- La estación más frecuentada por los visitantes.")


catalog = None
servicefile = "Bikeshare-ridership-2021-utf8-small.csv"

def optionZero(catalog):
    print("\nCargando información de transporte de Bikeshare ridership...")
    totaltrips, dfD, dfND, vertexND, edgesND = controller.loadTrips(catalog, servicefile)
    numedges = controller.totalConnections(catalog)
    numvertex = controller.totalStops(catalog)
    print('Numero de viajes: ' + str(totaltrips))
    print("DiGraph:")
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    x = "Las primeras y últimas 5 estaciones cargadas en DiGraph son: \n" + dfD
    print(x)
    print("----------------------")
    print("Graph:")
    print('Numero de vertices: ' + str(vertexND))
    print('Numero de arcos: ' + str(edgesND))
    y = "Las primeras y últimas 5 estaciones cargadas en Graph son: \n" + dfND
    print(y)


def optionOne(catalog):
    try:
        df = controller.popularStations(catalog)
        print(df)
    except Exception as exp:
        return None


def optionTwo(catalog, name, available, min, max):
    try:
        df = controller.planTrips(catalog, name, available, min, max)
        print(df)
    except Exception as exp:
        return None


def optionThree(catalog):
    try:
        size, df = controller.stronglyConnected(catalog)
        print("La cantidad de componentes fuertemente conectados es: ", size)
        print(df)
    except Exception as exp:
        return None


def optionFour(catalog, origen, destino):
    try:
        cost, df = controller.fastRoute(catalog, origen, destino)
        print("El tiempo total de recorrido es: ", cost)
        print(df)
    except Exception as exp:
        return None

def optionFive(catalog, min, max):
    try:
        df = controller.routesInDateRange(catalog, min, max)
        print(df)
    except Exception as exp:
        return None


def optionSix(catalog,bikeId):
    try:
        df = controller.bikerMaintenance(catalog, bikeId)
        print(df)
    except Exception as exp:
        return None


def optionSeven(catalog, station, startdate, starthour, enddate, endhour):
    try:
        df = controller.infoStation(catalog, station, startdate, starthour, enddate, endhour)
        print(df)
    except Exception as exp:
        return None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        catalog = controller.init()
        optionZero(catalog)

    elif int(inputs[0]) == 1:
        optionOne(catalog)

    elif int(inputs[0]) == 2:
        name = input("Estación de inicio:  ")
        available = int(input("Disponibilidad del usuario: "))
        min = int(input("Mínimo estaciones de parada: "))
        max = int(input("Máximo rutas de respuesta: "))
        optionTwo(catalog, name, available, min, max)

    elif int(inputs[0]) == 3:
        optionThree(catalog)

    elif int(inputs[0]) == 4:
        origen = input("Estación de origen: ")
        destino = input("Estación de destino: ")
        optionFour(catalog, origen, destino)

    elif int(inputs[0]) == 5:
        min = input("Fecha inicial: " )
        max = input("Fecha final: " )
        optionFive(catalog, min, max)
        
    elif int(inputs[0]) == 6:
        bikeId = input("Identificador de la bicicleta: ")
        optionSix(catalog,bikeId)

    elif int(inputs[0]) == 7:
        station = input("Estación: ")
        startdate = input("Fecha inicial: ")
        starthour = input("Hora inicial: ")
        enddate = input("Fecha final: ")
        endhour = input("Hora final")
        optionSeven(catalog, station, startdate, starthour, enddate, endhour)

    else:
        sys.exit(0)
sys.exit(0)
