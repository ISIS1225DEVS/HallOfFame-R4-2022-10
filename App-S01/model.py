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


from xml.dom.minidom import Element
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Sorting import shellsort  as sh
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import prim as pr

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def analizerStart():
    analizer={}
    analizer["vertexList"]=lt.newList("SINGLE_LINKED")
    analizer["edgesDict"]=mp.newMap(30000,
                            maptype='PROBING',
                             loadfactor=0.5)
    analizer["contadorEstaciones"]=mp.newMap(30000,
                            maptype='PROBING',
                             loadfactor=0.5)
    analizer['dirGraph']=gr.newGraph(directed=True,
                            size=800, comparefunction=None)
    analizer['graph']=gr.newGraph(directed=False,
                            size=1000, comparefunction=None)
    analizer['dictAuxiliar']=mp.newMap(30000,
                            maptype='PROBING',
                             loadfactor=0.5)
    analizer['scc']=mp.newMap(30000,
                            maptype='PROBING',
                             loadfactor=0.5)
    analizer["tripList"]=lt.newList("SINGLE_LINKED")
    return analizer

def vertexDict(analizer, stationId, stationName):
    if stationName=='':
        stationName='uknown'
    llave=(stationName, stationId)
    if lt.isPresent(analizer['vertexList'],llave)==0:
        lt.addLast(analizer['vertexList'], llave)
        mp.put(analizer['dictAuxiliar'], stationName, llave)

    
def edgesDict(analizer, startStationId, startStationName, endStationId, endStationName, tripDuration):

    if startStationId != endStationId and startStationName!= endStationName and tripDuration >=0:
        if startStationName=='':
            startStationName='uknown'
        if endStationName=='':
            endStationName='uknown'
        verticeI=(startStationName, startStationId)
        verticeF=(endStationName, endStationId)

        arco=(verticeF,verticeI)

        if mp.contains(analizer['edgesDict'],arco)==False:
            listaTiempos=[]
            listaTiempos.append(int(tripDuration))
            mp.put(analizer['edgesDict'], arco, listaTiempos)

        else:
            llaveValor=mp.get(analizer['edgesDict'],arco)
            listaTiempos=list(me.getValue(llaveValor))
            listaTiempos.append(int(tripDuration))
            mp.put(analizer['edgesDict'], arco, listaTiempos)

    

def createGraph(analizer):
    for vertice in lt.iterator(analizer['vertexList']):
        gr.insertVertex(analizer['dirGraph'], vertice)

    listaVertices=mp.keySet(analizer['edgesDict'])

    for tuplaVertice in lt.iterator(listaVertices):
        llaveValor=mp.get(analizer['edgesDict'], tuplaVertice)
        listaTiempos=list(me.getValue(llaveValor))
        tamanioLista=len(listaTiempos)
        sumaLista=sum(listaTiempos)
        promedio=sumaLista/tamanioLista
        verticeA=tuplaVertice[0]
        verticeB=tuplaVertice[1]
        gr.addEdge(analizer['dirGraph'],verticeA, verticeB, promedio )

    lista=analizer['vertexList']
    i=0
    listaFinal=lt.newList()
    listaFinall=lt.newList()
    h=lt.size(lista)
    j=0
    i=0
    for vertice in lt.iterator(lista):
        outdegree=gr.outdegree(analizer['graph'], vertice)
        indegree=gr.indegree(analizer['graph'], vertice)
        nombre=vertice[0]
        Id=vertice[1]
        tupla=('NOMBRE: '+str(nombre),'ID VERTICE: '+str(Id), 'OUTDEGREE VERTICE '+str(outdegree), 'INDEGREE VERTice'+str(indegree))
        lt.addLast(listaFinal, tupla)
        i+=1
        if i==5:
            break

    while j<5:
        vertice=lt.getElement(lista, h)
        outdegree=gr.outdegree(analizer['graph'], vertice)
        indegree=gr.indegree(analizer['graph'], vertice)
        nombre=vertice[0]
        Id=vertice[1]
        tupla=('NOMBRE: '+str(nombre),'ID VERTICE: '+str(Id), 'OUTDEGREE VERTICE: '+str(outdegree), 'INDEGREE VERTICE: '+str(indegree))
        lt.addLast(listaFinall, tupla)
        j+=1
        h-=1
        
    return listaFinal, listaFinall

    


def createGraphNoDir(analizer):
    for vertice in lt.iterator(analizer['vertexList']):
        gr.insertVertex(analizer['graph'], vertice)
    listaVertices=mp.keySet(analizer['edgesDict'])
    listaVerticesNodirijidos=lt.newList()

    for tuplaVertice in lt.iterator(listaVertices):
        verticeA, verticeB =tuplaVertice
        if lt.isPresent(listaVertices, (verticeB,verticeA))!=0:
           lt.addLast(listaVerticesNodirijidos,tuplaVertice)
           pos=lt.isPresent(listaVertices,(verticeA,verticeB))
           lt.deleteElement(listaVertices, pos)

    for tuplaVertice in lt.iterator(listaVerticesNodirijidos):
        llaveValor=mp.get(analizer['edgesDict'], tuplaVertice)
        listaTiempos=list(me.getValue(llaveValor))
        tamanioLista=len(listaTiempos)
        sumaLista=sum(listaTiempos)
        promedio=sumaLista/tamanioLista
        verticeA=tuplaVertice[0]
        verticeB=tuplaVertice[1]
        gr.addEdge(analizer['graph'],verticeA, verticeB, promedio )

   

