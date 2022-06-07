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






from logging import info
from DISClib.ADT.indexminpq import contains
import config
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import bfs as bfs
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.ADT import stack
from DISClib.Utils import error as error
from datetime import datetime
assert config

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def newAnalyzer():
        analyzer = {
            'completeTrips': None,   # lista donde se almacenan todos los viajes que tienen información completa
            'connections': None,     # grafo, cada vertice es una estación, los arcos son viajes
            "stations": None,        # mapa con las estaciones; key: <id>-<nameStation>    value: dic con información de la estación 
            "search": None,          # estructura para dfs o bfs (para recorrer el grafo)
            "components": None,      # estructura para kosaraju (componentes fuertemente conectados)
            "minPaths": None,        # estructura para dijsktra (árbol de caminos mínimos)
        }

        analyzer["completeTrips"] = lt.newList("ARRAY_LIST") 

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=790,comparefunction=compareStations)    

        analyzer["stations"] = m.newMap(790,maptype="PROBING")          

        return analyzer


def compareStations(station, keyValueStation):
    stationName=keyValueStation["key"]
    if station == stationName:
        return 0
    elif station > stationName:
        return 1
    else:
        return -1






# ____________________________________________________
#  Cargar, limpiar y organizar información
# ____________________________________________________

def loadAndCleanData(analyzer,trip):
    #Condiciones
    hasOriginId=len(trip["Start Station Id"])!=0
    hasEndId=len(trip["End Station Id"])!=0
    if hasOriginId and hasEndId:
        hasDifferent_Origin_End=(float(trip["Start Station Id"])!=float(trip["End Station Id"])) 
    hasTripDuration=float(trip["Trip  Duration"])>0
    hasBikeId=len(trip["Bike Id"])>0
    #Filtro
    if hasOriginId and hasEndId and hasDifferent_Origin_End and hasTripDuration and hasBikeId:
        formatDestination(trip)                         # Ej.: 7516.0 -> 7516
        getNames(trip)                                  # Completar estaciones que no tienen nombre con "Unknown"
        lt.addLast(analyzer["completeTrips"],trip)      # El viaje se añade a la lista de viajes con info completa
        createStations(analyzer,trip)                   # Se crean las estaciones (vertices) y rutas (arcos) en el grafo, y se añade la información al mapa
    return analyzer

def formatDestination(trip):
    d=trip["End Station Id"]
    if len(d)>0:
        trip["End Station Id"]=d[0]+d[1]+d[2]+d[3]
    return trip

def getNames(trip):
    originName=trip["Start Station Name"]
    destName=trip["End Station Name"]
    if len(originName)==0:
            trip["Start Station Name"]="Unknown"              
    if len(destName)==0:                                                    
            trip["End Station Name"]="Unknown"
    return trip

def createStations(analyzer,trip):
    originId=trip["Start Station Id"]
    destId=trip["End Station Id"]
    originName=trip["Start Station Name"]
    destName=trip["End Station Name"]
    originVert=originId+"-"+originName
    destVert=destId+"-"+destName
    #Para el grafo:
    addStationToGraph(analyzer, originVert)
    addStationToGraph(analyzer, destVert)
    addConnection(analyzer, originVert, destVert,trip)
    #Para el mapa:
    addStationToMap(analyzer,originVert,originName,originId)
    addStationToMap(analyzer,destVert,destName,destId)
    addTrip(analyzer,originVert,destVert,trip)
    return analyzer

# Para el grafo:

def addStationToGraph(analyzer, vert):
    if not gr.containsVertex(analyzer["connections"], vert):
        gr.insertVertex(analyzer["connections"], vert)
    return analyzer

def addConnection(analyzer,vertA,vertB,trip):                
    time=int(trip["Trip  Duration"])
    edge=gr.getEdge(analyzer["connections"],vertA,vertB)
    if edge is None:
        gr.addEdge(analyzer["connections"],vertA,vertB,time)
        newEdge=gr.getEdge(analyzer["connections"],vertA,vertB)
        newEdge["trips"]=1
    else:
        edge["trips"]+=1
        edge["weight"]=(time+edge["weight"])/edge["trips"]
    return analyzer

# Para el mapa:

def addStationToMap(analyzer,vertice,name,id):
    map=analyzer["stations"]
    if not m.contains(map,vertice):
        entry={"vertice":vertice,"name":name,"id":id,"inTrips":None,"outTrips":None,
                "dateInTrips":None, "dateOutTrips":None}
        entry["inTrips"]=lt.newList("ARRAY_LIST")
        entry["outTrips"]=lt.newList("ARRAY_LIST")
        m.put(map,vertice,entry)
    return analyzer

def addTrip(analyzer,originVert,destVert,trip):
    map=analyzer["stations"]
    origin=me.getValue(m.get(map,originVert))
    dest=me.getValue(m.get(map,destVert))
    lt.addLast(origin["outTrips"],trip)
    lt.addLast(dest["inTrips"],trip)
    return analyzer


# _______________________________________________________
#  Funciones de consulta - Respecto a la cerga de datos
# _______________________________________________________


def totalTrips(analyzer):
    return lt.size(analyzer["completeTrips"])

def totalConnections(analyzer):
    return gr.numEdges(analyzer["connections"])

def totalStations(analyzer):
    return gr.numVertices(analyzer["connections"])

def getVertices(analyzer):
    return gr.vertices(analyzer["connections"]) 

def firstAndLast5(lista):
    if lista==None:
        return None
    elif lt.size(lista)<=10: 
        return lista
    else:
        nuevaLista=lt.newList("ARRAY_LIST")
        for i in range(5):                     
            elemento=lt.getElement(lista,i+1)
            lt.addLast(nuevaLista,elemento)
        for i in range(5):                  
            elemento=lt.getElement(lista,lt.size(lista)-(4-i))
            lt.addLast(nuevaLista,elemento)
        return nuevaLista

def getInfoVert(analyzer,vertices):
    inforVert=lt.newList("ARRAY_LIST")
    for i in lt.iterator(vertices):
        inE=lt.size(me.getValue(m.get(analyzer["stations"],i))["inTrips"])
        outE=lt.size(me.getValue(m.get(analyzer["stations"],i))["outTrips"])
        inEdges=gr.indegree(analyzer["connections"],i)
        outEdges=gr.outdegree(analyzer["connections"],i)
        lt.addLast(inforVert,{"station":i,"inEdges":str(inEdges),"outEdges":str(outEdges),"inTrips":str(inE),"outTrips":str(outE)})
    return inforVert

def getNameFromVert(vertName):
    name=""
    for i in range(5,len(vertName)):
        name+=vertName[i]
    return name




# ___________________________________________________________
#  REQUERIMIENTO 1: ESTACIONES CON MÁS VIAJES DE SALIDA
# ___________________________________________________________

def orderVerticesByEdgeOuts(analyzer):
    mapStations=analyzer["stations"]
    lstStations=m.keySet(mapStations)
    vertices=lt.newList("ARRAY_LIST")
    for station in lt.iterator(lstStations):
        stationInfo=addNumOutTrips(station,mapStations)
        lt.addLast(vertices,stationInfo)
    orderedVert=merge.sort(vertices,cmpVertByEdgeOuts)
    first5=getFirst5(orderedVert)
    for stationInfo in lt.iterator(first5):
        getUserTypes(stationInfo)
        mostFrequentDate(stationInfo)
        mostFrequentHour(stationInfo)
    return first5

def addNumOutTrips(station,mapStations):
    entry=m.get(mapStations,station)
    value=me.getValue(entry)
    stationInfo=value.copy()
    stationInfo["numOutTrips"]=(lt.size(stationInfo["outTrips"]))
    return stationInfo

def cmpVertByEdgeOuts(v1,v2):
    v1=v1["numOutTrips"]
    v2=v2["numOutTrips"]
    return v1>v2

def getFirst5(lst):
    if lst==None:
        return None
    elif lt.size(lst)<=5:
        return lst
    else:
        first5=lt.newList("ARRAY_LIST")
        for i in range(5):              # CAMBIAR A 5
            element=lt.getElement(lst,i+1)
            lt.addLast(first5,element)
        return first5

def getUserTypes(stationInfo):
    stationInfo["Annual Member"]=0
    stationInfo["Casual Member"]=0
    lstOutTrips=stationInfo["outTrips"]
    for trip in lt.iterator(lstOutTrips):
        typeMember=trip["User Type"]
        stationInfo[typeMember]+=1
    return stationInfo

