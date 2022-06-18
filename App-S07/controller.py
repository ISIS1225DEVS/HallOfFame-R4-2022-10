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
import csv
from DISClib.ADT import graph as graph
from tabulate import tabulate

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


def newController():
    return model.newCatalog()

def loadData(catalog, file_size):
    trips_file = cf.data_dir + "Bikeshare-ridership-2021-utf8-" + file_size + ".csv"
    input_file = csv.DictReader(open(trips_file, encoding='utf-8'))
    total_trips = 0
    for trip in input_file:
        model.addToStationsMap(catalog["stations_map"], trip)
        model.addTrip(catalog["trips"], trip)
        total_trips += model.addToTripsMap(catalog["trips_map"], trip)

    catalog["start_date_ordered_trips"] = model.orderByStartDate(catalog["trips"])
    model.createTripsGraph(catalog)
    model.createOutDegreeOrderedGraph(catalog)

    print("Total viajes: ", total_trips)
    print("Total vertices", graph.numVertices(catalog["trips_graph"]))
    print("Total arcos: ", graph.numEdges(catalog["trips_graph"]))
    print("Primeros 5")
    print(tabulate(model.getFirstVertex(catalog["stations_map"], 5), headers=["id", "name", "from_count", "to_count"], tablefmt="grid"))
    print("Ultimos 5")
    print(tabulate(model.getLastVertex(catalog["stations_map"], 5), headers=["id", "name", "from_count", "to_count"], tablefmt="grid"))

def getMostStartStations(catalog):
    return model.getMostStartStations(catalog)


def findRoutes(catalog, start_station, available_time, min_stations, max_routes):
    station_id = getStationIdFromName(catalog["stations_map"], start_station)
    if station_id != None:
        return model.findRoutes(catalog, station_id, available_time, min_stations, max_routes)
    return None


def annualUserReport(catalog, start_date, end_date):
    routes = model.annualUserReport(catalog, start_date, end_date)
    return { 
        "total_trips": routes["total_trips"], 
        "total_time": routes["total_time"],
        "start_station": getMax(routes["start_stations"]),
        "end_station": getMax(routes["end_stations"]),
        "start_hour": getMax(routes["start_hours"]),
        "end_hour": getMax(routes["end_hours"])
        }

def bikeUsage(catalog, bike_id):
    usage = model.bikeUsage(catalog, int(float(bike_id)))
    return {
        "total_trips": usage["total_trips"], 
        "total_time": usage["total_time"],
        "start_station": getMax(usage["start_stations"]),
        "end_station": getMax(usage["end_stations"])
    }

def mostFrequentStation(catalog, station, start_date, end_date):
    station_id = getStationIdFromName(catalog["stations_map"], station)
    if station_id != None:
        stations =  model.mostFrequentStation(catalog, station_id, start_date, end_date)
    
    return {
        "total_trips_start": stations["total_trips_start"],
        "total_trips_end": stations["total_trips_end"],
        "max_average_time": model.getMaxTime(catalog, stations["trips"]),
        "end_stations": getMax(stations["end_stations"])
    }


def getMax(array):
    max = 0
    pointer = None
    for k, v in array.items():
        if v > max:
            max = v
            pointer = k
    return { "key": pointer, "value": max }


def strongLinked(catalog):
    return model.strongLinked(catalog)

def fastestRoute(catalog, start_station, end_station):
    start_station_id = getStationIdFromName(catalog["stations_map"], start_station)
    end_station_id = getStationIdFromName(catalog["stations_map"], end_station)
    if start_station_id != None and end_station_id != None:
        return model.fastestRoute(catalog["trips_graph"], start_station_id, end_station_id)
    return None

def getStationIdFromName(stations_map, name):
    for station_id, value in stations_map.items():
        if value["name"] == name:
            return station_id
    return None

def getFastestRouteSequence(catalog, route):
    sequence = []
    for edge in route:
        sequence.append([str(edge["start_station_id"]), catalog["stations_map"][edge["start_station_id"]]["name"], str(edge["time"])])
    sequence.append([str(route[-1]["end_station_id"]), catalog["stations_map"][route[-1]["end_station_id"]]["name"], "0"])
    return sequence

def getTotalTimeFastestRoute(route):
    time = 0
    for edge in route:
        time += edge["time"]
    return time

def getRouteSequence(catalog, route):
    sequence = []
    for station in route:
        sequence.append(str(station["id"]) + "-" + catalog["stations_map"][station["id"]]["name"])
    return ", ".join(sequence)

def getRouteTime(route):
    time = 0
    for station in route:
        time += station["time"]
    return time

def componentData(catalog, components):
    output = []
    for component in components.values():
        data = getMostStartsAndEnds(catalog, component)
        output.append([
            len(component),
            data["start_id"], 
            data["start_name"],
            data["end_id"],
            data["end_name"]
        ])
    return output

def getMostStartsAndEnds(catalog, component):
    max_starts = 0
    max_starts_id = None
    max_ends = 0
    max_ends_id = None

    for station_id in component:
        station = catalog["stations_map"][station_id]
        if station["from_count"] >= max_starts:
            max_starts = station["from_count"]
            max_starts_id = station["id"]
        if station["to_count"] >= max_ends:
            max_ends = station["to_count"]
            max_ends_id = station["id"]

    return {
        "start_id": max_starts_id,
        "start_name": catalog["stations_map"][max_starts_id]["name"],
        "end_id": max_ends_id,
        "end_name": catalog["stations_map"][max_ends_id]["name"]
    }


