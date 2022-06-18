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


from tracemalloc import start
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import graph as graph
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import datetime
from datetime import timedelta
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.Algorithms.Graphs import dfs as dfs
from DISClib.Algorithms.Graphs import dijsktra as dijsktra

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento


def newCatalog():
    catalog = {

        "trips_graph": graph.newGraph("ADJ_LIST", True, 10),
        "outdegree_ordered_graph": lt.newList("ARRAY_LIST", cmpfunction=compareByOutDegree),
        "trips": lt.newList(datastructure="ARRAY_LIST"),
        "trips_map": {},
        "stations": lt.newList(datastructure="ARRAY_LIST"),
        "start_date_ordered_trips": None,
        "stations_map": {}
    }

    return catalog

def addTrip(trips, trip):
    if not trip["Start Station Id"] == "" and not trip["End Station Id"] == "":
        lt.addLast(trips, trip)

def addStations(stations, station):
    lt.addLast(stations, station)

def getTime(tiempo_inicial, tiempo_final):
    tiempo_total = stringToDateTime(tiempo_final) - stringToDateTime(tiempo_inicial)
    return tiempo_total


def stringToDateTime(string):
    return datetime.strptime(string, '%m/%d/%Y %H:%M')

def stringToDate(string):
    return stringToDateTime(string).date().strftime("%m/%d/%Y")


def stringToHourMinute(string):
    return stringToDateTime(string).strftime('%H:%M')

def stringToHour(string):
    return stringToDateTime(string).strftime('%H')

def numVertex(trips_graph):
    return graph.numVertices(trips_graph)

def numEdges(trips_graph):
    return graph.numEdges(trips_graph)

def createKey(start_id, end_id):
    return (str(start_id) + "," + str(end_id))

def addToTripsMap(trips_map, trip):
    if not trip["Start Station Id"] == "" and not trip["End Station Id"] == "":
        start_station_id = int(float(trip["Start Station Id"]))
        end_station_id = int(float(trip["End Station Id"]))
        key = createKey(start_station_id, end_station_id)
        if key in trips_map:
            saved_trip = trips_map[key]
            saved_trip["time"] += int(trip["Trip  Duration"])
            saved_trip["quantity"] += 1
        else:
            trips_map[key] = {
                "time": int(trip["Trip  Duration"]),
                "quantity": 1,
                "start_id": start_station_id,
                "end_id": end_station_id
            }
        return 1
    return 0

def createTripsGraph(catalog):
    for trip in catalog["trips_map"].values():
        addToTripsGraph(catalog["trips_graph"], trip)

def addToTripsGraph(trips, trip):
    start_id = trip["start_id"]
    end_id = trip["end_id"]
    if not graph.containsVertex(trips, start_id):
        graph.insertVertex(trips, start_id)
    if not graph.containsVertex(trips, end_id):
        graph.insertVertex(trips, end_id)
    average_time = trip["time"]/trip["quantity"]
    graph.addEdge(trips, start_id, end_id, average_time)
    
def getFirstVertex(vertex_map, n):
    items = list(vertex_map.values())[:n]
    first = []
    for vertex in items:
        first.append([vertex["id"], vertex["name"], vertex["from_count"], vertex["to_count"]])
    return first

def getLastVertex(vertex_map, n):
    items = list(vertex_map.values())[-n:]
    last = []
    for vertex in items:
        last.append([vertex["id"], vertex["name"], vertex["from_count"], vertex["to_count"]])
    return last