def mostFrequentDate(stationInfo):
    mapTripsOut=m.newMap(800,maptype="CHAINING")
    for i in lt.iterator(stationInfo["outTrips"]):
        startTrip=str(datetime.strptime(i["Start Time"],"%m/%d/%Y %H:%M").date())
        if not m.contains(mapTripsOut,startTrip):
            entry={"numTrips":1}
            m.put(mapTripsOut,startTrip,entry)
        else: 
            value=me.getValue(m.get(mapTripsOut,startTrip))
            value["numTrips"]+=1
    stationInfo["mostFrequentDate"]=getMostFrequent(mapTripsOut)
    return stationInfo

def mostFrequentHour(stationInfo):
    mapHourOut=m.newMap(800,maptype="CHAINING")
    for i in lt.iterator(stationInfo["outTrips"]):
        startTrip=datetime.strptime(i["Start Time"],"%m/%d/%Y %H:%M").hour
        startInverval=str(startTrip)+":"+"00"+" - "+str(startTrip)+":"+"59"
        if not m.contains(mapHourOut,startInverval):
            entry={"numTrips":1}
            m.put(mapHourOut,startInverval,entry)
        else:
            value=me.getValue(m.get(mapHourOut,startInverval))
            value["numTrips"]+=1
    stationInfo["mostFrequentHour"]=getMostFrequent(mapHourOut)
    return stationInfo

def getMostFrequent(map):
    keys=m.keySet(map)
    feature=""
    cont=0
    for i in lt.iterator(keys):
        numTrips=me.getValue(m.get(map,i))["numTrips"]
        if numTrips>cont:
            cont=numTrips
            feature=i
    return feature+"\n==> "+str(cont)


# ___________________________________________________________
#  REQUERIMIENTO 2: PLANEAR PASEOS TURÍSTICOS
# ___________________________________________________________

def getVertFromNameStation(analyzer,name):
    mapStations=analyzer["stations"]
    stations=m.keySet(mapStations)
    for station in lt.iterator(stations):
        stationName=getNameFromVert(station)
        if stationName==name:
            return station
    return None

def searchPaths(analyzer, initialStation):
    analyzer["search"]=dfs.DepthFirstSearch(analyzer["connections"], initialStation)     
    return analyzer

def filterPathsByTimeAndNumStations(analyzer, maxTime, minStations):
    minStations=float(minStations)
    maxTime=float(maxTime)
    stations=gr.vertices(analyzer["connections"])
    lstPaths=lt.newList("ARRAY_LIST")
    for i in lt.iterator(stations):
        existPath=dfs.hasPathTo(analyzer["search"],i)
        if existPath:
            path=dfs.pathTo(analyzer["search"],i)               
            timePath=getTimePath(analyzer,path)
            numStations=stack.size(path)-1
            if timePath<=maxTime and numStations>=minStations:         # segundos
                lt.addLast(lstPaths,path)
    return lstPaths

def getTimePath(analyzer,path):
    pila=path.copy()
    grafo=analyzer["connections"]
    time=0
    startVert=None
    endVert=None
    count=True
    while not stack.isEmpty(pila):  
        if count:
            startVert=stack.pop(pila)
        else:
            endVert=stack.pop(pila)
            edge=gr.getEdge(grafo,startVert,endVert)
            weight=edge["weight"]
            time+=weight
            startVert=endVert
        count=False
    return time
  

def preparElementsForPrint(analyzer,paths,numAnswers):
    numAnswers=int(numAnswers)
    if lt.size(paths)==0:
        numAnswers=0
    elif lt.size(paths)<numAnswers:
        numAnswers=lt.size(paths)
    lstPaths=lt.newList("ARRAY_LIST")
    for i in range(1,numAnswers+1):
        path=lt.getElement(paths,i)
        p={"numStations":None,"time [min]":None,"tourInfo":""}
        p["numStations"]=stack.size(path)-1
        time=getTimePath(analyzer,path)
        p["time"]=str(round(time/60,2))+" min"+"\n"+str(round(time,2))+" s"
        while not stack.isEmpty(path):
            station=stack.pop(path)
            if len(p["tourInfo"])==0:
                p["tourInfo"]=station
            else:
                p["tourInfo"]+=" ===> "+station
        lt.addLast(lstPaths,p)
    return lstPaths

                      

