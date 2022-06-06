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
from itertools import count
from msilib.schema import Component
from multiprocessing import connection
import queue
from tkinter.messagebox import NO
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bmf
from DISClib.Algorithms.Graphs import prim 
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.ADT import stack
from DISClib.Utils import error as error
import csv
import sys
import pandas as pd
from tabulate import tabulate
import copy
import time
from time import mktime
import datetime
from datetime import date
from datetime import time
from datetime import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


def newCatalog():
    """ Inicializa el analizador

   stations: Tabla de hash para guardar los vertices del grafo
   trips: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    # try:
    catalog = {
        "bikes": None,
        "stations": None,
        "trips": None,
        "components": None,
        "paths": None,
        "searchdjk": None, 
        "searchbmf": None
    }

    catalog["stations"] = mp.newMap(numelements=800,
                                    maptype="PROBING",
                                    comparefunction=cmpStations)

    catalog["connections"] = mp.newMap(numelements=639200,
                                        maptype="PROBING",
                                        comparefunction=cmpStations)

    catalog["connectionsC"] = mp.newMap(numelements=639200,
                                        maptype="PROBING",
                                        comparefunction=cmpStations)
    
    catalog["connectionsA"] = mp.newMap(numelements=639200,
                                        maptype="PROBING",
                                        comparefunction=cmpStations)

    catalog["connectionsND"] = mp.newMap(numelements=639200,
                                            maptype="PROBING",
                                            comparefunction=cmpStations)

    catalog["tripsxduration"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=639200,
                                            comparefunction=cmpStations)

    catalog["tripsxdurationND"] = gr.newGraph(datastructure="ADJ_LIST",
                                                directed=False,
                                                size=639200,
                                                comparefunction=cmpStations)

    catalog["tripsxamount"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=639200,
                                            comparefunction=cmpStations)

    catalog["tripsxcasual"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=639200,
                                            comparefunction=cmpStations)
                                        
    catalog["tripsxannual"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=639200,
                                            comparefunction=cmpStations)

    catalog["stationnamexid"] = mp.newMap(numelements=800,
                                            maptype="PROBING",
                                            comparefunction=cmpStations)
    
    catalog["idxstationname"] = mp.newMap(numelements=800,
                                            maptype="PROBING",
                                            comparefunction=cmpStations)

    catalog["fixedstation"] = mp.newMap(numelements=800,
                                        maptype="PROBING",
                                        comparefunction=cmpStations)


    catalog["arrivalaux1"] = mp.newMap(numelements=18400,
                                        maptype="PROBING",
                                        comparefunction=cmpStations)

    catalog["searchdjk"] = {"search": None,
                            "graphname": None,
                            "vertex": None}

    catalog["searchscc"] = {"search": None,
                            "graphname": None,
                            "vertex": None} 

    catalog["MST"] = {"search": None,
                        "graphname": None,
                        "vertex": None}

    catalog["bfs"] = {"search": None,
                        "graphname": None,
                        "vertex": None}

    catalog["dfs"] = {"search": None,
                        "graphname": None,
                        "vertex": None}

    catalog["datalist"] = lt.newList("SINGLE_LINKED")
    return catalog
    # except Exception as exp:
    #     error.reraise(exp, "model:newcatalog")


def addTripList(catalog, trip):
    lt.addLast(catalog["datalist"], trip)


def loadData(catalog):
    tripslist = catalog["datalist"]
    totaltrips = lt.size(tripslist)
    for trip in lt.iterator(tripslist):
        origin = int(float(trip["Start Station Id"]))
        destination = int(float(trip["End Station Id"]))
        catalog, origin = addStationD(catalog, origin, trip, "origen")
        catalog, destination = addStationD(catalog, destination, trip, "destino")
        addConnectionD(catalog, origin, destination, trip)

    for edge in lt.iterator(gr.edges(catalog["tripsxduration"])):
        connectionid = (edge["vertexA"], edge["vertexB"])
        connection = mp.get(catalog["connections"], connectionid)["value"]

        suma = 0
        for duration in lt.iterator(connection["tripsdurations"]):
            suma += int(duration)

        connection["durationprom"] = promedio(suma, connection["tripsamount"])
        edge["weight"] = promedio(suma, connection["tripsamount"])

    addConnectionND(catalog)
    vertexND = gr.numVertices(catalog["tripsxdurationND"])
    edgesND = gr.numEdges(catalog["tripsxdurationND"])
    vertexlist = gr.vertices(catalog["tripsxduration"])
    vertexlistND = gr.vertices(catalog["tripsxdurationND"])

    dfD = prints(catalog, vertexlist, 0)
    dfND = prints(catalog, vertexlistND, 1)

    
    return totaltrips, dfD, dfND, vertexND, edgesND

def prints(catalog, vertexlist, index):
    size = lt.size(vertexlist)
    sa.sort(vertexlist, cmpVertex)

    if size < 5:
        trips5x5 = lt.subList(vertexlist, 1, size)
    elif size < 10:
        t1 = lt.subList(vertexlist, 1, 5)
        t2 = lt.subList(vertexlist, 6, size-5)
        trips5x5 = lt.concat(t1, t2, "ARRAY_LIST")
    else:
        t1 = lt.subList(vertexlist, 1, 5)
        t2 = lt.subList(vertexlist, size - 4, 5)
        trips5x5 = lt.concat(t1, t2, "ARRAY_LIST")

    newvertex = lt.newList()

    catalog["arrivalaux"] = mp.newMap(numelements=18400,
                                      maptype="PROBING")

    if index == 0:
        for vertex in lt.iterator(trips5x5):
            dict = {"Station ID": vertex,
                    "Station Name": None,
                    "In Degree (Routes)": None,
                    "Out Degree (Routes)": None,
                    "Departure Trips": None,
                    "Arrival Trips": None}

            dict["Station Name"] = mp.get(catalog["idxstationname"], vertex)["value"]
            dict["Out Degree (Routes)"] = gr.outdegree(catalog["tripsxamount"], vertex)
            dict["In Degree (Routes)"] = gr.indegree(catalog["tripsxamount"], vertex)
            dict["Departure Trips"] = tripsDepartureCount(catalog["tripsxamount"], vertex)
            dict["Arrival Trips"] = tripsArrivalCount(catalog, catalog["tripsxamount"], vertex)

            lt.addLast(newvertex, dict)
    elif index == 1:
        for vertex in lt.iterator(trips5x5):
            dict = {"Station ID": vertex,
                    "Station Name": None}
            
            dict["Station Name"] = mp.get(catalog["idxstationname"], vertex)["value"]
            dict["Degree (Routes)"] = gr.degree(catalog["tripsxdurationND"], vertex)

            lt.addLast(newvertex, dict)

    
    df = dataFrame(newvertex, 1)
    return df


def addStationD(catalog, id, trip, type):
    """
    Adiciona una estación como un vertice del grafo
    """
    # try:
    if id == int(float(trip["Start Station Id"])):
        name = formatStr(trip["Start Station Name"])
        name = name.lower()
        id = fixID(catalog, id, trip["Start Station Name"])
        if name != "":
            mp.put(catalog["stationnamexid"], name, id)
        mp.put(catalog["idxstationname"], id, trip["Start Station Name"])
    elif id == int(float(trip["End Station Id"])):
        name = formatStr(trip["End Station Name"])
        name = name.lower()
        id = fixID(catalog, id, trip["End Station Name"])
        if name != "":
            mp.put(catalog["stationnamexid"], name, id)
        mp.put(catalog["idxstationname"], id, trip["End Station Name"])

    if not gr.containsVertex(catalog["tripsxduration"], id) and not gr.containsVertex(catalog["tripsxamount"], id):
        gr.insertVertex(catalog["tripsxduration"], id)
        gr.insertVertex(catalog["tripsxamount"], id)
        gr.insertVertex(catalog["tripsxdurationND"], id)

    if mp.contains(catalog["stations"], id):
        entry = mp.get(catalog["stations"], id)
        entry = me.getValue(entry)
    else:
        entry = {"Station ID": id,
                 "Departure Time": mp.newMap(numelements=180, maptype="PROBING"),
                 "Departure Dates": mp.newMap(numelements=180, maptype="PROBING"),
                 "Departure Hours": mp.newMap(numelements=180, maptype="PROBING")}

        mp.put(catalog["stations"], id, entry)
    
    if type == "origen":
        starttime = trip["Start Time"]
        date, hour = starttime.split(" ")
        date = str(formatDate(date))
        hour = str(formatHour(hour))

        addDate(entry["Departure Dates"], date)
        addDate(entry["Departure Hours"], hour)

    if not gr.containsVertex(catalog["tripsxannual"], id) and trip["User Type"] == "Annual Member":
        gr.insertVertex(catalog["tripsxannual"], id)
    elif not gr.containsVertex(catalog["tripsxcasual"], id) and trip["User Type"] == "Casual Member":
        gr.insertVertex(catalog["tripsxcasual"], id)

    return catalog, id
    # except Exception as exp:
    #     error.reraise(exp, "model:addstop")

def fixID(catalog, id, name):
    name = formatStr(name)
    if mp.contains(catalog["idxstationname"], id):
        name2cmp = mp.get(catalog["idxstationname"], id)["value"]
        name2cmp = formatStr(name2cmp)

        if name != name2cmp:
            id += 1000
            id = fixID(catalog, id, name)

    return id

def formatStr(str):
    whitelist = set('abcdefghijklmnopqrstuvwxyz/-,ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    str = ''.join(filter(whitelist.__contains__, str))
    str = str.lower()
    return str
        
        
def addDate(map, date):
    if mp.contains(map, date):
        entry = mp.get(map, date)["value"]
    else:
        entry = {"date": date, "count": 0}
        mp.put(map, date, entry)
    entry["count"] += 1
#d
def addConnectionD(catalog, origin, destination, trip):
    """
    Adiciona un arco entre dos estaciones
    """
    connectionid = (origin, destination)
    if trip["User Type"] == "Annual Member":
        graphname = catalog["tripsxannual"]
        mapname = catalog["connectionsA"]
    elif trip["User Type"] == "Casual Member":
        graphname = catalog["tripsxcasual"]
        mapname = catalog["connectionsC"]

    exists1 = gr.getEdge(catalog["tripsxduration"], origin, destination)
    exists2 = gr.getEdge(graphname, origin, destination)
    
    if exists1 != None:
        entry1 = mp.get(catalog["connections"], connectionid)
        entry1 = me.getValue(entry1)
    else:
        gr.addEdge(catalog["tripsxduration"], origin, destination)
        gr.addEdge(catalog["tripsxamount"], origin, destination)
        entry1 = {"connectionid": connectionid,
                  "origin": origin,
                  "destination": destination,
                  "tripsid": lt.newList(),
                  "tripsdurations": lt.newList(),
                  "tripsamount": None}
        mp.put(catalog["connections"], connectionid, entry1)

    if exists2 != None:
        entry2 = mp.get(mapname, connectionid)
        entry2 = me.getValue(entry2)
    else:
        gr.addEdge(graphname, origin, destination)
        entry2 = {"connectionid": connectionid,
                  "origin": origin,
                  "destination": destination,
                  "tripsid": lt.newList(),
                  "tripsdurations": lt.newList(),
                  "tripsamount": None}
        mp.put(mapname, connectionid, entry2)

    lt.addLast(entry1["tripsid"], trip["Trip Id"])
    lt.addLast(entry1["tripsdurations"], trip["Trip  Duration"])
    entry1["tripsamount"] = lt.size(entry1["tripsid"])
    lt.addLast(entry2["tripsid"], trip["Trip Id"])
    lt.addLast(entry2["tripsdurations"], trip["Trip  Duration"])
    entry2["tripsamount"] = lt.size(entry2["tripsid"])

    amountedge1 = gr.getEdge(catalog["tripsxamount"], origin, destination)
    amountedge1["weight"] = entry1["tripsamount"]

    amountedge2 = gr.getEdge(graphname, origin, destination)
    amountedge2["weight"] = entry2["tripsamount"]

    return catalog


def addConnectionND(catalog):
    """
    Adiciona un arco entre dos estaciones
    """
    vertexlist = gr.vertices(catalog["tripsxduration"])
    for vertexa in lt.iterator(vertexlist):
        for vertexb in lt.iterator(vertexlist):
            edge1 = gr.getEdge(catalog["tripsxduration"], vertexa, vertexb)
            edge2 = gr.getEdge(catalog["tripsxduration"], vertexb, vertexa)
            if edge1 != None and edge2 != None:
                connectionid = fixConnectionID(vertexa, vertexb)
                exists = gr.getEdge(catalog["tripsxdurationND"], connectionid[0], connectionid[1])
                if exists != None:
                    entry = mp.get(catalog["connectionsND"], connectionid)
                    entry = me.getValue(entry)
                    durationedge = exists
                else:
                    gr.addEdge(catalog["tripsxdurationND"], connectionid[0], connectionid[1])
                    durationedge = gr.getEdge(catalog["tripsxdurationND"], connectionid[0], connectionid[1])
                    entry = {"connectionid": connectionid,
                            "vertexa": connectionid[0],
                            "vertexb": connectionid[1],
                            "tripsid": None,
                            "tripsdurations": None,
                            "tripsamount": None}
                    mp.put(catalog["connectionsND"], connectionid, entry)
                connectionid2 = (connectionid[1], connectionid[0])
                ids1 = mp.get(catalog["connections"], connectionid)["value"]["tripsid"]
                ids2 = mp.get(catalog["connections"], connectionid2)["value"]["tripsid"]
                ids = lt.concat(ids1, ids2)
                duration1 = mp.get(catalog["connections"], connectionid)["value"]["tripsdurations"]
                duration2 = mp.get(catalog["connections"], connectionid2)["value"]["tripsdurations"]
                durationlist = lt.concat(duration1, duration2)
                entry["tripsid"] = ids
                entry["tripsdurations"] = durationlist
                entry["tripsamount"] = lt.size(entry["tripsid"])
                weight = edge1["weight"] + edge2["weight"]
                entry["durationprom"] = promedio(weight, 2)
                durationedge["weight"] = promedio(weight, 2)

    return catalog


def fixConnectionID(vxa, vxb):
    if vxa < vxb:
        id = (vxa, vxb)
    elif vxa > vxb:
        id = (vxb, vxa)

    return id


def promedio(sum, count):
    return sum/count


def totalStops(catalog):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(catalog["tripsxduration"])


def totalConnections(catalog):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(catalog["tripsxamount"])


def cmpStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1


def cmpTrips(trip1, trip2):
    """
    Compara dos rutas
    """
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1


def cmpTripsID(trip1, trip2):
    return int(trip1["Trip Id"]) < int(trip2["Trip Id"])


def cmpTripsDuration(trip1, trip2):
    return int(trip1["Trip  Duration"]) < int(trip2["Trip  Duration"])


def cmpStationDepartures(station1, station2):
    return int(station1["Departure Trips"]) > int(station2["Departure Trips"])


def cmpVertex(vertex1, vertex2):
    return vertex1 < vertex2

def cmpComponents(component1, component2):
    return lt.size(component1["Stations IDs"]) > lt.size(component2["Stations IDs"])


def formatDate(fecha):
    if len(fecha) == 4:
        y = int(fecha)
        joined = date(year=y, month=1, day=1)        
    elif len(fecha) <= 7:
        str = fecha
        lista = str.split("/")
        str = "01 "+ lista[0] + " " + lista[1]
        joined = time.strptime(str, "%d %b %y")
        joined = date.fromtimestamp(mktime(joined))
    else:
        joined = fecha

    joined = joined + " 00:00:00"

    dt_object = datetime.strptime(joined, "%m/%d/%Y %H:%M:%S").date()

    return dt_object


def formatHour(time):
    hour, min = time.split(":")

    return hour


def dataFrame(trips, vuelta):
    # try:
    size = lt.size(trips)

    if vuelta <= 2:
        trips5x5 = trips

    elif vuelta == 3:
        if size < 5:
            trips5x5 = lt.subList(trips, 1, size)
        else:
            trips5x5 = lt.subList(trips, 1, 5)

    elif vuelta >= 4:
        if size < 3:
            trips5x5 = lt.subList(trips, 1, size)
        elif size < 6:
            t1 = lt.subList(trips, 1, 3)
            t2 = lt.subList(trips, 4, size-3)
            trips5x5 = lt.concat(t1, t2, "ARRAY_LIST")
        else:
            t1 = lt.subList(trips, 1, 3)
            t2 = lt.subList(trips, size - 2, 3)
            trips5x5 = lt.concat(t1, t2, "ARRAY_LIST")

    dftrips = pd.DataFrame()
    dftrips.reset_index(drop=True)

    for trip in lt.iterator(trips5x5):
        for key in trip.keys():
            tripkey = trip[key]
            tripkey = str(tripkey)
            x = len(tripkey)
            if x == 0:
                trip[key] = "Unknown"

        dftrips_new = pd.DataFrame(trip, index=[None])
        dftrips = pd.concat([dftrips, dftrips_new])
        
    if vuelta == 2:
        dftrips = dftrips[["Component number", "Cantidad", "Stations IDs", "Most Departures ID", "Most Departures Name", "Most Arrivals ID", "Most Arrivals Name"]]

    for key in dftrips.columns:
        if key == "Station Name" or key == "Stations IDs":
            dftrips[key] = dftrips[key].str.wrap(35)


    df = tabulate(dftrips, headers="keys", tablefmt='fancy_grid', showindex=False)

    return df

    # except Exception:
    #     return None


def popularStations(catalog):
    vertexlist = gr.vertices(catalog["tripsxamount"])
    newvertex = lt.newList()

    for vertex in lt.iterator(vertexlist):
        dict = {"Station ID": vertex,
                "Departure Trips": tripsDepartureCount(catalog["tripsxamount"], vertex),
                "Out Degree": gr.outdegree(catalog["tripsxamount"], vertex)}

        lt.addLast(newvertex, dict)

    sa.sort(newvertex, cmpStationDepartures)
    size = lt.size(newvertex)

    if size < 5:
        stations5 = lt.subList(newvertex, 1, size)
    else:
        stations5 = lt.subList(newvertex, 1, 5)

    for station in lt.iterator(stations5):
        station["Station Name"] = mp.get(catalog["idxstationname"], station["Station ID"])["value"]
        if gr.containsVertex(catalog["tripsxcasual"], station["Station ID"]):
            station["Casual Member Trips"] = tripsDepartureCount(catalog["tripsxcasual"], station["Station ID"])
        else:
            station["Casual Member Trips"] = 0

        if gr.containsVertex(catalog["tripsxannual"], station["Station ID"]):
            station["Annual Member Trips"] = tripsDepartureCount(catalog["tripsxannual"], station["Station ID"])
        else:
            station["Annual Member Trips"] = 0

        entry = mp.get(catalog["stations"], station["Station ID"])["value"]
        map2 = entry["Departure Dates"]
        map3 = entry["Departure Hours"]


        maxkey1, maxamount1 = maxKey(map2, "count")
        maxkey2, maxamount2 = maxKey(map3, "count")


        maxkey2 = str(maxkey2) + ":00 - " + str(maxkey2) + ":59"
       

        station["Rush Date"] = str(maxkey1) + " (" + str(maxamount1) + ")"
        station["Rush Hour"] = str(maxkey2) + " (" + str(maxamount2) + ")"
    
    df = dataFrame(stations5, 1)
    
    return df

def tripsDepartureCount(graph, id):
    count = 0
    if gr.containsVertex(graph, id):
        adjlist = gr.adjacentEdges(graph, id)
        for edge in lt.iterator(adjlist):
            if edge["vertexA"] == id:
                count += edge["weight"]
    return count


def tripsArrivalCount(catalog, graph, id):
    initMap(catalog, graph)
    if mp.contains(catalog["arrivalaux"], id):
        count = mp.get(catalog["arrivalaux"], id)["value"]["count"]
    else:
        count = 0
    return count


def initMap(catalog, graph):
    if mp.isEmpty(catalog["arrivalaux"]):
        vertexlist = gr.vertices(graph)
        for vertex in lt.iterator(vertexlist):
            adjlist = gr.adjacentEdges(graph, vertex)
            for edge in lt.iterator(adjlist):
                vertexb = edge["vertexB"]
                if mp.contains(catalog["arrivalaux"], vertexb):
                    entry = mp.get(catalog["arrivalaux"], vertexb)["value"]
                else:
                    entry = {"id": vertexb, "count": 0}
                    mp.put(catalog["arrivalaux"], vertexb, entry)
                entry["count"] += edge["weight"]


def maxKey(map, element):
    keylist = mp.keySet(map)
    sa.sort(keylist, cmpVertex)
    maxkey = "Unknown"
    maxamount = 0

    for key in lt.iterator(keylist):
        if key != None:
            actkey = key
            actamount = int(mp.get(map, key)["value"][element])
            if actamount > maxamount:
                maxkey = actkey
                maxamount = actamount
    return maxkey, maxamount


def initSearch(type, catalog, graphname, vertex=None):
    if (catalog[type]["search"] == None) or (catalog[type]["graphname"] != graphname) or (catalog[type]["vertex"] != vertex):
        if type == "searchdjk":
            catalog[type]["search"] = djk.Dijkstra(catalog[graphname], vertex)
        elif type == "searchscc":
            catalog[type]["search"] = scc.KosarajuSCC(catalog[graphname])
        elif type == "MST":
            catalog[type]["search"] = prim.PrimMST(catalog[graphname], vertex)
        elif type == "bfs":
            catalog[type]["search"] = bfs.BreadhtFisrtSearch(catalog[graphname], vertex)
        elif type == "dfs":
            catalog[type]["search"] = dfs.DepthFirstSearch(catalog[graphname], vertex)

        catalog[type]["graphname"] = graphname
        catalog[type]["vertex"] = vertex
        
    return catalog


def planTrips(catalog, name, available, minst, maxrt):
    name = formatStr(name)
    name = name.lower()

    stationid = mp.get(catalog["stationnamexid"], name)["value"]

    initSearch("searchdjk", catalog, "tripsxdurationND", stationid)
    searchdjk = catalog["searchdjk"]["search"]

    vertexlist = gr.vertices(catalog["tripsxdurationND"])
    sa.sort(vertexlist, cmpVertex)
    newvertex = lt.newList()

    count = 0

    for vertex in lt.iterator(vertexlist):
        path = djk.pathTo(searchdjk, vertex)
        cost = 2* djk.distTo(searchdjk, vertex)
        if path != None:
            size = stack.size(path)
        else:
            size = 0

        if size > minst+1 and cost < available and lt.size(newvertex) < maxrt:
            dict = pathLists(catalog, size, path, vertex)
            dict["Route Time"] = cost // 2
            dict["Roundtrip Time"] = cost
            lt.addLast(newvertex, dict)

    df = dataFrame(newvertex, 1)
    
    return df


def pathList2(catalog, size, path, vertex):
    dict = {"Destination": vertex,
            "Stations in order": lt.newList("ARRAY_LIST"),
            "Stop Stations": size,
            "Route Time": None,
            "Roundtrip Time": None}

    for x in range(size-1):
        actid = stack.pop(path)
        actname = mp.get(catalog["idxstationname"], actid)["value"]
        actstation = str(actid) + " - " + str(actname)
        lt.addLast(dict["estaciones"], actstation)

    dict["estaciones"] = listToStr(dict["estaciones"], 1)
    
    return dict
    

def pathLists(catalog, size, path, vertex):
    dict = {"Destination": vertex,
            "Stations in order": lt.newList("ARRAY_LIST"),
            "Stop Stations": size,
            "Route Time": None,
            "Roundtrip Time": None}

    for x in range(size-1):
        if x == 0:
            actedge = stack.pop(path)
            actid1 = actedge["vertexA"]
            actname1 = mp.get(catalog["idxstationname"], actid1)["value"]
            actstation1 = str(actid1) + " - " + str(actname1)
            lt.addLast(dict["Stations in order"], actstation1)
            actid2 = actedge["vertexB"]
            actname2 = mp.get(catalog["idxstationname"], actid2)["value"]
            actstation2 = str(actid2) + " - " + str(actname2)
            lt.addLast(dict["Stations in order"], actstation2)
        elif x > 0 and x < size:
            actid = stack.pop(path)["vertexB"]
            actname = mp.get(catalog["idxstationname"], actid)["value"]
            actstation = str(actid) + " - " + str(actname)
            lt.addLast(dict["Stations in order"], actstation)

    dict["Stations in order"] = listToStr(dict["Stations in order"], 1)
    
    return dict


def stronglyConnected(catalog):
    initSearch("searchscc", catalog, "tripsxamount")
    searchscc = catalog["searchscc"]["search"]
    keylist = mp.keySet(searchscc["idscc"])

    mapa = mp.newMap(numelements=100, maptype="PROBING")

    for key in lt.iterator(keylist):
        component = mp.get(searchscc["idscc"], key)["value"]
        if mp.contains(mapa, component):
            entry = mp.get(mapa, component)["value"]
        else:
            entry = {"Component number": component,
                     "Stations IDs": lt.newList()}
        lt.addLast(entry["Stations IDs"], key)
        mp.put(mapa, component, entry)

    componentlist = mp.valueSet(mapa)
    sa.sort(componentlist, cmpComponents)

    size = lt.size(componentlist)

    if size < 5:
        stations5 = lt.subList(componentlist, 1, size)
    else:
        stations5 = lt.subList(componentlist, 1, 5)

    counter = 1

    for dict in lt.iterator(stations5):
        maxkeyd = lt.firstElement(dict["Stations IDs"])
        maxkeya = lt.firstElement(dict["Stations IDs"])
        for actstation in lt.iterator(dict["Stations IDs"]):
            maxkeya, maxkeyd = maxDA(catalog["tripsxamount"], maxkeyd, maxkeya, actstation)
        dict["Cantidad"] = lt.size(dict["Stations IDs"])
        dict["Stations IDs"] = listToStr(dict["Stations IDs"])
        dict["Most Departures ID"] = maxkeyd
        dict["Most Departures Name"] = mp.get(catalog["idxstationname"], maxkeyd)["value"]
        dict["Most Arrivals ID"] = maxkeya
        dict["Most Arrivals Name"] = mp.get(catalog["idxstationname"], maxkeya)["value"]
        counter += 1

    df = dataFrame(stations5, 2)

    return size, df

def maxDA(graph, maxkeyd, maxkeya, actstation):
    maxd = gr.outdegree(graph, maxkeyd) 
    maxa = gr.indegree(graph, maxkeya)
    actd = gr.outdegree(graph, actstation) 
    acta = gr.indegree(graph, actstation)
    if actd > maxd:
        maxd = actd
        maxkeyd = actstation
    
    if acta > maxa:
        maxa = acta
        maxkeya = actstation
    return maxkeya, maxkeyd

def listToStr(lista, index=None):
    size = lt.size(lista)
    cadena = ""
    counter = 1
    for element in lt.iterator(lista):
        if counter != size:
            if index == 1:
                cadena += str(element) + ", \n"
            else:
                cadena += str(element) + ", "
        else:
            cadena += str(element)
        counter += 1

    if len(cadena) > 99 and not index == 1:
        cadena = cadena[:100] + " (...)"
    return cadena


def fastRoute(catalog, origen, destino):
    origen = formatStr(origen)
    origen = origen.lower()
    destino = formatStr(destino)
    destino = destino.lower()

    originid = mp.get(catalog["stationnamexid"], origen)["value"]
    destinationid = mp.get(catalog["stationnamexid"], destino)["value"]

    initSearch("searchdjk", catalog, "tripsxduration", originid)
    searchdjk = catalog["searchdjk"]["search"]

    cost = round(djk.distTo(searchdjk, destinationid))
    path = djk.pathTo(searchdjk, destinationid)
    size = stack.size(path) 

    newstations = lt.newList()

    for x in range(size):
        dict = {"Station ID": None,
                "Station Name": None,
                "Time to next station": None}
        if x == size-1:
            id = stack.pop(path)
            id1 = id["vertexA"]
            id2 = id["vertexB"]
            dict["Station ID"] = id1
            dict["Station Name"] = mp.get(catalog["idxstationname"], id1)["value"]
            dict["Time to next station"] = int(float(gr.getEdge(catalog["tripsxduration"], id1, id2)["weight"]))
            lt.addLast(newstations, dict)
            dict2 = {"Station ID": None,
                    "Station Name": None,
                    "Time to next station": None}
            dict2["Station ID"] = id2
            dict2["Station Name"] = mp.get(catalog["idxstationname"], id2)["value"]
            dict2["Time to next station"] = "End"
            lt.addLast(newstations, dict2)
        else:
            id = stack.pop(path)
            id1 = id["vertexA"]
            id2 = id["vertexB"]
            dict["Station ID"] = id1
            dict["Station Name"] = mp.get(catalog["idxstationname"], id1)["value"]
            dict["Time to next station"] = int(float(gr.getEdge(catalog["tripsxduration"], id1, id2)["weight"]))
            lt.addLast(newstations, dict)

    if lt.size(newstations) >= 12:
        t1 = lt.subList(newstations, 1, 3)
        t2 = lt.subList(newstations, lt.size(newstations) - 2, 3)
        newstations = lt.concat(t1, t2, "ARRAY_LIST")

    df = dataFrame(newstations, 1)
    return cost, df

def routesInDateRange(catalog, min, max):
    min = formatDate(min)
    max = formatDate(max)
    dateMap2(catalog, min, max)

    tripslist = lt.newList()
    keylist = om.keys(catalog["annualxdate"], min, max)
    for key in lt.iterator(keylist):
        entry = om.get(catalog["annualxdate"], key)["value"]
        lt.concat(tripslist, entry["Trips"])

    graph, x = dateGraph(catalog, tripslist)

    size = lt.size(tripslist)
    mapa = mp.newMap(numelements=100,
           maptype="PROBING")

    totalduration = 0

    catalog["arrivalaux"] = mp.newMap(numelements=18400,
                                      maptype="PROBING")

    for trip in lt.iterator(tripslist):
        addStationAnnual2(catalog, graph, mapa, trip["Start Station Name"], int(float(trip["Start Station Id"])))
        addStationAnnual2(catalog, graph, mapa, trip["End Station Name"], int(float(trip["End Station Id"])))
        totalduration += int(float(trip["Trip  Duration"]))
    
    maxkeyO, maxamountO = maxKey(mapa, "Origin")
    maxkeyD, maxamountD = maxKey(mapa, "Destination")
    maxkeyS, maxamountS = maxKey(catalog["annualxhour"], "Start")
    maxkeyE, maxamountE = maxKey(catalog["annualxhour"], "End")

    nameO = mp.get(catalog["idxstationname"], maxkeyO)["value"]
    nameD = mp.get(catalog["idxstationname"], maxkeyD)["value"]

    maxkeyS = str(maxkeyS) + ":00 - " + str(maxkeyS) + ":59"
    maxkeyE = str(maxkeyE) + ":00 - " + str(maxkeyE) + ":59"

    x = lt.newList()
    dict = {"Total Trips": size,
            "Total Duration": totalduration,
            "Popular Departure Station": str(maxkeyO) + " - " + str(nameO) + " (" + str(maxamountO) + ")",
            "Popular Arrival Station": str(maxkeyD) + " - " + str(nameD) + " (" + str(maxamountD) + ")",
            "Popular Start Hour": maxkeyS + " (" + str(maxamountS) + ")",
            "Popular End Hour": maxkeyE + " (" + str(maxamountE) + ")"}
    lt.addLast(x, dict)

    df = dataFrame(x, 1)
    return df


def dateMap2(catalog, stardate, enddate):
    catalog["annualxdate"] = om.newMap(omaptype="RBT")
    catalog["annualxhour"] = mp.newMap(numelements=30,
                                       maptype="PROBING")
    datemap = catalog["annualxdate"]
    hourmap = catalog["annualxhour"]
    for trip in lt.iterator(catalog["datalist"]):
        if trip["User Type"] == "Annual Member":
            starttime = trip["Start Time"]
            date, hour = starttime.split(" ")
            date = formatDate(date)
            hour = formatHour(hour)
            if om.contains(datemap, date):
                entry = om.get(datemap, date)["value"]
            else:
                entry = {"Date": date,
                         "Trips": lt.newList()}
                om.put(datemap, date, entry)
            lt.addLast(entry["Trips"], trip)

            if date > stardate and date < enddate:
                if mp.contains(hourmap, hour):
                    entry = mp.get(hourmap, hour)["value"]
                else:
                    entry = {"Hour": hour,
                            "Start": 0,
                            "End": 0}
                    mp.put(hourmap, hour, entry)

                entry["Start"] += 1

                endtime = trip["End Time"]
                date, hour2 = endtime.split(" ")
                hour2 = str(formatHour(hour2))

                if mp.contains(hourmap, hour2):
                    entry = mp.get(hourmap, hour2)["value"]
                else:
                    entry = {"Hour": hour2,
                            "Start": 0,
                            "End": 0}
                    mp.put(hourmap, hour2, entry)

                entry["End"] += 1


def dateGraph(catalog, tripslist):
    graph = gr.newGraph(datastructure="ADJ_LIST",
                        directed=True,
                        size=639200,
                        comparefunction=cmpStations)

    mapa = mp.newMap(numelements=30,
                     maptype="PROBING")

    for trip in lt.iterator(tripslist):
        origin = int(float(trip["Start Station Id"]))
        origin = checkID(catalog, trip["Start Station Name"], origin)
        destination = int(float(trip["End Station Id"]))
        destination = checkID(catalog, trip["End Station Name"], destination)
        connectionid = (origin, destination)

        if not gr.containsVertex(graph, origin):
            gr.insertVertex(graph, origin)
        if not gr.containsVertex(graph, destination):
            gr.insertVertex(graph, destination)

        exists1 = gr.getEdge(graph, origin, destination)
        
        if exists1 != None:
            entry1 = mp.get(mapa, connectionid)["value"]
        else:
            gr.addEdge(graph, origin, destination)
            entry1 = {"connectionid": connectionid,
                    "origin": origin,
                    "destination": destination,
                    "tripsid": lt.newList(),
                    "tripsdurations": lt.newList(),
                    "tripsamount": None}
            mp.put(mapa, connectionid, entry1)

        lt.addLast(entry1["tripsid"], trip["Trip Id"])
        lt.addLast(entry1["tripsdurations"], trip["Trip  Duration"])
        entry1["tripsamount"] = lt.size(entry1["tripsid"])
        amountedge1 = gr.getEdge(graph, origin, destination)
        amountedge1["weight"] = entry1["tripsamount"]

    return graph, mapa


def addStationAnnual2(catalog, graph, mapa, name, givenid):
    id = checkID(catalog, name, givenid)
    if not mp.contains(mapa, id):
        entry = {"Origin": tripsDepartureCount(graph, id), 
                 "Destination": tripsArrivalCount(catalog, graph, id)}
        mp.put(mapa, id, entry)


def checkID(catalog, name, givenid):
    name = formatStr(name)
    name2 = mp.get(catalog["idxstationname"], givenid)
    if name2:
        name2 = formatStr(name2["value"])

    if name == name2:
        id = int(givenid)
    elif mp.contains(catalog["stationnamexid"], name):
        id = mp.get(catalog["stationnamexid"], name)["value"]
    else:
        id = copy.deepcopy(givenid)
        id += 1000
        checkID(catalog, name, id)

    return id


def infoStation(catalog, station, startdate, starthour, enddate, endhour):
    station = formatStr(station)
    station = station.lower()
    startdate = formatDate(startdate)
    starthour = formatHour(starthour)
    enddate = formatDate(enddate)
    endhour = formatHour(endhour)
    id = mp.get(catalog["stationnamexid"], station)["value"]
    tripslist = mp.get(catalog["stations"], id)["value"]
    tripslist = tripslist["Trips"]

    catalog["arrivalaux"] = mp.newMap(numelements=18400,
                                      maptype="PROBING")

    startdatelist = filteredList(tripslist, "Start", startdate, enddate, starthour, endhour)
    enddatelist = filteredList(tripslist, "End", startdate, enddate, starthour, endhour)

    graph1, mapa1 = dateGraph(catalog, startdatelist)
    graph2, mapa2 = dateGraph(catalog, enddatelist)

    sa.sort(startdatelist, cmpTripsDuration)

    x = lt.newList()

    dict = {"Departure Trips": str(tripsDepartureCount(graph1, id)), 
            "Arrival Trips": str(tripsArrivalCount(catalog, graph2, id)), 
            "Longest Trip Duration": str(lt.getElement(startdatelist, 1)["Trip  Duration"]), 
            "Most Arrivals To": mostArrivals(graph2, id)}

    lt.addLast(x, dict)

    df = dataFrame(x, 1)
    return df


def mostArrivals(graph, id):
    maxkey = "Unknown"
    maxamount = 0
    if gr.containsVertex(graph, id):
        adjlist = gr.adjacentEdges(graph, id)
        for edge in lt.iterator(adjlist):
            if edge["vertexA"] == id:
                if edge["weight"] > maxamount:
                    maxkey = edge["vertexB"]
                    maxamount = edge["weight"]
    return maxkey


def filteredList(tripslist, type, startdate, enddate, starthour, endhour):
    newlist = lt.newList()
    type = type + " Time"
    counter = 0
    for trip in lt.iterator(tripslist):
        datetime = trip[type]
        date, hour = datetime.split(" ")
        date = formatDate(date)
        hour = formatHour(hour)

        if trip["User Type"] == "Casual Member":
            counter += 1
            if date == startdate and hour >= starthour:
                lt.addLast(newlist, trip)
            elif date >= startdate and date <= enddate:
                lt.addLast(newlist, trip)
            elif date == enddate and hour <= endhour:
                lt.addLast(newlist, trip)

    return newlist
def bikerMaintenance(catalog, bikeId):
    trips = lt.newList("ARRAY_LIST")

    bikeId = str(float(bikeId))

    for trip in lt.iterator(catalog["datalist"]):
        if bikeId == trip["Bike Id"]:
            lt.addLast(trips,trip)

    bikerGraph(catalog,trips)

    size = lt.size(trips)
    
    mapa = mp.newMap(numelements=100,
           maptype="PROBING")
    
    totalduration = 0

    for trip in lt.iterator(trips):
        addStationBiker(catalog, mapa, trip["Start Station Name"], int(float(trip["Start Station Id"])))
        addStationBiker(catalog, mapa, trip["End Station Name"], int(float(trip["End Station Id"])))
        totalduration += int(float(trip["Trip  Duration"]))

    
    maxkeyO, maxamountO = maxKey(mapa, "Origin")
    maxkeyD, maxamountD = maxKey(mapa, "Destination")

    nameO = mp.get(catalog["idxstationname"], maxkeyO)["value"]
    nameD = mp.get(catalog["idxstationname"], maxkeyD)["value"]

    x = lt.newList()
    dict = {"Total Trips": size,
            "Total Duration": totalduration,
            "Popular Departure Station": str(maxkeyO) + " - " + str(nameO),
            "Popular Arrival Station": str(maxkeyD) + " - " + str(nameD)}
    lt.addLast(x, dict)
    
    df = dataFrame(x, 1)
    return df


def initMap(catalog, graph):
    if mp.isEmpty(catalog["arrivalaux"]):
        vertexlist = gr.vertices(graph)
        for vertex in lt.iterator(vertexlist):
            adjlist = gr.adjacentEdges(graph, vertex)
            for edge in lt.iterator(adjlist):
                vertexb = edge["vertexB"]
                if mp.contains(catalog["arrivalaux"], vertexb):
                    entry = mp.get(catalog["arrivalaux"], vertexb)["value"]
                else:
                    entry = {"id": vertexb, "count": 0}
                    mp.put(catalog["arrivalaux"], vertexb, entry)
                entry["count"] += edge["weight"]



def bikerGraph(catalog,trips):

    catalog["bikerGraph"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=50,
                                            comparefunction=cmpStations)

    catalog["bikerConnections"] = mp.newMap(numelements=30,
                                       maptype="PROBING")


    for trip in lt.iterator(trips):
        origin = int(float(trip["Start Station Id"]))
        origin = checkID(catalog, trip["Start Station Name"], origin)
        destination = int(float(trip["End Station Id"]))
        destination = checkID(catalog, trip["End Station Name"], destination)
        connectionid = (origin,destination)
       
        if not gr.containsVertex(catalog["bikerGraph"], origin):
            gr.insertVertex(catalog["bikerGraph"], origin)
        if not gr.containsVertex(catalog["bikerGraph"], destination):
            gr.insertVertex(catalog["bikerGraph"], destination)
    
        exists = gr.getEdge(catalog["bikerGraph"], origin, destination)

        if exists != None:
            entry = mp.get(catalog["bikerConnections"], connectionid)
            entry = me.getValue(entry)
        else:
            gr.addEdge(catalog["bikerGraph"], origin, destination)
            entry = {"connectionid": connectionid,
                  "origin": origin,
                  "destination": destination,
                  "tripsid": lt.newList(),
                  "tripsdurations": lt.newList(),
                  "tripsamount": None}
            mp.put(catalog["bikerConnections"], connectionid, entry)

        lt.addLast(entry["tripsid"], trip["Trip Id"])
        lt.addLast(entry["tripsdurations"], trip["Trip  Duration"])
        entry["tripsamount"] = lt.size(entry["tripsid"])
        amountedge1 = gr.getEdge(catalog["bikerGraph"], origin, destination)
        amountedge1["weight"] = entry["tripsamount"]

def addStationBiker(catalog, mapa, name, givenid):
    id = checkID(catalog, name, givenid)
    if not mp.contains(mapa, id):
        entry = {"Origin": tripsDepartureCount(catalog["bikerGraph"], id), 
                 "Destination": tripsArrivalCount1(catalog, catalog["bikerGraph"], id)}
        mp.put(mapa, id, entry)

def tripsArrivalCount1(catalog, graph, id):
    initMap1(catalog, graph)
    if mp.contains(catalog["arrivalaux1"], id):
        count = mp.get(catalog["arrivalaux1"], id)["value"]["count"]
    else:
        count = 0
    return count


def initMap1(catalog, graph):
    if mp.isEmpty(catalog["arrivalaux1"]):
        vertexlist = gr.vertices(graph)
        for vertex in lt.iterator(vertexlist):
            adjlist = gr.adjacentEdges(graph, vertex)
            for edge in lt.iterator(adjlist):
                vertexb = edge["vertexB"]
                if mp.contains(catalog["arrivalaux1"], vertexb):
                    entry = mp.get(catalog["arrivalaux1"], vertexb)["value"]
                else:
                    entry = {"id": vertexb, "count": 0}
                    mp.put(catalog["arrivalaux1"], vertexb, entry)
                entry["count"] += edge["weight"]
