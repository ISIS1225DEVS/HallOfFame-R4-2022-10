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


from cgi import MiniFieldStorage
from cmath import inf
from gettext import Catalog
from hashlib import new
from tracemalloc import start
from DISClib.ADT.indexminpq import size
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import graph as gr
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.ADT import stack
from DISClib.Algorithms.Graphs import dijsktra as djk
from datetime import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initializeCatalog():
    """
    Se encarga de inicializar un catálogo vacío.

    #Describir cada componente del analyzer
    """
    analyzer = {
        'graph':None,
        'stops':None,
        'minCostPaths':None,
        'searchResult':None,
        'mapEdges':None,
        'vertexInfoMap':None,

        'stationNameMap': None,
        'bikeMap': None,

        #Req 1
        'RBTForNumTrips': None,
        'RBTForTopStations':None,
        'topFiveStationsKeys':None,

        #Req 3
        'conComponents':None, #Esta entrada luego será cubierta con el resultado del algoritmo de Kosaraju.
        #Req 5
        'datesRBT':None

    }

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=1500000,
                                              comparefunction=compStationIds)
    
    analyzer['mapEdges'] = mp.newMap(10000,
                                            maptype="CHAINING",
                                            loadfactor=2,
                                            comparefunction=cmpStationId)

    analyzer["vertexInfoMap"] = mp.newMap(10000,
                                            maptype="CHAINING",
                                            loadfactor=2,
                                            comparefunction=cmpVertexInfo)
    
    analyzer["stationNameMap"] = mp.newMap(10000,
                                            maptype="CHAINING",
                                            loadfactor=2,
                                            comparefunction=cmpVertexInfo)
    
    analyzer["bikeMap"] = mp.newMap(10000,
                                            maptype="CHAINING",
                                            loadfactor=2,
                                            comparefunction=cmpVertexInfo)

    #Para el requerimiento 1
    analyzer["RBTForNumTrips"] = om.newMap("RBT")

    analyzer["RBTForTopStations"] = om.newMap("RBT")

    analyzer["topFiveStationsKeys"] = lt.newList("ARRAY_LIST")

    #Para el requerimiento 5
    analyzer["datesRBT"] = om.newMap(omaptype="RBT")

    return analyzer
# Funciones para agregar informacion al catalogo

def addTrip(catalog, tripInfo):
    """
    Se encarga de cargar la información de cada viaje leído del archivo csv a
    las distintas estructuras de datos que lo requieran en una sola iteración por viaje leído.
    """

    #Construcción de filtros para la información leída.
    empty = 0
    startStation = tripInfo['Start Station Id']
    endStation = tripInfo['End Station Id']
    tripTime = tripInfo['Trip  Duration']
    BikeId = tripInfo['Bike Id']
    nameO = tripInfo['Start Station Name']
    nameD = tripInfo['End Station Name']
    userType = tripInfo["User Type"]


    #Date type fix for every data set
    date_time_str = tripInfo["Start Time"]
    date_time_obj = datetime.strptime(date_time_str, '%m/%d/%Y %H:%M')

    tripInfo["Start Time"] = date_time_obj

    if startStation == '':
        empty+=1
    else:
        startStation = startStation.replace('.0','')

    if endStation == '':
        empty+=1
    else:
        endStation = endStation.replace('.0','')

    same=0

    if startStation==endStation:
        same+=1


    elif tripTime != '0' and tripTime != '' and BikeId != '':
        if startStation !='' and endStation !='':
            #Aquí se deben llamar las funciones de carga de datos a las estructuras, pues son los viajes filtrados.
            addStation(catalog, startStation, nameO)
            addStation(catalog, endStation, nameD)
            updateEdge(catalog, startStation, nameO, endStation, nameD, tripTime)

            #Llamada a función que añade info de los vertex a una tabla de hash
            addVertexInfoToMap(catalog, tripInfo, startStation, nameO, endStation, nameD)
            addStationNameMap(catalog, startStation, nameO, endStation, nameD)
            addBikeTripInfo(catalog, tripInfo, startStation, nameO, endStation, nameD, tripTime)

            #Para el árbol de fechas del requerimiento 5
            if userType == "Annual Member":
                buildDatesRBT(catalog, tripInfo)


    elif empty == 0:
        empty += 1
    
    return catalog, same, empty


# Funciones para creacion de datos

def addStation(catalog, stationID, name):

    vertexId = stationID + '-' + name

    if not gr.containsVertex(catalog['graph'], vertexId):
        gr.insertVertex(catalog['graph'], vertexId)
    return catalog

    
def updateEdge(catalog, startStation, nameO, endStation, nameD, tripTime):

    edges = catalog['mapEdges']
    weight = int(tripTime)

    vertexA = startStation + '-' + nameO
    vertexB = endStation + '-' + nameD
    edgeId= vertexA+ '@' + vertexB

    presente = mp.get(edges, edgeId)

    if presente==None:
        info = newInfo(weight,1)
        mp.put(edges,edgeId,info)
    else:
        edgeR=me.getValue(presente)
        edgeR['num']+=1
        peso = edgeR['weight']
        edgeR['weight']=(weight+peso)/edgeR['num']
        mp.put(edges,edgeId,edgeR)


def newInfo(weight, num):

    entry = {'weight':None,
                'num':None}
    
    entry['weight']=weight
    entry['num']=num
    return entry


def addEdges(catalog):

    map=catalog['mapEdges']
    graph = catalog['graph']
    lstEdges=mp.keySet(map)

    for key in lt.iterator(lstEdges):
        keyvalue = mp.get(map,key)
        value = me.getValue(keyvalue)
        peso=value['weight']
        pos = key.find('@')
        size = len(key)
        startid=key[0:pos]
        endid=key[pos+1:size]
        gr.addEdge(graph, startid, endid,peso)