# ___________________________________________________________
#  REQUERIMIENTO 3: COMPONENTES FUERTEMENTE CONECTADOS
# ___________________________________________________________

def searchComponents(analyzer):
    analyzer["components"]=scc.KosarajuSCC(analyzer["connections"])
    return analyzer

def getNumComponents(analyzer):
    return scc.connectedComponents(analyzer["components"])

def getComponents(analyzer):
    SCC=analyzer["components"]
    grafo=analyzer["connections"]
    components=m.newMap(numelements=200,maptype="PROBING")
    for station in lt.iterator(gr.vertices(grafo)):
        sccId=m.get(SCC["idscc"],station)["value"]   # id del SCC al que pertenece la estación 
        existComponent=m.contains(components,sccId)
        if existComponent:
            entry=m.get(components,sccId)
            value=me.getValue(entry)
            lt.addLast(value["stations"],station)
        else:
            entry={"sccId":sccId,"stations":None}
            entry["stations"]=lt.newList("ARRAY_LIST")
            lt.addLast(entry["stations"],station)
            m.put(components,sccId,entry)
    return components

def preparComponentsForPrint(analyzer,components):
    mapStations=analyzer["stations"]
    lstComponents=lt.newList("ARRAY_LIST")
    for i in lt.iterator(m.valueSet(components)):
        component={"componentId":i["sccId"],"numStations":None,"mostStartStation":"None","mostEndStation":"None"}
        component["numStations"]=lt.size(i["stations"])
        stationMostOut, stationMostIn=mostInOutTrips(i["stations"],mapStations)
        if len(stationMostOut)!=0:
            component["mostStartStation"]=stationMostOut
        if len(stationMostIn)!=0:
            component["mostEndStation"]=stationMostIn
        lt.addLast(lstComponents,component)
    return lstComponents

def mostInOutTrips(stations,mapStations):
    stationMostOut=""
    stationMostIn=""
    outTrips=0
    inTrips=0
    for j in lt.iterator(stations):
        numOutTrips, numInTrips=getNumTrips(mapStations,j)
        if numInTrips>inTrips:
            inTrips=numInTrips
            stationMostIn=j
        if numOutTrips>outTrips:
            outTrips=numOutTrips
            stationMostOut=j
    return stationMostOut,stationMostIn

def getNumTrips(mapStations,station):
    entry=m.get(mapStations,station)
    value=me.getValue(entry)
    stationInfo=value
    numOutTrips=lt.size(stationInfo["outTrips"])
    numInTrips=lt.size(stationInfo["inTrips"])
    return numOutTrips,numInTrips



# ___________________________________________________________
#  REQUERIMIENTO 4: RUTA RÁPIDA
# ___________________________________________________________

def minimumCostPaths(analyzer,startStation):
    startStation=getVertFromNameStation(analyzer,startStation)
    analyzer["minPaths"]=djk.Dijkstra(analyzer["connections"],startStation)
    return analyzer

def getMinimumPath(analyzer,endStation):
    endStation=getVertFromNameStation(analyzer,endStation)
    path=djk.pathTo(analyzer["minPaths"],endStation)
    return path

def getTimeAndInfoPath(analyzer,path):
    path=fixStack(path)                       
    lstInfoPath=lt.newList("ARRAY_LIST")
    infoPath={"time":None,"info":None}
    time=getTimePath(analyzer,path)   
    infoPath["time"]=str(round(time/60,2))+" min"+"\n"+str(round(time,2))+" s"
    infoPath["info"]=createTimePathInfo(analyzer,path)
    lt.addLast(lstInfoPath,infoPath)
    return lstInfoPath

def createTimePathInfo(analyzer,path):
    pila=path.copy()
    grafo=analyzer["connections"]
    timeInfoPath=""
    startVert=None
    endVert=None
    count=True
    while not stack.isEmpty(pila):  
        if count:
            startVert=stack.pop(pila)
        else:
            endVert=stack.pop(pila)
            edge=gr.getEdge(grafo,startVert,endVert)
            time=edge["weight"]
            timeInfoPath=addInfoStation(analyzer,timeInfoPath,startVert,endVert,time)
            startVert=endVert
        count=False
    return timeInfoPath