def addToStationsMap(stations_map, trip):
# las 5 estaciones solicitadas con la siguiente información:
# o Identificador de la estación.
# o Nombre de la estación.
# o Cantidad de viajes que han iniciado en esa estación.
# o El total de viajes iniciados por tipo de usuario (casual y por suscripción.
# o La fecha (formato “MM/DD/AAAA”) del año en la que mas viajes se inician.
# o la hora del día (0:00 – 0:59, 1:00 – 1:59 am, 2:00 – 2:59, …, 23:00 – 23:59) en la que
# más viajes se inician.
    if not trip["Start Station Id"] == "" and not trip["End Station Id"] == "":
        start_station_id = int(float(trip["Start Station Id"]))
        end_station_id = int(float(trip["End Station Id"]))
        time = getTime(trip["Start Time"], trip["End Time"])

        start_station_id = int(float(trip["Start Station Id"]))
        end_station_id = int(float(trip["End Station Id"]))
        station = {}
        annual = 0
        casual = 0
        unknown = 0
        if trip["User Type"] == "Annual Member":
            annual = 1
        elif trip["User Type"] == "Casual Member":
            casual = 1
        else:
            unknown = 1
    
        date = stringToDate(trip["Start Time"])
        hour = stringToHour(trip["Start Time"])
        if start_station_id in stations_map:
            stations_map[start_station_id]["from_count"] += 1
            stations_map[start_station_id]["annuals"] += annual
            stations_map[start_station_id]["casuals"] += casual
            stations_map[start_station_id]["unknowns"] += unknown
            stations_map[start_station_id]["time"]["acum_time"] += time
            stations_map[start_station_id]["time"]["quantity"] += 1
        else:
            station = { 
                "id": start_station_id,
                "name": trip["Start Station Name"], 
                "from_count": 1, 
                "to_count": 0,
                "annuals": annual,
                "casuals": casual,
                "unknowns": unknown,
                "dates": {},
                "hours": {},
                "time": { "acum_time": time, "quantity": 1 }
                }
            stations_map[start_station_id] = station

        if end_station_id in stations_map:
            stations_map[end_station_id]["to_count"] += 1
        else:
            station = { 
                "id": end_station_id,
                "name": trip["End Station Name"], 
                "from_count": 0, 
                "to_count": 1,
                "annuals": 0,
                "casuals": 0,
                "unknowns": 0,
                "dates": {},
                "hours": {},
                "time": { "acum_time": timedelta(), "quantity": 0 }
            }
            stations_map[end_station_id] = station

        if date in stations_map[start_station_id]["dates"]:
            stations_map[start_station_id]["dates"][date] += 1
        else:
            stations_map[start_station_id]["dates"][date] = 1
        
        if hour in stations_map[start_station_id]["hours"]:
            stations_map[start_station_id]["hours"][hour] += 1
        else:
            stations_map[start_station_id]["hours"][hour] = 1

def addToStationsMap(stations_map, trip):
# las 5 estaciones solicitadas con la siguiente información:
# o Identificador de la estación.
# o Nombre de la estación.
# o Cantidad de viajes que han iniciado en esa estación.
# o El total de viajes iniciados por tipo de usuario (casual y por suscripción.
# o La fecha (formato “MM/DD/AAAA”) del año en la que mas viajes se inician.
# o la hora del día (0:00 – 0:59, 1:00 – 1:59 am, 2:00 – 2:59, …, 23:00 – 23:59) en la que
# más viajes se inician.
    if not trip["Start Station Id"] == "" and not trip["End Station Id"] == "":
        start_station_id = int(float(trip["Start Station Id"]))
        end_station_id = int(float(trip["End Station Id"]))
        time = getTime(trip["Start Time"], trip["End Time"])

        start_station_id = int(float(trip["Start Station Id"]))
        end_station_id = int(float(trip["End Station Id"]))
        station = {}
        annual = 0
        casual = 0
        unknown = 0
        if trip["User Type"] == "Annual Member":
            annual = 1
        elif trip["User Type"] == "Casual Member":
            casual = 1
        else:
            unknown = 1
    
        date = stringToDate(trip["Start Time"])
        hour = stringToHour(trip["Start Time"])
        if start_station_id in stations_map:
            stations_map[start_station_id]["from_count"] += 1
            stations_map[start_station_id]["annuals"] += annual
            stations_map[start_station_id]["casuals"] += casual
            stations_map[start_station_id]["unknowns"] += unknown
            stations_map[start_station_id]["time"]["acum_time"] += time
            stations_map[start_station_id]["time"]["quantity"] += 1
        else:
            if trip["Start Station Name"] == "":
                name = "Unknown Satation"
            else:
                name = trip["Start Station Name"]
            station = { 
                "id": start_station_id,
                "name": name, 
                "from_count": 1, 
                "to_count": 0,
                "annuals": annual,
                "casuals": casual,
                "unknowns": unknown,
                "dates": {},
                "hours": {},
                "time": { "acum_time": time, "quantity": 1 }
                }
            stations_map[start_station_id] = station

        if end_station_id in stations_map:
            stations_map[end_station_id]["to_count"] += 1
        else:
            if trip["End Station Name"] == "":
                name = "Unknown Satation"
            else:
                name = trip["End Station Name"]
            station = { 
                "id": end_station_id,
                "name": name, 
                "from_count": 0, 
                "to_count": 1,
                "annuals": 0,
                "casuals": 0,
                "unknowns": 0,
                "dates": {},
                "hours": {},
                "time": { "acum_time": timedelta(), "quantity": 0 }
            }
            stations_map[end_station_id] = station

        if date in stations_map[start_station_id]["dates"]:
            stations_map[start_station_id]["dates"][date] += 1
        else:
            stations_map[start_station_id]["dates"][date] = 1
        
        if hour in stations_map[start_station_id]["hours"]:
            stations_map[start_station_id]["hours"][hour] += 1
        else:
            stations_map[start_station_id]["hours"][hour] = 1