# ==============================
# Funciones utilizadas para comparar elementos
# ==============================

def compStationIds(id1,id2):
    """
    Compara dos estaciones
    """
    id2 = id2['key']

    if (id1 == id2):
        return 0
    elif (id1 > id2):
        return 1
    else:
        return -1

def cmpStationId(st1, st2):
    """
    Compara la información de 2 clubes
    """
    st2 = me.getKey(st2)
    if (st1 == st2):
        return 0
    elif (st1 < st2):
        return -1
    else:
        return 1

def cmpVertexInfo(vx1, vx2):
    """
    Compara la información de 2 vértices
    """
    vx2 = me.getKey(vx2)
    if (vx1 == vx2):
        return 0
    elif (vx1 < vx2):
        return -1
    else:
        return 1

def cmpVertex(vx1,vx2):

    if (vx1 == vx2):
        return 0
    elif (vx1 < vx2):
        return -1
    else:
        return 1


#Funciones de utilidad adicionales
def countVertex(graph):
    "Cuenta y devuelve la cantidad de vértices en un grafo dado"

    return gr.numVertices(graph)

def countEdges(graph):
    "Cuenta y devuelve la cantidad de arcos en un grafo dado"

    return gr.numEdges(graph)





#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Funciones de consulta
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Requerimiento 1
def topFiveStartStations(catalog):
    """
    Se encarga de realizar la búsqueda del top 5 de estaciones con más viajes de salida y devolver su información en un formato lista.
    """
    topFiveList = lt.newList("ARRAY_LIST")
    finalTopFiveList = lt.newList("ARRAY_LIST")

    topFiveIDs = catalog["topFiveStationsKeys"]
    vertexInfoMap = catalog["vertexInfoMap"]

    #Devolver la información de ese top 5 de IDs a partir de buscar las IDs en la tabla de hash
    for key in lt.iterator(topFiveIDs):
        vertexInfo = mp.get(vertexInfoMap, key)
        vertexInfoDict = me.getValue(vertexInfo)
        lt.addLast(topFiveList, vertexInfoDict)

    #Devolver una lista construida en la carga de datos, la cual contiene el ID, el día en el que más salieron viajes y la hora también del
    #top 5 estaciones de salida.
    catalogTopFive = catalog["topStationsDatesHours"]

    #------------------Fin de cálculos y procesamiento con las estructuras de datos---------------------------------------------------------------------------------------------------------------------

    #Construcción de la lista final que se devolverá
    counter = 1

    for vertex in lt.iterator(topFiveList):
        stationID = vertex["stationID"]
        stationName = vertex["stationName"]
        amountDepartureTrips = lt.size(vertex["connectsToList"])
        AnnualTypeTrips = vertex["Annual members"]
        CasualTypeTrips = vertex["Casual members"]
        totalOutTrips = AnnualTypeTrips + CasualTypeTrips

        secondDict = lt.getElement(catalogTopFive, counter)
        topDate = secondDict["Top Date"]
        topHour = secondDict["Top Hour"]

        topHour = str(topHour)+":00 a "+str(topHour+1)+":00"

        itemDict = {"ID de la estación": stationID,
                    "Nombre de la estación":stationName,
                    "Cantidad de rutas que tiene de salida":amountDepartureTrips,
                    "Cantidad total de viajes de salida realizados": totalOutTrips,
                    "Viajes hechos por usuarios Anuales": AnnualTypeTrips,
                    "Viajes hechos por usuarios Casuales": CasualTypeTrips,
                    "Fecha en la que salieron más viajes": topDate,
                    "Hora a la que salieron más viajes": topHour}
        
        lt.addLast(finalTopFiveList, itemDict)
        counter+=1

    return finalTopFiveList

"""
Información de ayuda temporal:
        vertexInfo = {"stationID": endStation,
                        "stationName": stationName,
                        "connectsToList": connectionsList,
                        "connectedToList": connectedToList,
                        "Annual members": 0,
                        "Casual members": 0,
                        "datesMap": datesMap 
"""

# Requerimiento 2
def searchPaths(catalog, startName, duration, minS, maxS):

    nameMap = catalog['stationNameMap']
    graph = catalog['graph']
    couple = mp.get(nameMap, startName)
    startId = me.getValue(couple)

    lstAdj = gr.adjacents(graph, startId)
    lstCaminos=lt.newList('ARRAY_LIST')
    contRutas =0

    for adj in lt.iterator(lstAdj):
        dura = gr.getEdge(graph,startId,adj)['weight']

        if dura<duration:
            lstRuta=lt.newList('ARRAY_LIST')
            lt.addLast(lstRuta,adj)
            lstNew = continuePath(graph,adj,dura,lstRuta,duration,minS,maxS)

            if contRutas<maxS and lstNew != 'nada':
                lt.addLast(lstCaminos,lstNew)
                contRutas+=1
            elif contRutas== maxS:
                lstPeso, lstParadas =tiempoyNumParadas(graph, lstCaminos)
                return lstCaminos,lstPeso, lstParadas
            
            if adj == lt.lastElement(lstAdj):
                lstPeso, lstParadas = tiempoyNumParadas(graph, lstCaminos)
                return lstCaminos, lstPeso, lstParadas

    """
    result_bfs = dfs.DepthFirstSearch(graph, startId)
    listaVertices = gr.vertices(graph)
    listaDestinos = lt.newList('ARRAY_LIST')

    for vertex in lt.iterator(listaVertices):
        if dfs.hasPathTo(result_bfs, vertex):
            lt.addLast(listaDestinos, vertex)

    contR = 0
    lstRta = lt.newList('ARRAY_LIST')

    for destino in lt.iterator(listaDestinos):
        path = dfs.pathTo(result_bfs, destino)
        numParadas = lt.size(path)-1
        if numParadas >= minS and contR < maxS:
            seAcabo = False
            peso = 0
            while seAcabo == False:
                if stack.size(path)>=2:
                    ini = stack.pop(path)
                    fin = stack.pop(path)
                    peso += gr.getEdge(graph, ini, fin)['weight']
                elif stack.size(path)==1:
                    finF= stack.pop(path)
                    peso += gr.getEdge(graph, fin, finF)['weight']
                elif stack.size(path)==0:
                    seAcabo = True
                    contR+=1
                    camino=dfs.pathTo(result_bfs, destino)
                    termino = False
                    lstFinal = lt.newList('ARRAY_LIST')
                    while termino == False:
                        if stack.size(camino)>0:
                            idStack = stack.pop(camino)
                            idNom = idStack
                            lt.addLast(lstFinal,idNom)
                        elif stack.size(camino) == 0:
                            pathInfo = {"path": lstFinal,
                                        "duration": peso,
                                        'numEstaciones': numParadas}
                            
                            lt.addLast(lstRta,pathInfo)
                            termino = True

                if peso>duration:
                    seAcabo = True

        elif contR == maxS:
            break

    return lstRta
    """
    