def addInfoStation(analyzer,timeInfoPath,startVert,endVert,time):
    time=str(round(time/60,1))
    if len(timeInfoPath)==0:
        timeInfoPath="["+startVert+"]"+" == "+time+" min"+" ==> "+"["+endVert+"]"
    else:
        timeInfoPath+=" == "+time+" min"+" ==> "+"["+endVert+"]"
    return timeInfoPath


def fixStack(pila):
    p2=stack.newStack()
    p3=stack.newStack()
    while not stack.isEmpty(pila):
        element=stack.pop(pila)
        stack.push(p2,element["vertexA"])
        if stack.isEmpty(pila):
            stack.push(p2,element["vertexB"])
    while not stack.isEmpty(p2):
        element=stack.pop(p2)
        stack.push(p3,element)
    return p3


# ___________________________________________________________
#  REQUERIMIENTO 5: RUTAS EN UN RANGO DE FECHAS
# ___________________________________________________________

def getTripsByDate(analyzer,startDate,endDate):
    trips=lt.newList("ARRAY_LIST")
    totalTime=0
    startDate=startDate+" 00:00"
    endDate=endDate+" 24:59"
    for i in lt.iterator(analyzer["completeTrips"]):
        if i["Start Time"]>=startDate and i["End Time"]<=endDate:
            lt.addLast(trips,i)
            totalTime+=int(i["Trip  Duration"])
    return trips,totalTime

def getFrequentStations(trips):
    mapTripsOut=m.newMap(800,maptype="CHAINING")
    mapTripsIn=m.newMap(800,maptype="CHAINING")
    for i in lt.iterator(trips):
        origin=i["Start Station Id"]+"-"+i["Start Station Name"]
        dest=i["End Station Id"]+"-"+i["End Station Name"]
        if not m.contains(mapTripsOut,origin):
            entry={"numTrips":1}
            m.put(mapTripsOut,origin,entry)
        else:
            numTrips=me.getValue(m.get(mapTripsOut,origin))
            numTrips["numTrips"]+=1
        if not m.contains(mapTripsIn,dest):
            entry={"numTrips":1}
            m.put(mapTripsIn,dest,entry)
        else:
            numTrips=me.getValue(m.get(mapTripsIn,dest))
            numTrips["numTrips"]+=1
    originStation=getMostFrequent(mapTripsOut)
    destStation=getMostFrequent(mapTripsIn)
    return originStation,destStation

def getFrequentHours(trips):
    mapHourOut=m.newMap(100,maptype="CHAINING")
    mapHourIn=m.newMap(100,maptype="CHAINING")
    for i in lt.iterator(trips):
        startTrip=datetime.strptime(i["Start Time"],"%m/%d/%Y %H:%M").hour
        endTrip=datetime.strptime(i["End Time"],"%m/%d/%Y %H:%M").hour
        startInverval=str(startTrip)+":"+"00"+" - "+str(startTrip)+":"+"59"
        endInverval=str(endTrip)+":"+"00"+" - "+str(endTrip)+":"+"59"
        if not m.contains(mapHourOut,startInverval):
            entry={"numTrips":1}
            m.put(mapHourOut,startInverval,entry)
        else:
            value=me.getValue(m.get(mapHourOut,startInverval))
            value["numTrips"]+=1
        if not m.contains(mapHourIn,endInverval):
            entry={"numTrips":1}
            m.put(mapHourIn,endInverval,entry)
        else:
            value=me.getValue(m.get(mapHourIn,endInverval))
            value["numTrips"]+=1
    mostStartHour=getMostFrequent(mapHourOut)
    mostEndHour=getMostFrequent(mapHourIn)
    return mostStartHour,mostEndHour

# ___________________________________________________________
#  REQUERIMIENTO 6: INFORMACIÓN DE BICICLETA
# ___________________________________________________________

def getTripsByBikeId(analyzer,bikeId):
    trips=lt.newList("ARRAY_LIST")
    numTrips=0
    totalTime=0
    for i in lt.iterator(analyzer["completeTrips"]):
        if float(i["Bike Id"])==float(bikeId):
            numTrips+=1
            totalTime+=int(i["Trip  Duration"])
            lt.addLast(trips,i)
    return trips,numTrips,totalTime


   


