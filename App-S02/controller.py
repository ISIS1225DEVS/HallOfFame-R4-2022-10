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
from math import gcd
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog

def loadTrips(catalog, tripsfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    tripsfile = cf.data_dir + tripsfile
    inputfile = csv.DictReader(open(tripsfile, encoding="utf-8"),
                                delimiter=",")

    for trip in inputfile:
        duration = int(float(trip["Trip  Duration"]))
        if bool1(trip) and bool2(trip) and bool3(trip) and bool4(duration) and bool5(trip):
            model.addTripList(catalog, trip)
    totaltrips, dfD, dfND, vertexND, edgesND = model.loadData(catalog)
    return totaltrips, dfD, dfND, vertexND, edgesND

def bool1(trip):
    if trip["End Station Id"] != "":
        return True
    else:
        return False

def bool2(trip):
    if trip["Start Station Id"] != "":
        return True
    else:
        return False

def bool3(trip):
    if trip["Bike Id"] != "":
        return True
    else:
        return False

def bool4(duration):
    if duration > 0:
        return True
    else:
        return False

def bool5(trip):
    if trip["Start Station Name"] != trip["End Station Name"]:
        return True
    else:
        return False


# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalStops(catalog):
    """
    Total de paradas de autobus
    """
    return model.totalStops(catalog)


def totalConnections(catalog):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(catalog)

def popularStations(catalog):
    return model.popularStations(catalog)


def planTrips(catalog, name, available, min, max):
    return model.planTrips(catalog, name, available, min, max)


def stronglyConnected(catalog):
    return model.stronglyConnected(catalog)


def fastRoute(catalog, origen, destino):
    return model.fastRoute(catalog, origen, destino)
    

def routesInDateRange(catalog, min, max):
    return model.routesInDateRange(catalog, min, max)


def infoStation(catalog, station, startdate, starthour, enddate, endhour):
    return model.infoStation(catalog, station, startdate, starthour, enddate, endhour)


def bikerMaintenance(catalog,bikerId):
    return model.bikerMaintenance(catalog,bikerId)