def continuePath(graph,adjV,peso,lstRuta,duration,minS,maxS):
    lstAdj = gr.adjacents(graph,adjV)

    for adj in lt.iterator(lstAdj):
        dura = gr.getEdge(graph,adjV,adj)['weight']
        peso+=dura
        if peso<duration:
            lt.addLast(lstRuta,adj)
            continuePath(graph,adj,peso,lstRuta,duration,minS,maxS)
        
        if peso<duration and lt.size(lstRuta)>=minS:
            return lstRuta
        
        if peso>duration and lt.size(lstRuta)<minS:
            return 'nada'

def tiempoyNumParadas(graph, lstCaminos):

    lstPeso = lt.newList('ARRAY_LIST')
    lstParadas = lt.newList('ARRAY_LIST')
    
    for camino in lt.iterator(lstCaminos):
        peso = 0
        for cont in range(1,lt.size(camino)+1,1):
            
            if cont<=lt.size(camino)-1:
                ini = lt.getElement(camino,cont)
                fin = lt.getElement(camino,cont+1)
                weight = gr.getEdge(graph, ini,fin)
                if weight != None:
                    weight = weight['weight']
                    peso+=weight
            
        lt.addLast(lstPeso,peso)
        lt.addLast(lstParadas,lt.size(camino))

    return lstPeso, lstParadas
    

#Requerimiento 3: Componentes fuertemente conectados
def getSCCfromGraph(catalog):
    """
    Calcula los componentes conectados del grafo.
    Se utiliza el algoritmo de Kosaraju.
    """
    #En la carga de datos, ya se llamó a la función de Kosaraju para identificar estos componentes fuertemente conectados,
    #Además, se clasificaron en una tabla de hash.
    componentsMap = catalog["componentsMap"]
    vertexInfoMap = catalog["vertexInfoMap"]

    sccNumber = catalog["numberOfSCC"]

    #Ahora, queda iterar sobre cada lista de ids de cada componente fuertemente conectado y devolver la información de las estaciones
    #donde más viajes inician y terminan, llamando a una función que busque ese id de estación en el mapa de información de cada estación
    #del catálogo.

    #Diccionario de respuesta
    infoDict = {"Total de componente fuertemente conectados":sccNumber,
                "Información por componente":lt.newList("ARRAY_LIST")}

    #Llaves del mapa
    componentNumbers = mp.keySet(componentsMap)

    #Devolución de las listas de ids de cada componente
    for comp in lt.iterator(componentNumbers):
        kv = mp.get(componentsMap, comp)
        k = comp
        idList = me.getValue(kv)
        idListSize = lt.size(idList)
        #Contadores de viajes para hallar las estaciones más visitadas
        maxDeparture = 0
        maxArrive = 0
        topDeparture = None
        topArrive = None
        topDepartureID = None
        topArriveID = None

        #Iteración sobre esa lista para hallar las estaciones donde más viajes inician y terminan
        for id in lt.iterator(idList):
            findVertex = mp.get(vertexInfoMap, id)
            vertexInfo = me.getValue(findVertex)
            departures = lt.size(vertexInfo["connectsToList"])
            arrivals = lt.size(vertexInfo["connectedToList"])

            if departures > maxDeparture:
                maxDeparture = departures
                topDepartureID = id
                topDeparture = vertexInfo["stationName"]

            if arrivals > maxArrive:
                maxArrive = arrivals
                topArriveID = id
                topArrive = vertexInfo["stationName"]

        compDict = {"Número de componente":k,
                    "Tamaño del componente":idListSize,
                    "Estación de la que más salen viajes":(topDepartureID, topDeparture),
                    "Estación a la que más llegan viajes":(topArriveID, topArrive),
                    "Número máximo de viajes de salida":departures,
                    "Número máximo de viajes que llegan":arrivals}

        lt.addLast(infoDict["Información por componente"], compDict)

    componentsList = infoDict["Información por componente"]
    componentsList = sortSCC(componentsList)

    #Diccionario de respuesta
    infoDict = {"Total de componente fuertemente conectados":sccNumber,
                "Información por componente":componentsList}


    return infoDict