#Req 1
def cmpOutdegree(elemento1, elemento2):
    return(elemento1[1]>elemento2[1])
    
def contadorEstaciones(analizer, startStation, stationId):
    if mp.contains(analizer['contadorEstaciones'], (startStation,stationId))==False:
        contador=1
        mp.put(analizer['contadorEstaciones'], (startStation,stationId), contador)
    else: 
        llaveValor=mp.get(analizer['contadorEstaciones'], (startStation,stationId))
        contador=me.getValue(llaveValor)
        contador+=1
        mp.put(analizer['contadorEstaciones'],(startStation, stationId) ,contador)
        
def respuestaReq1(analizer):
    i=1
    lista=mp.keySet(analizer['contadorEstaciones'])
    listaRespuesta=lt.newList()
    listaFinal=lt.newList()
    lista5Primeros=lt.newList()
    for estacion in lt.iterator(lista):
        llaveValor=mp.get(analizer['contadorEstaciones'], estacion)
        recorridos=me.getValue(llaveValor)
        lt.addLast(listaFinal,(estacion, recorridos) )
    listaFinal=sh.sort(listaFinal, cmpOutdegree)
    while i<=5:
        element=lt.getElement(listaFinal, i)
        lt.addLast(lista5Primeros, element)
        i+=1
    for valor in lt.iterator(lista5Primeros):
        estacion=valor[0]
        outdegree=gr.outdegree(analizer['dirGraph'], estacion)
        subscriberOutTrips=gr.indegree(analizer['dirGraph'], estacion)
        outTrips=valor[1]
        nombre=estacion[0]
        id=estacion[1]
        lt.addLast(listaRespuesta,'Nombre: '+str(nombre))
        lt.addLast(listaRespuesta,'id: '+str(id))
        lt.addLast(listaRespuesta,'OutTrips: '+str(outTrips))
        lt.addLast(listaRespuesta,'SubscribersOutTrips '+str(subscriberOutTrips))
        lt.addLast(listaRespuesta,'outDegree: '+str(outdegree))
    return(listaRespuesta)


#Req 2
def shortestPath(analizer, vertex, numEstaciones, duration, numRutas):
    search=dij.Dijkstra(analizer['dirGraph'],vertex )
    pathToList=lt.newList()
    numEstacionesList=lt.newList()
    lista=lt.newList()
    listaFinal=lt.newList()

    for vertex in lt.iterator(analizer['vertexList']):
        if dij.hasPathTo(search, vertex) ==True:
            lt.addLast(pathToList, vertex)
    for vertex in lt.iterator(pathToList):
        if lt.size(dij.pathTo(search, vertex))>numEstaciones:
            lt.addLast(numEstacionesList, vertex)
    for vertex in lt.iterator(numEstacionesList):
        if dij.distTo(search, vertex)<duration:
            lt.addLast(lista, vertex)
    size=lt.size(lista)
    i=1
    for valor in lt.iterator(lista):
        tupla=('total Stops: '+str(lt.size(dij.pathTo(search, valor))),"routeTime: "+str(dij.distTo(search, valor)), dij.pathTo(search, vertex),size )
        lt.addLast(listaFinal, tupla)
        i+=1
        if i>=numRutas:
            break
    return listaFinal

#Req 3
def stronglyConcetedC(analizer):
    diGraph=analizer['dirGraph']
    search=scc.KosarajuSCC(diGraph)
    count=scc.connectedComponents(search)
    vertex=lt.getElement(analizer['vertexList'],1)
    sccCount=scc.sccCount(diGraph, search, vertex)
    listaKeySet=mp.keySet(sccCount['idscc'])
    
    for estacion in lt.iterator(listaKeySet):
        llaveValor=mp.get(sccCount['idscc'], estacion)
        scca=me.getValue(llaveValor)
        if mp.contains(analizer['scc'],scca )==False:
            lista=lt.newList('ARRAY_LIST')
            lt.addLast(lista, estacion)
            mp.put(analizer['scc'], scca, lista)
        else:
            llaveValor=mp.get(analizer['scc'], scca)
            lista=me.getValue(llaveValor)
            if lt.isPresent(lista, estacion)==0:
                lt.addLast(lista,estacion)
    
    listaTuplas=lt.newList()
    for sccc in lt.iterator(mp.keySet(analizer['scc'])):
        llavevalor=mp.get(analizer['scc'], sccc)
        valor=me.getValue(llavevalor)
        size=lt.size(valor)
        vertex=lt.getElement(valor, 1)
        componenteFuerte=sccc
        lt.addLast(listaTuplas, ('IDcomponente: '+str(componenteFuerte),'TAMANIO: '+str(size),'vertice mas concurrido: ' +str(vertex)))
    listaFinal=sh.sort(listaTuplas, cmpOutdegree)
    return(listaFinal, count)

#Req 4
def requerimiento4(analizer, verticeI, verticeF):
    search=dij.Dijkstra(analizer['dirGraph'], verticeI)
    ruta=dij.pathTo(search, verticeF )
    time=dij.distTo(search, verticeF)
    return(ruta, time)

#Req 6
def tripList(analizer, trip):
    lt.addLast(analizer['tripList'], trip)

def bikeNum(analizer, bikeId):
    listaBikeId=lt.newList("ARRAY_LIST")
    for valor in lt.iterator(analizer['tripList']):
        if int(float(valor['Bike Id']))==bikeId:
            lt.addLast(listaBikeId, valor)
    return(lt.size(listaBikeId))


   

    
    



































# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