def getMostStartStations(catalog):
    return lt.subList(catalog["outdegree_ordered_graph"], 1, 5)

def orderByOutDegree(vertex):
    return mg.sort(vertex, compareByOutDegree)

def compareByOutDegree(vertex1, vertex2):
    return vertex1["outdegree"] > vertex2["outdegree"]

def orderByStartDate(trips):
    return mg.sort(trips, compareByStartDate)

def compareByStartDate(trip1, trip2):
    return stringToDateTime(trip1["Start Time"]) < stringToDateTime(trip2["Start Time"])

def createOutDegreeOrderedGraph(catalog):
    vertexes = graph.vertices(catalog["trips_graph"])
    for n in range(0, lt.size(vertexes)):
        id = lt.getElement(vertexes, n)
        vertex = { 
            "id": id, 
            "outdegree": graph.outdegree(catalog["trips_graph"], id),
            "indegree" : graph.indegree(catalog["trips_graph"], id)
            }
        lt.addLast(catalog["outdegree_ordered_graph"], vertex )
    catalog["outdegree_ordered_graph"] = mg.sort(catalog["outdegree_ordered_graph"], compareByOutDegree)
        
def findRoutes(catalog, start_station, available_time, min_stations, max_routes):
    trips_graph = catalog["trips_graph"]
    routes = []
    if graph.containsVertex(trips_graph, start_station):
        adjacent_edges = graph.adjacentEdges(trips_graph, start_station)
        edge = adjacent_edges["first"]
        while (edge != None):
            stations = [{ "id": start_station, "time": 0 }]
            edge_time = edge["info"]["weight"]
            if edge_time < available_time:
                stations.append({ "id": edge["info"]["vertexB"], "time": edge_time })
                route = getNextStation(trips_graph, stations, available_time - edge_time)
                if len(route) >= min_stations:
                    routes.append(route)
                    if len(routes) >= max_routes:
                        break
            edge = edge["next"]
    
    return routes

def getNextStation(trips_graph, stations, time):
    adjacent_edges = graph.adjacentEdges(trips_graph, stations[-1]["id"])
    edge = adjacent_edges["first"]
    while (edge["next"] != None):
        edge_time = edge["info"]["weight"]
        if edge_time < time:
            stations.append({ "id": edge["info"]["vertexB"], "time": edge_time })
            return getNextStation(trips_graph, stations, time - edge_time)
        edge = edge["next"]
    return stations