"""
       vertexInfo = {"stationID": startStation,
                        "stationName": stationName,
                        "connectsToList": connectionsList,
                        "connectedToList": connectedToList,
                        "Annual members": 0, #Son quienes salen de la estación solamente.
                        "Casual members": 0,
                        "datesMap": datesMap

"""
#Ordenar los resultados de los componentes fuertemente conectados
def sortSCC(sccList):
    """
    Ordena los resultados de los SCC según tamaño e ID.
    """
    result = sa.sort(sccList, cmpSortSCC)

    return result


def cmpSortSCC(scc1, scc2):
    """
    Ordena según tamaño de componente.
    """
    size1 = scc1["Número máximo de viajes de salida"] + scc1["Número máximo de viajes que llegan"]
    size2 = scc2["Número máximo de viajes de salida"] + scc2["Número máximo de viajes que llegan"]
    id1 = scc1["Número de componente"]
    id2 = scc2["Número de componente"]

    if size1 == size2:
        return id1> id2

    else:
        return size1 > size2




# Requerimiento 4
def searchMinCostPath(catalog,nameO, nameD):

    nameMap = catalog['stationNameMap']
    graph = catalog['graph']
    couple1 = mp.get(nameMap, nameO)
    couple2 = mp.get(nameMap, nameD)
    startId = me.getValue(couple1)
    endId = me.getValue(couple2)

    result_djk = djk.Dijkstra(graph, startId)
    path = djk.pathTo(result_djk, endId)

    seAcabo = False
    pesoTot = 0
    lstProm = lt.newList('ARRAY_LIST')
    lstNom = lt.newList('ARRAY_LIST')
    idNom = startId
    lt.addLast(lstNom,idNom)
    while seAcabo == False:
                if stack.size(path)>0:
                    fin1 = stack.pop(path)
                    ver1 = fin1['vertexB']
                    peso = fin1['weight']
                    pesoTot += peso
                    lt.addLast(lstProm, peso)

                    idNom1 = ver1
                    lt.addLast(lstNom,idNom1)
                elif stack.size(path)==0:
                    seAcabo = True
    
    return lstNom, lstProm, pesoTot



#Requerimiento 5
def routesReport(catalog, iDate, fDate):
    """
    Función que se encarga de encontrar información sobre la dinámica de transporte
    de los usuarios ANUALES dentro del rango de fechas dado, para presentarse como reporte.
    """
    #Obtención de la información del catálogo
    datesRBT = catalog["datesRBT"]
    vertexInfoMap = catalog["vertexInfoMap"]

    iDate = datetime.strptime(iDate, '%Y-%m-%d')
    fDate = datetime.strptime(fDate, '%Y-%m-%d')

    #Creación de contadores
    tripsCounter = 0
    tripsDuraton = 0

    maxDepartureTrips = 0
    maxArrivalTrips = 0
    topDepartureStation = None
    topArrivalStation = None

    listOfVertex = om.values(datesRBT, iDate, fDate) #Array list

    #Creación de listas array para guardar el conteo de horas de llegada y salida.
    endHoursList = lt.newList("ARRAY_LIST")
    begHoursList = lt.newList("ARRAY_LIST")

    for i in range(0, 24):
        lt.addLast(endHoursList, {"Hora":i,"counter":0})
        lt.addLast(begHoursList, {"Hora":i,"counter":0})

    #Iteración sobre la lista de fechas y sus estaciones relacionadas
    for dateDict in lt.iterator(listOfVertex):
        #TripsNumber and TripsDuration
        tripsNumber = dateDict["tripsNumber"]
        tripDuration = dateDict["tripsDuration"]
        tripsCounter += tripsNumber
        tripsDuraton += tripDuration

        #Estaciones de donde más salen y a donde más llegan
        dictList = dateDict["dictList"]
        
        for infoDict in lt.iterator(dictList):
            stationID = infoDict["startStation"]
            #print(infoDict)
            stationName = infoDict["startStation"]

            #Búsqueda de la información de esa estación en el mapa de infoVertex.
            vertexInfo = om.get(vertexInfoMap, stationID)
            vertexInfo = me.getValue(vertexInfo) #Aquí ya se tiene el diccionario con la info del vértice

            departuresNumber = lt.size(vertexInfo["connectsToList"])
            arrivalsNumber = lt.size(vertexInfo["connectedToList"])

            #Comparación con máximos
            if departuresNumber > maxDepartureTrips:
                maxDepartureTrips = departuresNumber
                topDepartureStation = stationName

            if arrivalsNumber > maxArrivalTrips:
                maxArrivalTrips = arrivalsNumber
                topArrivalStation = stationName

        
        #Ahora, se debe hallar la hora en la que más salen y llegan viajes en ese rango de fechas
        endHoursMap = dateDict["endHoursMap"]
        begHoursMap = dateDict["begHoursMap"]
        keys = mp.keySet(endHoursMap)
        keys2 = mp.keySet(begHoursMap)

        for endHour in lt.iterator(keys):
            getCounter = mp.get(endHoursMap, endHour)
            getCounter = me.getValue(getCounter)
            getCounter = getCounter["counter"]
            #Contador de la lista
            iList = lt.getElement(endHoursList, endHour)
            iList["counter"] += getCounter

        for begHour in lt.iterator(keys2):
            getCounter2 = mp.get(begHoursMap, begHour)
            getCounter2 = me.getValue(getCounter2)
            getCounter2 = getCounter2["counter"]
            #Contador de la lista
            iList2 = lt.getElement(begHoursList, begHour)
            iList2["counter"] += getCounter2

    #print("\nMax num viajes iniciados:",maxDepartureTrips)
    #print("Max num viajes que llegan:",maxArrivalTrips)

    #Encontrar los rangos de horas mayor
    maxBegHourC = 0
    maxBegHour = None
    maxEndHourC = 0
    maxEndHour = None

    for hour in lt.iterator(endHoursList):
        localCounter = hour["counter"]
        hourInt = hour["Hora"]

        if localCounter > maxEndHourC:
            maxEndHourC = localCounter
            maxEndHour = hourInt

    for hour2 in lt.iterator(begHoursList):
        localCounter2 = hour2["counter"]
        hourInt2 = hour2["Hora"]

        if localCounter2 > maxBegHourC:
            maxBegHourC = localCounter2
            maxBegHour = hourInt2

    maxBegHour = str(maxBegHour)+":00 - "+str(maxBegHour+1)+":00"
    maxEndHour = str(maxEndHour)+":00 - "+str(maxEndHour+1)+":00"
    

    #Creación de un diccionario de respuesta
    routesInfo = {"Cantidad de viajes realizados":tripsCounter,
                    "Duración de todos los viajes en segundos":tripsDuraton,
                    "Estación de la que más salen viajes":topDepartureStation,
                    "Estación a la que más llegan viajes":topArrivalStation,
                    "Hora en la que más viajes salen":maxBegHour,
                    "Hora en la que más viajes llegan":maxEndHour}

    return routesInfo


