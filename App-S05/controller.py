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
import time
import tracemalloc
from DISClib.ADT import list as lt

size = "50pct"

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadServices(analyzer):
    
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    servicesfile = cf.data_dir + "Bikeshare-ridership-2021-utf8-{0}.csv".format(size)
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"), delimiter=",")

    Total_trips = 0

    for service in input_file:
        
        model.should_analyze(service, analyzer)
        Total_trips += 1
        
        
    
    model.create_out_trip_tree(analyzer)
    model.create_graph(analyzer)
    model.do_the_kosaraju(analyzer)

    
    model.Create_R3(analyzer)
    
        
    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()


    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)


    return time, memory, Total_trips
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def callR1(analyzer):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    top_5_list = model.R1_answer(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    return time, memory, top_5_list


def callR2(analyzer, v_start, limite_estaciones, limite_tiempo, limite_estaciones_maximo):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    FittingPaths = model.R2_answer(analyzer, v_start, limite_estaciones, limite_tiempo, limite_estaciones_maximo)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)

    return time, memory, FittingPaths

def callR3(analyzer):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    answer = model.R3_answer(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    return time, memory, answer

def callR4(analyzer,origen, destination):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    distance, camino = model.R4_answer(analyzer,origen, destination)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    return time, memory, distance, camino 


def callR5(analyzer, fecha_inicial, fecha_final):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    tupla_completa = model.R5_answer(analyzer, fecha_inicial, fecha_final)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    return time, memory, tupla_completa

def callR6(analyzer, bike_inp):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    num_viajes, timpo_rec, vert_max_out, vert_max_in = model.R6_answer(analyzer, bike_inp)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory) 

    return time, memory, num_viajes, timpo_rec, vert_max_out, vert_max_in

def callR7(analyzer,vert_inp, fecha_inicial, fecha_final):
    tracemalloc.start()

    start_time = getTime()
    start_memory = getMemory()

    in_trips, out_trips, most_trips_ended = model.R7_answer(analyzer,vert_inp, fecha_inicial, fecha_final)

    stop_memory = getMemory()
    stop_time = getTime()
  
    tracemalloc.stop()

    time = deltaTime(stop_time, start_time)
    memory = deltaMemory(stop_memory, start_memory)
    
    return time, memory, in_trips, out_trips, most_trips_ended 


# ___________________________________________________
# TIEMPO
# ___________________________________________________

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




# ___________________________________________________
# MEMORIA
# ___________________________________________________
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