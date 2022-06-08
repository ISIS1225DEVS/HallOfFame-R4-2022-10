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

import numbers
import config as cf
import sys
import controller
import threading
from DISClib.ADT import list as lt
assert cf
if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#///////////////////////////////Funciones para iniciar y cargar el catálogo////////////////////////////////////////////
def initializeCatalog():
    """
    LLama la función del catálogo para inicializar un catálogo vacío.
    """
    catalog = controller.init()

    return catalog

def loadData(catalog, num):
    """
    Envía la información sobre qué archivo csv leer.
    """
    if num == 1:
        csvName = 'Bikeshare-ridership-2021-utf8-small.csv'
    elif num == 2:
        csvName = 'Bikeshare-ridership-2021-utf8-5pct.csv'
    elif num == 3:
        csvName = 'Bikeshare-ridership-2021-utf8-10pct.csv'
    elif num == 4:
        csvName = 'Bikeshare-ridership-2021-utf8-20pct.csv'
    elif num == 5:
        csvName = 'Bikeshare-ridership-2021-utf8-30pct.csv'
    elif num == 6:
        csvName = 'Bikeshare-ridership-2021-utf8-50pct.csv'
    elif num == 7:
        csvName = 'Bikeshare-ridership-2021-utf8-80pct.csv'
    elif num == 8:
        csvName = 'Bikeshare-ridership-2021-utf8-largepct.csv'
 
    tripsNumber, catalog, time, memory, autoRoute, emptyInfo, vertexNum, edgesNum, fivesList = controller.loadData(catalog, csvName)


    return tripsNumber, catalog, time, memory, autoRoute, emptyInfo, vertexNum, edgesNum, fivesList

#Requerimiento 1
def topFiveStartStations(catalog):
    """
 .   Se encarga de realizar la búsqueda del top 5 de estaciones con más viajes de salida y devolver su información en un formato lista.
    """
    topFiveList, time, memory = controller.topFiveStartStations(catalog)

    return topFiveList, time, memory

# Requerimiento 2
def giveRoutes(lstCaminos,lstPeso, lstParadas):
    print("-----------------------------------------------------------------------------------\n")
    print("Puede tomar las siguientes rutas: ")
    print("-----------------------------------------------------------------------------------\n")
    cont = 0
    for cont in range(1, lt.size(lstCaminos)+1,1):
        lstEstaciones = lt.getElement(lstCaminos,cont)
        for estacion in lt.iterator(lstEstaciones):
            print(estacion)
        print("-----------------------------------------------------------------------------------\n")
        
        duracion = str(lt.getElement(lstPeso,cont)/60)
        numEstaciones = lt.getElement(lstParadas,cont)
        print('Esta ruta tiene una duracion de: ' + duracion + ' minutos')
        print('Estaciones visitadas: ' + str(numEstaciones))
        print("-----------------------------------------------------------------------------------\n")
        
#Requerimiento 3
def getSCCfromGraph(catalog):
    """
    Calcula los componentes conectados del grafo.
    Se utiliza el algoritmo de Kosaraju.
    """
    sccNumber, time, memory = controller.getSCCfromGraph(catalog)

    return sccNumber, time, memory

#Requerimiento 4
def giveMinCostPath(lstNom, lstProm, pesoTot, nameO, nameD):
    print("-----------------------------------------------------------------------------------\n")
    print("La ruta más rápida para llegar a " + nameD + ' desde ' + nameO + ' es: ')
    print("-----------------------------------------------------------------------------------\n")
    cont = 0
    for cont in range(0,lt.size(lstNom),1):
        if cont==lt.size(lstNom)-1:
            print(lstNom['elements'][cont]+ '\n')
        else:
            print(lstNom['elements'][cont] + ' ,Tiempo hasta siguiente estacion: ' + str(lstProm['elements'][cont]/60) + ' minutos')

    print('Esta ruta tiene una duracion de: ' + str(pesoTot/60) + ' minutos\n')


#Requerimiento 5
def routesReport(catalog, iDate, fDate):
    """
    Función que se encarga de encontrar información sobre la dinámica de transporte
    de los usuarios ANUALES dentro del rango de fechas dado, para presentarse como reporte.
    """
    routesInfo, time, memory = controller.routesReport(catalog, iDate, fDate)

    return routesInfo, time, memory


# Requerimiento 6
def giveBikeInfo(totTrip, hours, nameO, nameD, nameBike):
    print("-----------------------------------------------------------------------------------\n")
    print("La información de la bicicleta con Id " + nameBike + ' es:\n' )

    print('Número total de viajes realizados con esta bicicleta: ' + str(totTrip))
    print('Número total de horas utilizada: ' + str(hours/3600))
    print('Estación en la que más viajes se iniciaron con esta bicicleta: ' + nameO)
    print('Estación en la que más viajes terminaron con esta bicicleta: ' + nameD + '\n')