"""
        data = {"tripsNumber":0,
                "tripsDuration":0,
                "dictList":dictList,
                "endHoursMap": hoursMap}
"""

"""
    infoDict = {"startStation":startStation,  #(ID, name)
                "endStation":endStation,
                "Hour":begHour}
"""

# Requerimiento 6
def getBikeInfo(catalog,nameBike):

    bikeMap = catalog['bikeMap']
    valueKey = mp.get(bikeMap, nameBike)
    info = me.getValue(valueKey)

    totTrip = info['TotalTrips']
    hours = info['TotalTime']
    numOrigen = info['InfoOrigen']['numA']
    numDestino = info['InfoDestino']['numD']
    cont = 1
    big = 0
    for cont in range(1,lt.size(numOrigen)+1,1):
        present = lt.getElement(numOrigen,cont)

        if present > big:
            big=present
    
    posO = lt.isPresent(info['InfoOrigen']['numA'],big)
    nameO = lt.getElement(info['InfoOrigen']['lstA'],posO)
    cont = 1
    big = 0
    for cont in range(1,lt.size(numDestino)+1,1):
        present = lt.getElement(numDestino,cont)

        if present > big:
            big=present
    
    posD = lt.isPresent(info['InfoDestino']['numD'],big)
    nameD = lt.getElement(info['InfoDestino']['lstD'],posD)

    return totTrip, hours, nameO, nameD




#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Funciones para resolver requerimientos\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#Carga de datos (mostrar 5 primeros y últimos vértices del grafo)

