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
import datetime
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def analizerStart():
    return model.analizerStart()

def loadData(analizer):
    tagsfile = cf.data_dir + 'Bikeshare/Bikeshare-ridership-2021-utf8-small.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))

    for trip in input_file:
        if trip['Start Station Id']!='' and trip['End Station Id']!='' and trip['Trip  Duration']!='' and trip['Bike Id']!='':
            date_timeA=datetime.datetime.strptime(trip['Start Time'][11:],"%H:%M")
            date_timeB=datetime.datetime.strptime(trip['End Time'][11:],"%H:%M")
            I_timedelta = date_timeA - datetime.datetime(1900, 1, 1)
            F_timedelta = date_timeB - datetime.datetime(1900, 1, 1)
            secondsI = I_timedelta.total_seconds()
            secondsf = F_timedelta.total_seconds()
            totalSeconds=int(float(secondsf-secondsI))  
            model.vertexDict(analizer, int(trip['Start Station Id']),trip['Start Station Name'])
            model.vertexDict(analizer, int(float(trip['End Station Id'])),trip['End Station Name'])
            model.edgesDict(analizer, int(trip['Start Station Id']),trip['Start Station Name'],int(float(trip['End Station Id'])),trip['End Station Name'], totalSeconds)
            model.contadorEstaciones(analizer, trip['Start Station Name'],int(trip['Start Station Id']) )
            model.tripList(analizer, trip)

        
def createGraph(analizer):
    return model.createGraph(analizer)

def createGraphNodir(analizer):
    return model.createGraphNoDir(analizer)

def repuestaReq1(analizer):
    return model.respuestaReq1(analizer)

def shortestPath(analizer, vertex, numEstaciones, duration, num):
    return model.shortestPath(analizer, vertex, numEstaciones, duration, num)

def stronlgyConected(analizer):
   return model.stronglyConcetedC(analizer)

def requerimiento4(analizer, verticeI, verticeF):
    return model.requerimiento4(analizer, verticeI, verticeF)
def bikeNum(analizer, bikeId):
    return model.bikeNum(analizer, bikeId)