def annualUserReport(catalog, start_date, end_date):
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    trips = catalog["trips"]
    date_ordered_trips = catalog["start_date_ordered_trips"]
    routes = {
        "total_trips": 0,
        "total_time": 0,
        "start_stations": {},
        "end_stations": {},
        "start_hours": {},
        "end_hours": {}
    }
    for trip in date_ordered_trips["elements"]:
        if trip["User Type"] == "Annual Member":
            if stringToDateTime(trip["Start Time"]) >= start_date:
                if stringToDateTime(trip["Start Time"]) > end_date:
                    break
                else:
                    routes["total_trips"] += 1
                    routes["total_time"] += int(trip["Trip  Duration"])
                    start_station_id = int(trip["Start Station Id"])
                    if start_station_id in routes["start_stations"]:
                        routes["start_stations"][start_station_id] += 1
                    else:
                        routes["start_stations"][start_station_id] = 1

                    end_station_id = int(float(trip["End Station Id"]))
                    if end_station_id in routes["end_stations"]:
                        routes["end_stations"][end_station_id] += 1
                    else:
                        routes["end_stations"][end_station_id] = 1

                    hour = stringToHour(trip["Start Time"])
                    if hour in routes["start_hours"]:
                        routes["start_hours"][hour] += 1
                    else:
                        routes["start_hours"][hour] = 1

                    hour = stringToHour(trip["End Time"])
                    if hour in routes["end_hours"]:
                        routes["end_hours"][hour] += 1
                    else:
                        routes["end_hours"][hour] = 1

    return routes

def bikeUsage(catalog, bike_id):
    trips = catalog["trips"]
    usage = {
        "total_trips": 0,
        "total_time": 0,
        "start_stations": {},
        "end_stations": {}
    }
    for trip in trips["elements"]:
        if trip["Bike Id"] != "":
            if int(float(trip["Bike Id"])) == bike_id:
                usage["total_trips"] += 1
                usage["total_time"] += int(trip["Trip  Duration"])
                start_station_id = int(trip["Start Station Id"])
                if start_station_id in usage["start_stations"]:
                    usage["start_stations"][start_station_id] += 1
                else:
                    usage["start_stations"][start_station_id] = 1

                end_station_id = int(float(trip["End Station Id"]))
                if end_station_id in usage["end_stations"]:
                    usage["end_stations"][end_station_id] += 1
                else:
                    usage["end_stations"][end_station_id] = 1
    return usage

def mostFrequentStation(catalog, station_id, start_date, end_date):
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    trips = catalog["trips"]
    date_ordered_trips = catalog["start_date_ordered_trips"]
    routes = {
        "total_trips_start": 0,
        "total_trips_end": 0,
        "trips": [],
        "end_stations": {}
    }
    for trip in date_ordered_trips["elements"]:
        if trip["User Type"] == "Casual Member":
            if stringToDateTime(trip["Start Time"]) >= start_date:
                if stringToDateTime(trip["Start Time"]) > end_date:
                    break
                else:
                    start_station_id = int(trip["Start Station Id"])
                    end_station_id = int(float(trip["End Station Id"]))
                    if start_station_id == station_id:
                        key = createKey(start_station_id, end_station_id)
                        if key not in routes["trips"]:
                            routes["trips"].append(key)
                        routes["total_trips_start"] += 1
                        if end_station_id in routes["end_stations"]:
                            routes["end_stations"][end_station_id] += 1
                        else:
                            routes["end_stations"][end_station_id] = 1
                    elif end_station_id == station_id:
                        routes["total_trips_end"] += 1
    return(routes)

def getMaxTime(catalog, stations):
    max_time = 0
    max_station = None
    for station in stations:
       vertexes = station.split(",")
       edge = graph.getEdge(catalog["trips_graph"], int(vertexes[0]), int(vertexes[1]))
       if edge["weight"] > max_time:
           max_time = edge["weight"]
           max_station = int(vertexes[1])
    return { "station_id": max_station, "quantity": max_time }

def strongLinked(catalog):
    search = scc.KosarajuSCC(catalog["trips_graph"])
    components = {}
    for station in search["idscc"]["table"]["elements"]:
        if station["value"] != None:
            if station["value"] in components:
                if station["key"] not in components[station["value"]]:
                    components[station["value"]].append(station["key"])
            else:
                components[station["value"]] = [station["key"]]
    
    return components

def fastestRoute(trips_graph, start_station_id, end_station_id):
    search = dijsktra.Dijkstra(trips_graph, start_station_id)
    edges = dijsktra.pathTo(search, end_station_id)
    stations = []
    edge = edges["first"]
    while (edge != None):
        stations.append({ 
            "start_station_id": edge["info"]["vertexA"],
            "end_station_id": edge["info"]["vertexB"],
            "time": edge["info"]["weight"] 
        })
        edge = edge["next"]
    return stations[::-1]