def loadedDataInformation(catalog):
    "Devuelve una lista con la información de los 5 primeros y últimos vértices registrados en el grafo construido"

    graph = catalog["graph"]
    vertexInfoMap = catalog["vertexInfoMap"]

    vertexList = gr.vertices(graph)
    
    firstFive = lt.newList("ARRAY_LIST")
    lastFive = lt.newList("ARRAY_LIST")
    vertexListSize = lt.size(vertexList)

    needed = 5

    for number in range(1, needed+1):
        lt.addLast(firstFive, lt.getElement(vertexList, number))
    
    for number in range(vertexListSize-4, vertexListSize+1):
        lt.addLast(lastFive, lt.getElement(vertexList, number))

    fivesList = lt.newList("ARRAY_LIST")

    for vertex in lt.iterator(firstFive):
        
        vertexInfoDict = mp.get(vertexInfoMap, vertex)
        #print(gr.degree(graph, vertex))
        vertexInfoDict = me.getValue(vertexInfoDict)

        ID = vertexInfoDict["stationID"]
        stationName = vertexInfoDict["stationName"]
        departTrips = lt.size(vertexInfoDict["connectsToList"])
        arriveTrips = lt.size(vertexInfoDict["connectedToList"])

        infoDict = {"ID de la estación": ID,
                    "Nombre de la estación": stationName,
                    "Viajes que salen": departTrips,
                    "Viajes que llegan": arriveTrips }
        
        lt.addLast(fivesList, infoDict)

    #For last five, now.
    for vertex in lt.iterator(lastFive):
        
        vertexInfoDict = mp.get(vertexInfoMap, vertex)
        vertexInfoDict = me.getValue(vertexInfoDict)

        ID = vertexInfoDict["stationID"]
        stationName = vertexInfoDict["stationName"]
        departTrips = lt.size(vertexInfoDict["connectsToList"])
        arriveTrips = lt.size(vertexInfoDict["connectedToList"])

        infoDict = {"ID de la estación": ID,
                    "Nombre de la estación": stationName,
                    "Número total de rutas vinculadas":departTrips + arriveTrips,
                    "Número de rutas que salen": departTrips,
                    "Número de rutas que llegan": arriveTrips }
        
        lt.addLast(fivesList, infoDict)

    #print(fivesList)

    return fivesList


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Carga de datos en las estructuras construidas.
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def addVertexInfoToMap(catalog, tripInfo, startStation, nameO, endStation, nameD):
    """
    Se encarga de añadir y actualizar info de los vértices en una tabla de hash con mecanismo separate chaining
    """
    vertexMap = catalog["vertexInfoMap"]
    rbt = catalog["RBTForNumTrips"]

    vertexA = startStation + '-' + nameO
    vertexB = endStation + '-' + nameD

    startStation = vertexA
    endStation = vertexB

    #For Start Station
    #Is the vertex already in the map?
    containsStart = mp.get(vertexMap, vertexA)

    if containsStart == None:
        #Construction of a dictionary with the info each vertex will save
        stationName = tripInfo["Start Station Name"]
        connectionsList = lt.newList("ARRAY_LIST") #Lista de los IDs de estaciones a las que está conectada esta estación
        lt.addLast(connectionsList, endStation)
        connectedToList = lt.newList("ARRAY_LIST") #Lista de los IDs de estaciones que se conectan a esta estación
        #User Type
        userType = tripInfo["User Type"]
        #Date when trip started
        startingDate = str(tripInfo["Start Time"]) #Formato “%d/%m/%y %H:%M”

        startingDay = startingDate[0:10]

        startingHour = startingDate[11:13]
        startingHour = int(startingHour)

        datesMap = mp.newMap(365,               #We create a map to save dates and their respective number of trips done there
                            maptype="PROBING",  #This one contains days of the year
                            loadfactor=0.5)     #Inside of it there is another map for each day with ranges of hours.

        hoursMap = mp.newMap(24,
                            maptype="PROBING",  #This map contains ranges of hours of a day and the number of trips that departed 
                            loadfactor=0.5)     #at that hour range
                                                #The ranges will contain integers, example: 17-18
        
        #Adding Hour ranges
        for i in range(0, 25):
            mp.put(hoursMap, i, {"counter":0})

        
        #Adding days
        containsDay = mp.get(datesMap, startingDay)

        if containsDay == None:
            counter = 1
            dayDict = {"counter":counter, "hoursMap": hoursMap}

            #Adding hour to range
            hour = mp.get(dayDict["hoursMap"], startingHour)
            hourCounter = me.getValue(hour)
            hourCounter["counter"] += 1


            mp.put(datesMap, startingDay, dayDict)
        
        else:
            valueDay = me.getValue(containsDay)
            valueDay += 1




        vertexInfo = {"stationID": startStation,
                        "stationName": stationName,
                        "connectsToList": connectionsList, #Son quienes salen de la estación solamente.
                        "connectedToList": connectedToList, 
                        "Annual members": 0, 
                        "Casual members": 0,
                        "datesMap": datesMap
        }

        if userType == "Annual Member":
            vertexInfo["Annual members"] +=1

        elif userType == "Casual Member":
            vertexInfo["Casual members"] +=1

        mp.put(vertexMap, startStation, vertexInfo)


        #Adición al RBT de número de viajes
        om.put(rbt, startStation, {"Number":lt.size(connectionsList)})



    else:
        infoDict = me.getValue(containsStart)
        connectsToList = infoDict["connectsToList"]
        
        #Check if the target station is already here
        isInList = lt.isPresent(connectsToList, endStation)

        if isInList == 0:
            lt.addLast(connectsToList, endStation)

        #Add user Type
        userType = tripInfo["User Type"]

        if userType == "Annual Member":
            infoDict["Annual members"] +=1

        elif userType == "Casual Member":
            infoDict["Casual members"] +=1

        #Date when trip started
        startingDate = str(tripInfo["Start Time"]) #Formato “%d/%m/%y %H:%M”

        startingDay = startingDate[0:10]
    
        startingHour = startingDate[11:13]
        startingHour = int(startingHour)

        #DatesMap contains Day?
        datesMap = infoDict["datesMap"]
        containsDay = mp.get(datesMap, startingDay)

        if containsDay == None:
            counter = 1

            hoursMap = mp.newMap(24,
                            maptype="PROBING",  #This map contains ranges of hours of a day and the number of trips that departed 
                            loadfactor=0.5)     #at that hour range
                                                #The ranges will contain integers, example: 17-18
        
            #Adding Hour ranges
            for i in range(0, 25):
                mp.put(hoursMap, i, {"counter":0})

            dayDict = {"counter":counter, "hoursMap": hoursMap}

            #Adding hour to range
            hour = mp.get(dayDict["hoursMap"], startingHour)
            hourCounter = me.getValue(hour)
            hourCounter["counter"] += 1

            mp.put(datesMap, startingDay, dayDict)
        
        else:
            valueDay = me.getValue(containsDay)
            valueDay["counter"] +=1

            hour = mp.get(valueDay["hoursMap"], startingHour)
            hourCounter = me.getValue(hour)
            hourCounter["counter"] += 1

        #print(infoDict) #Works fine, saves counter for hours

        #Adición al rbt de número de viajes
        #containsNumTrips = om.contains(rbt, startStation)

        node = om.get(rbt, startStation)
        number = me.getValue(node)
        number["Number"] = lt.size(infoDict["connectsToList"])


    #----------------------------------------------------PART 2 ----------------------------------------------------------------

    #Now for the end station
    containsEnd = mp.get(vertexMap, vertexB)

    if containsEnd == None:
        #Construction of a dictionary with the info each vertex will save
        stationName = tripInfo["End Station Name"]
        connectionsList = lt.newList("ARRAY_LIST")
        connectedToList = lt.newList("ARRAY_LIST")
        lt.addLast(connectedToList, startStation)

        vertexInfo = {"stationID": endStation,
                        "stationName": stationName,
                        "connectsToList": connectionsList,
                        "connectedToList": connectedToList,
                        "Annual members": 0,
                        "Casual members": 0,
                        "datesMap": datesMap   
        }

        mp.put(vertexMap, endStation, vertexInfo)

        #Adición al RBT de número de viajes
        om.put(rbt, endStation, {"Number":lt.size(connectionsList)})
    
    else:
        infoDict = me.getValue(containsEnd)
        connectedToList = infoDict["connectedToList"]

        #Check if the origin station is already here
        isInList = lt.isPresent(connectedToList, startStation)
        if isInList == 0:
            lt.addLast(connectedToList, startStation) 

        #Adición al RBT de número de viajes                    
        node = om.get(rbt, endStation)
        number = me.getValue(node)
        number["Number"] = lt.size(infoDict["connectsToList"])


