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
from DISClib.ADT import list as lt
from App import model
import csv



# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Cargar, limpiar y información
# ___________________________________________________


def loadAndCleanData(analyzer, file):
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    k=0
    for trip in input_file:
        k+=1
        model.loadAndCleanData(analyzer,trip)
    return analyzer,k




# ___________________________________________________
#  Funciones de consulta
# ___________________________________________________

def totalTrips(analyzer):
    return model.totalTrips(analyzer)

def totalConnections(analyzer):
    return model.totalConnections(analyzer)

def totalStations(analyzer):
    return model.totalStations(analyzer)

def getVertices(analyzer):
    return model.getVertices(analyzer)

def firstAndLast5(lista):
    return model.firstAndLast5(lista)

def getInfoVert(analyzer,vertices):
    return model.getInfoVert(analyzer,vertices)




#####################################################################


# _____________________________________________________
#  REQUERIMIENTO 1: ESTACIONES CON MÁS VIAJES DE SALIDA
# _____________________________________________________

def orderVerticesByEdgeOuts(analyzer):
    return model.orderVerticesByEdgeOuts(analyzer)


# _____________________________________________________
#  REQUERIMIENTO 2: PLANEAR PASEOS TURÍSTICOS
# _____________________________________________________


def getVertFromNameStation(analyzer,initialStationName):
    return model.getVertFromNameStation(analyzer,initialStationName)

def searchPaths(analyzer, initialStationId):
    return model.searchPaths(analyzer, initialStationId)

def filterPathsByTimeAndNumStations(analyzer, maxTime, minStations):
    return model.filterPathsByTimeAndNumStations(analyzer, maxTime, minStations)

def preparElementsForPrint(analyzer,paths,numAnswers):
    return model.preparElementsForPrint(analyzer,paths,numAnswers)


# _____________________________________________________
#  REQUERIMIENTO 3: COMPONENTES FUERTEMENTE CONECTADOS
# _____________________________________________________

def searchComponents(analyzer):
    return model.searchComponents(analyzer)

def getNumComponents(analyzer):
    return model.getNumComponents(analyzer)

def getComponents(analyzer):
    return model.getComponents(analyzer)

def preparComponentsForPrint(analyzer,components):
    return model.preparComponentsForPrint(analyzer,components)

# ________________________________________________________
#  REQUERIMIENTO 4: RUTA RÁPIDA
# _________________________________________________________

def minimumCostPaths(analyzer,startStation):
    return model.minimumCostPaths(analyzer,startStation)

def getMinimumPath(analyzer,endStation):
    return model.getMinimumPath(analyzer,endStation)

def getTimeAndInfoPath(analyzer,path):
    return model.getTimeAndInfoPath(analyzer,path)


# ________________________________________________________
#  REQUERIMIENTO 5: RUTAS EN UN RANGO DE FECHAS
# _________________________________________________________

def getTripsByDate(analyzer,startDate,endDate):
    return model.getTripsByDate(analyzer,startDate,endDate)

def getFrequentStations(trips):
    return model.getFrequentStations(trips)

def getFrequentHours(trips):
    return model.getFrequentHours(trips)

# ___________________________________________________________
#  REQUERIMIENTO 6: INFORMACIÓN DE BICICLETA
# ___________________________________________________________

def getTripsByBikeId(analyzer,bikeId):
    return model.getTripsByBikeId(analyzer,bikeId)