def printMenu():
    print("\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("Bienvenido al programa analizador del sistema de préstado de bicicletas de la")
    print("                              ciudad de Toronto.")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("A continuación puedes elegir una de estas opciones de consulta:\n") 
    print("1- Inicializar el catálogo.")
    print("2- Cargar la información del catálogo.")
    print("3- Análisis para comprar bicicletas para las estaciones con más viajes de origen.")
    print("4- Planear paseos turísticos por la ciudad.")
    print("5- Reconocer los componentes fuertemente conectados del sistema.")
    print("6- Planear una ruta rápida para el usuario.")
    print("7- Reportar rutas en un rango de fechas para los usuarios anuales.")
    print("8- Planear el mantenimiento preventivo de bicicletas.")
    print("9- Terminar el programa y salir.")
    print("-----------------------------------------------------------------------------------\n")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar:\n>')
    print("\n>>Información: Se seleccionó la opción",inputs[0],"del catálogo.\n")
    if int(inputs[0]) == 1:
        print("Inicializando el catálogo...")
        catalog = initializeCatalog()
        print("\n>>El catálogo fue inicializado")

    elif int(inputs[0]) == 2:
        print("\nSe desea cargar un archivo con información sobre las rutas.")
        print("Elije una de las siguientes opciones (número entero) para el tamaño del archivo a cargar:\n")
        print("1- small")
        print("2- 5%")
        print("3- 10%")
        print("4- 20%")
        print("5- 30%")
        print("6- 50%")
        print("7- 80%")
        print("8- large\n")
        numberSelected = int(input("Elección:\n>"))
        print("\nSe va a cargar el tamaño de la [opción",str(numberSelected)+"]")
        print("\nSe están leyendo y cargando los datos...")
        tripsNumber, catalog, time, memory, autoRoute, emptyInfo, vertexNum, edgesNum, fivesList = loadData(catalog, numberSelected)
        memory = f"{memory:.3f}"
        time = f"{time:.3f}"
        print("\n:::Resultados de la ejecución:::\n")
        print("Los datos se cargaron satisfactoriamente.")
        print(">>Se ha leído y cargado la información de",tripsNumber,"viajes en el sistema de bicicletas de Toronto.\n")
        print("El grafo que modela el sistema de préstamo de bicicletas de toronto tiene las siguientes propiedades:")
        print(">>Posee "+str(vertexNum)+" vértices.")
        print(">>Posee "+str(edgesNum)+" arcos.")
        print("Como resultado de la filtración se han encontrado:")
        print(">>"+str(autoRoute)+" nodos que hacen un recorrido hacia ellos mismos.")
        print(">>"+str(emptyInfo)+" datos de estaciones vacíos.")
        print("Los cuales no se han tenido en cuenta para el desarrollo de los requerimientos\n")
        print(">>Estos datos ocupan un espacio de",memory,"KB en la memoria RAM del computador.")
        print(">>Se cargaron los datos del archivo en un tiempo de",time,"milisegundos.\n")
        print("A continuación, se presentará la información de los cinco primeros y últimos vértices registrados en el grafo:\n")
        counter = 1

        for vertexInfo in lt.iterator(fivesList):
            print("Vértice número "+str(counter))
            print("------------------------------")

            for keys,values in vertexInfo.items():
                print(keys, ":", values)
                
            print("\n")
            counter += 1

    elif int(inputs[0]) == 3: #Requerimiento 1
        print("\nA continuación, se realizará una búsqueda para hallar el top 5 de estaciones con más viajes de salida.\n")
        selection = int(input(">>Responde 1 para iniciar la búsqueda o 0 para cancelar el proceso: \n>"))
        print("\n")

        if selection == 1:
            topFiveList, time, memory = topFiveStartStations(catalog)
            memory = f"{memory:.3f}"
            time = f"{time:.3f}"       
                
            print("Ya se halló el top 5 de estaciones de salida.")
            print("\nLa búsqueda tomó un tiempo de",time,"milisegundos.")
            print("Los datos guardados para la respuesta ocupan",memory,"kilobytes en la memoria RAM.")
            print("\nA continuación, se mostrará la información para el top 5 de estaciones de salida:\n")

            counter = 1
            for top in lt.iterator(topFiveList):
                print("Estación número",counter)

                for keys, values in top.items():
                    print(keys, ":", values)
                
                print("\n")
                counter += 1

        else:
            pass

    
    elif int(inputs[0]) == 4:
        print('Planear paseos turísticos por la ciudad.\n')
        nameS = input('Ingrese el nombre de la estación de inicio: ')
        duration = int(input('Ingrese el tiempo que dispone para el paseo (en minutos): '))*60/2
        minS = int(input('Digite el número mínimo de estaciones que desea visitar: '))
        maxS = int(input('Ingrese el número máximo de rutas que desea consultar: '))
        lstCaminos,lstPeso, lstParadas, time, memory = controller.searchPaths(catalog, nameS, duration, minS, maxS)
        giveRoutes(lstCaminos,lstPeso, lstParadas)
        memory = f"{memory:.3f}"
        time = f"{time:.3f}"
        print(">>Este requerimiento ocupó un espacio de",memory,"KB en la memoria RAM del computador.")
        print(">>Se cargó el requerimiento en un tiempo de",time,"milisegundos.\n")
    

    elif int(inputs[0]) == 5: #Requerimiento 3: Grupal
        print("\nSe quieren reconocer los componentes fuertemente conectados del grafo modelado y algunos datos adicionales.")
        selection = int(input("\nPara iniciar el cálculo de los componentes, presiona (1), para cancelar presiona (0): \n>"))

        if selection == 1:
            sccData, time, memory = controller.getSCCfromGraph(catalog)
            memory = f"{memory:.3f}"
            time = f"{time:.3f}"

            sccNumber = sccData["Total de componente fuertemente conectados"]
            sccInfo = sccData["Información por componente"]

            print("\nSe han reconocido",sccNumber,"componentes fuertemente conectados en el grafo modelo.")
            print("\nEl cálculo tomó",time,"milisegundos en completarse.")
            print("La respuesta ocupa",memory,"kilobytes de espacio en la memoria RAM.")

            print("\nA continuación, se presentará información de los tres primeros y últimos componentes fuertemente conectados encontrados:\nEstos han sido ordenados según el tamaño de los componentes:\n")

            firstLastThree = lt.newList("ARRAY_LIST")

            counter = 3
            lstSize = lt.size(sccInfo)

            for i in range(1,counter+1):
                lt.addLast(firstLastThree, lt.getElement(sccInfo, i))

            for j in range(0, counter):
                lt.addLast(firstLastThree, lt.getElement(sccInfo, lstSize-j))

        
            for scc in lt.iterator(firstLastThree):

                for keys, values in scc.items():
                    print(keys, ":", values)

                print("\n")


    elif int(inputs[0]) == 6:
        print('Planear una ruta rápida para el usuario.\n')
        nameO = input('Ingrese el nombre de la estación de origen: ')
        nameD = input('Ingrese el nombre de la estación de destino: ')
        lstNom, lstProm, pesoTot, time, memory= controller.searchMinCostPath(catalog, nameO, nameD)
        giveMinCostPath(lstNom, lstProm, pesoTot, nameO, nameD)
        memory = f"{memory:.3f}"
        time = f"{time:.3f}"
        print(">>Este requerimiento ocupó un espacio de",memory,"KB en la memoria RAM del computador.")
        print(">>Se cargó el requerimiento en un tiempo de",time,"milisegundos.\n")



    elif int(inputs[0]) == 7: #Requerimiento 5: Grupal
        print("\nA continuación, se presentará un reporte de rutas para el beneficio de los usuarios de tipo ANUAL.")
        print("\nEs necesario que se de el rango de fechas para la búsqueda, ingresalos en el formato AAAA-MM-DD\nEjemplo:\n2021-03-14\n2021-06-30")
        iDate = input("\nIngresa la fecha de inicio: ")
        fDate = input("Ingresa la fecha final para la búsqueda: ")

        print("\nSe está determinando la información de los viajes realizados en esta fecha por las distintas rutas...")

        routesInfo, time, memory = routesReport(catalog, iDate, fDate)
        memory = f"{memory:.3f}"
        time = f"{time:.3f}"

        print("\n//////////Se ha generado un reporte de los viajes entre esas fechas///////////\n")
        print("El tiempo que tomó generarlo fue de",time,"milisegundos.")
        print("La memoria RAM ocupada para generar el reporte es de",memory,"Kilobytes.")
        print("\nEste es el reporte generado:\n")

        for keys, values in routesInfo.items():
            print(keys, ":", values)

        print("\n")



    elif int(inputs[0]) == 8:
        print('Planear mantenimiento preventivo de bicicletas.\n')
        nameBike = input('Ingrese el identificador de la bicicleta: ')
        totTrip, hours, nameO, nameD, time, memory= controller.getBikeInfo(catalog, nameBike)
        giveBikeInfo(totTrip, hours, nameO, nameD, nameBike)
        memory = f"{memory:.3f}"
        time = f"{time:.3f}"
        print(">>Este requerimiento ocupó un espacio de",memory,"KB en la memoria RAM del computador.")
        print(">>Se cargó el requerimiento en un tiempo de",time,"milisegundos.\n")



    elif int(inputs[0]) == 9:
        print(">>Se ha terminado el programa.\n")
        sys.exit(0)


    else:
        print("\n----------------------------------------------------------")
        print(">>>ATENCIÓN: Esa opción no es válida, intenta con otra:")
        print("----------------------------------------------------------\n")

#