def getTopFiveStationsList(catalog):
    """
    Devuelve la lista con los IDs de las 5 estaciones con más viajes de salida
    """
    #Construcción del nuevo RBT con el top de trips
    catalog = buildTopStationsRBT(catalog)

    #Determinar las 5 llaves que más viajes de inicio poseen
    fiveStationsList = catalog["topFiveStationsKeys"]
    topStationsRBT = catalog["RBTForTopStations"]
    vertexInfoMap = catalog["vertexInfoMap"]
    topFiveList = lt.newList("ARRAY_LIST")

    #print(topStationsRBT)

    top = 5
    
    for i in range(0,top):
        maxKey = om.maxKey(topStationsRBT)
        maxKV = om.get(topStationsRBT, maxKey)
        topKey = me.getValue(maxKV)

        lt.addLast(fiveStationsList, str(topKey))
        om.deleteMax(topStationsRBT)

    topFiveIDs = fiveStationsList

    for key in lt.iterator(topFiveIDs):
        vertexInfo = mp.get(vertexInfoMap, key)
        vertexInfoDict = me.getValue(vertexInfo)
        lt.addLast(topFiveList, vertexInfoDict)

    #Buscar el día en el que más salieron viajes y la hora también
    topStationsDaysHours = lt.newList("ARRAY_LIST")
    maxNumberDate = 0
    maxDate = None

    for dict in lt.iterator(topFiveList):
        datesMap = dict["datesMap"]
        #Hallar la fecha con más viajes de salida
        datesList = om.keySet(datesMap)

        for date in lt.iterator(datesList):
            kv = om.get(datesMap, date)
            k = date
            v = me.getValue(kv)
            v = v["counter"]
            #Comparación con el mayor
            if v > maxNumberDate:
                maxNumberDate = v
                maxDate = k

        #Devolver la hora con más viajes de salida
        maxNumberHour = 0
        maxHour = None

        maxDateValue = om.get(datesMap, maxDate)
        maxDateValue = me.getValue(maxDateValue)
        #print(maxDateValue)
        hoursMap = maxDateValue["hoursMap"]

        hoursList = om.keySet(hoursMap)
        for hour in lt.iterator(hoursList):
            hkhv = om.get(hoursMap, hour)
            hk = hour
            hv = me.getValue(hkhv)
            hv = hv["counter"]
            #Comparación con máx
            if hv > maxNumberHour:
                maxNumberHour = hv
                maxHour = hk
                

        id = dict["stationID"]
        item = {"ID": id, "Top Date": maxDate, "Top Hour": maxHour}
        lt.addLast(topStationsDaysHours, item)

    #Devolver la info del top 5 estaciones con su ID, top fecha y hora en cada una para viajes de salida.

    #Añadir esta lista resultado al catálogo
    catalog["topStationsDatesHours"] = topStationsDaysHours


def buildTopStationsRBT(catalog):
    """
    Construye el RBT para determinar el top de estaciones de donde salen viajes.
    """
    preRBT = catalog["RBTForNumTrips"]
    topStationsRBT = catalog["RBTForTopStations"]

    IDs = om.keySet(preRBT)
    #print(preRBT)

    for id in lt.iterator(IDs):
        kv = om.get(preRBT, id)
        k = id
        v = me.getValue(kv)
        v = v["Number"]

        #Add to new RBT (inverted)
        om.put(topStationsRBT, v, k)
    
    return catalog



#Precálculo de los componentes fuertemente conectados para responder al requerimiento 3 en menor tiempo
def findSCCfromGraph(catalog):
    """
    Se encarga de aplicar el algoritmo de Kosaraju al grafo, luego de identificar cada componente fuertemente conectada
    y encontrar información útil.
    """
    graph = catalog["graph"]

    catalog["conComponents"] = scc.KosarajuSCC(graph)
    kosarajuResult = catalog["conComponents"]
    #Different ssc
    sccNumber = scc.connectedComponents(kosarajuResult)

    print("\nPronto terminará la carga de datos\n")
    #Components clasification
    idscc = kosarajuResult["idscc"]
    idsccKeys = mp.keySet(idscc)

    #Creation of a map to save compNumber - ids
    compsMap = mp.newMap(sccNumber, 
                        maptype="PROBING",
                        loadfactor=0.5)

    for id in lt.iterator(idsccKeys):
        kv = mp.get(idscc, id)
        k = id
        v = me.getValue(kv)

        containsNumber = mp.get(compsMap, v)
        if containsNumber == None:

            idsList = lt.newList("ARRAY_LIST")
            lt.addLast(idsList, k)
            mp.put(compsMap, v, idsList)
        
        else:
            idsList = me.getValue(containsNumber)
            lt.addLast(idsList, k)

    catalog["componentsMap"] = compsMap
    catalog["numberOfSCC"] = sccNumber



#Construcción del RBT de fechas para el requerimiento 5
def buildDatesRBT(catalog, tripInfo):
    """
    Recibe solamente los viajes de los usuarios anuales para tomar su información y construir
    un RBT junto a su información de viaje, para luego responder a algunos requerimientos.
    """
    datesRBT = catalog["datesRBT"]
    begDate = tripInfo["Start Time"]
    endDate = tripInfo["End Time"]
    tripDuration = int(tripInfo["Trip  Duration"])
    startStation = tripInfo["Start Station Id"] + '-' + tripInfo["Start Station Name"]
    endStation = tripInfo["End Station Id"] + '-' + tripInfo["End Station Name"]


    #Filtro del formato de fecha
    begDate = str(begDate)
    begHour = int(begDate[11:13])
    begDate = begDate[0:10]

    begDate = datetime.strptime(begDate, '%Y-%m-%d')

    #Hora de llegada del viaje
    endHour = str(endDate)
    endHour = int(endHour[11:13])


    infoDict = {"startStation":startStation,
                "endStation":endStation,
                "Hours":(begHour, endHour)}

    #Does RBT contain the date already?
    containsDate = om.get(datesRBT, begDate)

    if containsDate == None:
        dictList = lt.newList("ARRAY_LIST")
        lt.addLast(dictList, infoDict)

        #Adición del mapa de horas de llegada
        #Formating for arriving hours
        hoursMap = mp.newMap(24,
                            maptype="PROBING",  #This map contains ranges of hours of a day and the number of trips that arrived
                            loadfactor=0.5)     #at that hour range
                                                #The ranges will contain integers, example: 17-18

        begHoursMap = mp.newMap(24,
                            maptype="PROBING",  #This map contains ranges of hours of a day and the number of trips that arrived
                            loadfactor=0.5)     #at that hour range
                                                #The ranges will contain integers, example: 17-18

        #Adding Hour ranges
        for i in range(0, 25):
            mp.put(hoursMap, i, {"counter":0})

        for i in range(0, 25):
            mp.put(begHoursMap, i, {"counter":0})

        #Adding hour to range
        hour = mp.get(hoursMap, endHour)
        hourCounter = me.getValue(hour)
        hourCounter["counter"] += 1

        hour2 = mp.get(begHoursMap, begHour)
        hourCounter2 = me.getValue(hour2)
        hourCounter2["counter"] += 1

        data = {"tripsNumber":0,
                "tripsDuration":0,
                "dictList":dictList,
                "endHoursMap": hoursMap,
                "begHoursMap": begHoursMap}

        data["tripsNumber"] += 1
        data["tripsDuration"] += tripDuration

        om.put(datesRBT, begDate, data)


    else:
        dictsList = me.getValue(containsDate)
        hoursMap = dictsList["endHoursMap"]
        begHoursMap = dictsList["begHoursMap"]

        dictsList["tripsNumber"] += 1
        dictsList["tripsDuration"] += tripDuration

        dictsList = dictsList["dictList"]
        lt.addLast(dictsList, infoDict)

        #Adding hour to range
        hour = mp.get(hoursMap, endHour)
        hourCounter = me.getValue(hour)
        hourCounter["counter"] += 1

        hour2 = mp.get(begHoursMap, begHour)
        hourCounter2 = me.getValue(hour2)
        hourCounter2["counter"] += 1


                        
def addStationNameMap(catalog, startStation, nameO, endStation, nameD):

    nameMap = catalog["stationNameMap"]

    startName = nameO 
    endName = nameD
    
    #For Start Station
    #Is the vertex already in the map?
    containsStart = mp.get(nameMap, startName)
    containsEnd = mp.get(nameMap, endName)

    if containsStart == None:
        #Construction of a dictionary with the info each vertex will save
        vertexA = startStation + '-' + nameO

        mp.put(nameMap, startName, vertexA)

    if containsEnd == None:
        
        vertexB = endStation + '-' + nameD
        mp.put(nameMap, endName, vertexB)



def addBikeTripInfo(catalog, tripInfo, startStation, nameO, endStation, nameD, tripTime):

    bikeMap = catalog['bikeMap']
    bikeId = tripInfo['Bike Id']
    bikeId = bikeId.replace('.0','')
    time = int(tripTime)
    vertexA = startStation + '-' + nameO
    vertexB = endStation + '-' + nameD

    containsBike = mp.get(bikeMap, bikeId)

    if containsBike == None:

        lstA = lt.newList('ARRAY_LIST', cmpfunction=cmpVertex)
        numA = lt.newList('ARRAY_LIST', cmpfunction=cmpVertex)
        lstD = lt.newList('ARRAY_LIST', cmpfunction=cmpVertex)
        numD = lt.newList('ARRAY_LIST', cmpfunction=cmpVertex)
        
        lt.addLast(lstA,vertexA)
        lt.addLast(numA,1)
        lt.addLast(lstD,vertexB)
        lt.addLast(numD,1)

        infoO = {'lstA': lstA,
                 'numA': numA}
        
        infoD = {'lstD': lstD,
                 'numD': numD}

        bikeInfo = {"TotalTrips": 1,
                    "TotalTime": time,
                    "InfoOrigen": infoO,
                    "InfoDestino": infoD}

        mp.put(bikeMap,bikeId,bikeInfo)
    else:
        info = me.getValue(containsBike)

        info['TotalTrips']+=1
        info['TotalTime']+=time
        
        estaA=lt.isPresent(info['InfoOrigen']['lstA'],vertexA)
        estaD=lt.isPresent(info['InfoDestino']['lstD'],vertexB)
        if estaA==0:
            lt.addLast(info['InfoOrigen']['lstA'],vertexA)
            lt.addLast(info['InfoOrigen']['numA'],1)
        elif estaA != 0:
            nuevo = lt.getElement(info['InfoOrigen']['numA'], estaA)+1
            lt.changeInfo(info['InfoOrigen']['numA'],estaA,nuevo)


        if estaD ==0:
            lt.addLast(info['InfoDestino']['lstD'],vertexB)
            lt.addLast(info['InfoDestino']['numD'],1)
        elif estaD != 0:
            nuevo = lt.getElement(info['InfoDestino']['numD'], estaD)+1
            lt.changeInfo(info['InfoDestino']['numD'],estaD,nuevo)

        mp.put(bikeMap,bikeId,info)