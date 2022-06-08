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
import tracemalloc
import time
import csv
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la función del modelo para iniciar un catálogo vacío.
    """
    return model.initializeCatalog()


def loadData(catalog, csvName):
    """
    Se encarga de leer la información de los archivos csv dependiendo del tamaño seleccionado
    para la lectura. Luego, ejecuta las funciones que organizan esos datos en las estructuras de datos
    del catálogo para luego realizar las consultas.
    """
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    file = cf.data_dir + csvName #csvName debe ser el nombre de ruta al archivo csv de small, large, etc.
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter=",")

    #Número de elementos (viajes) leídos:
    tripsNumber = 0

    #Lectura de datos incorrectos
    autoRoute = 0
    emptyInfo = 0

    #Lectura y carg de cada viaje
    for trip in input_file:
        tripsNumber += 1
        catalog, same, empty = model.addTrip(catalog, trip)
        autoRoute += same
        emptyInfo += empty

    print("Ya se leyeron y cargaron los viajes.")
    #Adición de vértices
    print("Se están añadiendo los ejes al grafo...")
    model.addEdges(catalog)

    #Construcción de la lista top 5 de estaciones de salida para el Requerimiento 1
    print("Se están encontrando el top 5 estaciones...")
    model.getTopFiveStationsList(catalog)

    #Precálculo de los componentes fuertemente conectados para resolver el requerimiento 3
    print("Calculando componentes fuertemente conectados...")
    model.findSCCfromGraph(catalog)

    #ESPACIO PARA PRINTS
    #print(catalog["datesRBT"])

    #Conteo de viajes, vértices y arcos
    tripsNumber = tripsNumber - autoRoute - emptyInfo

    #Info de 5 primeros y últimos vértices
    fivesList = loadedDataInformation(catalog)

    #Vértices del grafo
    vertexNum = model.countVertex(catalog["graph"])
    edgesNum = model.countEdges(catalog["graph"])

    #//////////////////////////////////////////////////////////////////////////////////

    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return tripsNumber, catalog, delta_time, delta_memory, autoRoute, emptyInfo, vertexNum, edgesNum, fivesList



# Funciones de consulta sobre el catálogo
def loadedDataInformation(catalog):
    "Devuelve una lista con la información de los 5 primeros y últimos vértices registrados en el grafo construido"

    return model.loadedDataInformation(catalog)



#Requerimiento 1
def topFiveStartStations(catalog):
    """
    Se encarga de realizar la búsqueda del top 5 de estaciones con más viajes de salida y devolver su información en un formato lista.
    """
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    topFiveList = model.topFiveStartStations(catalog)

    #/////////////////////////////////////////////////////////////////////////////////
    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return topFiveList, delta_time, delta_memory



#Requerimiento 2
def searchPaths(catalog, nameS, duration, minS, maxS):
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    lstCaminos,lstPeso, lstParadas = model.searchPaths(catalog,nameS, duration, minS, maxS)

    #//////////////////////////////////////////////////////////////////////////////////

    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return lstCaminos,lstPeso, lstParadas, delta_time, delta_memory


#Requerimiento 3
def getSCCfromGraph(catalog):
    """
    Calcula los componentes conectados del grafo.
    Se utiliza el algoritmo de Kosaraju.
    """
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    sccNumber = model.getSCCfromGraph(catalog)

    #/////////////////////////////////////////////////////////////////////////////////
    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return sccNumber, delta_time, delta_memory



#Requerimiento 4
def searchMinCostPath(catalog, nameO, nameD):
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    lstNom, lstProm, pesoTot = model.searchMinCostPath(catalog,nameO, nameD)

    #//////////////////////////////////////////////////////////////////////////////////

    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return lstNom, lstProm, pesoTot, delta_time, delta_memory


#Requerimiento 5
def routesReport(catalog, iDate, fDate):
    """
    Función que se encarga de encontrar información sobre la dinámica de transporte
    de los usuarios ANUALES dentro del rango de fechas dado, para presentarse como reporte.
    """
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    routesInfo = model.routesReport(catalog, iDate, fDate)


    #/////////////////////////////////////////////////////////////////////////////////
    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return routesInfo, delta_time, delta_memory



# Requerimiento 6
def getBikeInfo(catalog, nameBike):
    #Inicialización del proceso para medir memoria
    tracemalloc.start()

    #toma de tiempo y memoria al principio de la carga
    start_time = getTime()
    start_memory = getMemory()

    #///////////////////////////////Instrucciones centrales////////////////////////////

    totTrip, hours, nameO, nameD = model.getBikeInfo(catalog,nameBike)

    #//////////////////////////////////////////////////////////////////////////////////

    #Toma de tiempo y memoria al final de la carga
    stop_memory = getMemory()
    stop_time = getTime()

    #Finalizar la toma de datos de memoria
    tracemalloc.stop()

    #Diferencia de tiempo y memoria
    delta_memory = deltaMemory(stop_memory, start_memory) #Retorna en Kb
    delta_time = deltaTime(stop_time, start_time) #Retorna en ms

    return totTrip, hours, nameO, nameD, delta_time, delta_memory




#/////////////////////////Funciones para medir la memoria utilizada/////////////////////////////////

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

#////////////////////////Funciones de medición de tiempo/////////////////////////////////

# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed