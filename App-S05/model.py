"""
 * Copyright 20artamento de sistemas y Computación,
 * Universidad 
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


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import indexminpq as inpq
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
  
from datetime import datetime as dt
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.ADT import stack

assert cf

our_prime = 12345678910987654321
our_loadfactor = 0.5

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'search': None,
            'graph': None,
            'SCC': None,
            'paths': None,
            
            #graph
            "name_to_vertice":None,
            "vertices_list" : None,
            "edge_map": None,

            #Req 1
            "in_n_out_trips_hash":None,
            "in_n_out_trips_tree":None,
            "vert_rush_hour":None,
            "vert_rush_day":None,
            "member_vert":None,

            #Req 2
            "dijkstraN2": None,


            #Req 3
            "kosaraju":None,
            "R3_answer": None, 

            #Req 4
            "dijsktra":None,

            #Req 5
            "Arbol_fechas_usuarios_anuales": None,
            "viajes_InOut_por_vertice": None,
            'viajes_por_hora_anuales': None, 

            #req 6 

            "bikes_info": None,
            "bike_out_pq": None, 
            "bike_in_pq": None,

            #Req 7
            "date_tree_2": None,
            "in_n_out_trips_hash2" :None,
            "R7_vert_pq": None

            }


        analyzer["name_to_vertice"] =  mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)

        analyzer["vertices_list"] = lt.newList("ARRAY_LIST")

        analyzer["edge_map"] = mp.newMap(numelements= 100000,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)

        analyzer["in_n_out_trips_hash"] = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
                                                 
        analyzer["in_n_out_trips_tree"] = om.newMap(omaptype='RBT',
                                                    comparefunction=compare_r1)

        analyzer["graph"] = gr.newGraph(datastructure= "ADJ_LIST", 
                                        directed=True, 
                                        size = 770, 
                                        comparefunction=compare_gr)

        analyzer["vert_rush_hour"] = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
                                                 
        analyzer["vert_rush_day"] = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
                        
        analyzer["member_vert"] = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
        #Req5                                                                                  
        analyzer["Arbol_fechas_usuarios_anuales"] = om.newMap(omaptype='RBT',
                                                    comparefunction=compare_r1)
        
        analyzer['viajes_InOut_por_vertice'] = mp.newMap(numelements=770,
                                                 maptype= 'PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)

        analyzer['viajes_por_hora_anuales'] = mp.newMap(numelements= 24,
                                                 maptype= 'PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
        #Req6
        analyzer["bikes_info"] = mp.newMap(numelements= 10000,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
                                            
        analyzer["bike_out_pq"] = mp.newMap(numelements= 10000,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
        
        analyzer["bike_in_pq"] = mp.newMap(numelements= 10000,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)

        #Req 7
        analyzer["date_tree_2"] = om.newMap(omaptype='RBT',
                                            comparefunction=compare_r1)


        
        
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo
def compare_gr(stop, keyvaluestop):
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

def should_analyze(service, analyzer):
    if service["Start Station Id"] == "" or service["End Station Id"] == "" or service['Trip  Duration'] == "" or service["Bike Id"] == "":
        pass   
    else:

        if float(service["Start Station Id"]) == float(service["End Station Id"]):
            pass
        else:

            if float(service['Trip  Duration']) <= 0:
                pass
            else:
                load_service(analyzer, service)


    

def load_service(analyzer, service):
    service["Trip  Duration"] = float(service["Trip  Duration"])
    service["Start Station Id"]=int(float(service["Start Station Id"]))
    service["End Station Id"]=int(float(service["End Station Id"]))

    ver1, ver2 = addTo_name_to_vertice(analyzer, service)
    addTo_edge_map(analyzer, service, ver1, ver2)
    addTo_in_n_out_trips_hash(analyzer, ver1, ver2)
    
    update_minpq_hour (analyzer,service,ver1,ver2)
    update_minpq_day (analyzer,service,ver1,ver2)
    update_member_vert(analyzer, service, ver1, ver2)

    if service['User Type'] == 'Annual Member':
        carga_R5(analyzer, service)
    else:
        carga_R7(analyzer, service)

    bikes_info(analyzer, service, ver1, ver2)

def carga_R5(analyzer, service):
    RBT_fechas = analyzer['Arbol_fechas_usuarios_anuales']
    fecha = service['Start Time'][:-6]
    
    #Revisar si está, si no, agregar una lt como valor
    exist_fecha = om.get(RBT_fechas, fecha)
    if exist_fecha is None:
        lista_fecha = lt.newList('ARRAY_LIST')
        om.put(RBT_fechas, fecha, lista_fecha)
        exist_fecha = om.get(RBT_fechas, fecha)

    #Agregar el servicio a la lista
    lista_fecha = exist_fecha['value']
    lt.addLast(lista_fecha, service)
    

def update_member_vert(analyzer, service, ver1, ver2):
    map_members = analyzer["member_vert"]
    casual1, annual1 = mp.get(map_members,ver1)["value"]

    
    if service["User Type"] == "Casual Member":
        casual1 += 1
    
    if service["User Type"] == "Annual Member":
        annual1 += 1
    
    mp.put(map_members,ver1,(casual1, annual1))
    

def update_minpq_hour (analyzer,service,ver1,ver2):
    minpq_map = analyzer["vert_rush_hour"]
    time1 = hour_determiner(service["Start Time"])
    minpq1 = mp.get(minpq_map, ver1)["value"]
    if not inpq.contains(minpq1, time1):
        inpq.insert(minpq1,time1,0)
    
    inpq.increaseKey2(minpq1,time1)


def update_minpq_day (analyzer,service,ver1,ver2):
    minpq_map = analyzer["vert_rush_day"]
    time1 = day_determiner(service["Start Time"])
    minpq1 = mp.get(minpq_map, ver1)["value"]
    if not inpq.contains(minpq1, time1):
        inpq.insert(minpq1,time1,0)
    
    inpq.increaseKey2(minpq1,time1)

def day_determiner(time):
    day = time[:10]
    return day

def hour_determiner(time):
    dic_horas={
        "00":"0:00-0:59",
        "01":"1:00-1:59",
        "02":"2:00-2:59",
        "03":"3:00-3:59",
        "04":"4:00-4:59",
        "05":"5:00-5:59",
        "06":"6:00-6:59",
        "07":"7:00-7:59",
        "08":"8:00-8:59",
        "09":"9:00-9:59",
        "10":"10:00-10:59",
        "11":"11:00-11:59",
        "12":"12:00-12:59",
        "13":"13:00-13:59",
        "14":"14:00-14:59",
        "15":"15:00-15:59",
        "16":"16:00-16:59",
        "17":"17:00-17:59",
        "18":"18:00-18:59",
        "19":"19:00-19:59",
        "20":"20:00-20:59",
        "21":"21:00-21:59",
        "22":"22:00-22:59",
        "23":"23:00-23:59"}
    list = time[-5:].split(":")

    return dic_horas[list[0]]
    
def minpq_compare(num1, num2):
    num2 = num2["key"]
    if num1 == num2:
        return 0 
    elif num1 < num2:
        return 1
    else:
        return -1


def addTo_name_to_vertice(analzer, service):
    map = analzer["name_to_vertice"]

    start_name = service["Start Station Name"]
    end_name = service["End Station Name"]

    if start_name == "":
        start_name = "Unknown Station"
    
    if end_name == "":
        end_name = "Unknown Station"
    
    start_id = service["Start Station Id"]
    end_id = service["End Station Id"]

    key1 = start_name
    key2 = end_name 
    vertice1 = "{0}-{1}".format(start_id, start_name)
    vertice2 = "{0}-{1}".format(end_id, end_name)


    exist_value1 = mp.get(map, key1)
    if exist_value1 is None:
        vertice_list = lt.newList("ARRAY_LIST")
        mp.put(map, key1, vertice_list)
        exist_value1 = mp.get(map, key1)

    vertices1 = exist_value1["value"]

    is_present = False
    for ver in lt.iterator(vertices1):
        if vertice1 == ver:
            is_present = True
    
    if not is_present:
        lt.addLast(vertices1, vertice1)
        lt.addLast(analzer["vertices_list"],vertice1)
        mp.put(analzer["vert_rush_hour"], vertice1, inpq.newIndexMinPQ(minpq_compare))
        mp.put(analzer["vert_rush_day"], vertice1, inpq.newIndexMinPQ(minpq_compare))
        mp.put(analzer["member_vert"], vertice1, (0,0))
    exist_value2 = mp.get(map, key2)
    if exist_value2 is None:
        vertice_list = lt.newList("ARRAY_LIST")
        mp.put(map, key2, vertice_list)
        exist_value2 = mp.get(map, key2)
    
    vertices2 = exist_value2["value"]
    is_present2 = False
    for ver in lt.iterator(vertices2):
        if vertice2 == ver:
            is_present2 = True
    
    if not is_present2:
        lt.addLast(vertices2, vertice2)
        lt.addLast(analzer["vertices_list"],vertice2)
        mp.put(analzer["vert_rush_hour"], vertice2, inpq.newIndexMinPQ(minpq_compare))
        mp.put(analzer["vert_rush_day"], vertice2, inpq.newIndexMinPQ(minpq_compare))
        mp.put(analzer["member_vert"], vertice2, (0,0))

    return (vertice1, vertice2)

def addTo_edge_map(analyzer, service, ver1, ver2):
    map = analyzer["edge_map"]
    key = (ver1,ver2)
    
    exsist_edge = mp.get(map, key)
    if exsist_edge is None:
        mp.put(map, key, (0,0))
        exsist_edge = mp.get(map, key)
    
    total_time, num_of_trips = exsist_edge["value"]
    total_time += float(service["Trip  Duration"])
    num_of_trips += 1

    mp.put(map, key, (total_time, num_of_trips))


def addTo_in_n_out_trips_hash(analyzer, ver1, ver2):
    map = analyzer["in_n_out_trips_hash"]

    exist_ver1 = mp.get(map, ver1)
    if exist_ver1 is None:
        mp.put(map, ver1, (0,0))
        exist_ver1 = mp.get(map, ver1)

    in_trips1, out_trips1 = exist_ver1["value"]
    out_trips1 += 1

    mp.put(map, ver1,(in_trips1, out_trips1))
    

    exist_ver2 = mp.get(map, ver2)
    if exist_ver2 is None:
        mp.put(map, ver2, (0,0))
        exist_ver2 = mp.get(map, ver2)

    in_trips2, out_trips2 = exist_ver2["value"]
    in_trips2 += 1

    mp.put(map, ver2,(in_trips2, out_trips2)) 


def create_graph(analyzer):
    graph = analyzer["graph"]
    vert_list = analyzer["vertices_list"]
    edges_list = mp.keySet(analyzer["edge_map"]) 

    for vert in lt.iterator(vert_list):
        gr.insertVertex(graph, vert)
    
    for edge in lt.iterator(edges_list):
        start_v , end_v = edge
        sum, count = mp.get(analyzer["edge_map"], edge)["value"]
        weigth = round(sum / count, 2) 

        gr.addEdge(graph, start_v, end_v, weigth)

def do_the_kosaraju(analyzer):
    analyzer["kosaraju"] = scc.KosarajuSCC(analyzer["graph"])

# ___________________________________________________
# Requerimiento 1
# ___________________________________________________
def create_out_trip_tree(analyzer):
    vert_list = mp.keySet(analyzer["in_n_out_trips_hash"])
    for vert in lt.iterator(vert_list):
        in_trips, out_trips = mp.get(analyzer["in_n_out_trips_hash"],vert)["value"]

        exist_out = om.get(analyzer["in_n_out_trips_tree"], out_trips)
        if exist_out is None:
            new_lt = lt.newList("ARRAY_LIST")
            om.put(analyzer["in_n_out_trips_tree"], out_trips, new_lt)
            exist_out = om.get(analyzer["in_n_out_trips_tree"], out_trips)
        
        out_trips_vert_list = exist_out["value"]
        lt.addLast(out_trips_vert_list, vert)

def compare_r1(num1, num2):
    if num1 == num2:
        return 0 
    elif num1 > num2:
        return 1
    else:
        return -1

def bikes_info(analyzer, service, ver1, ver2):
    bike_id = service["Bike Id"].split(".")[0]

    map_bike_info = analyzer["bikes_info"]

    exist_bike = mp.get(map_bike_info, bike_id)

    if exist_bike == None:
        mp.put(map_bike_info, bike_id, (0,0))
        exist_bike = mp.get(map_bike_info, bike_id)

    num_viajes, time = exist_bike["value"]
    
    num_viajes += 1 
    time += float(service["Trip  Duration"]) 

    mp.put(map_bike_info, bike_id, (num_viajes, time))

    bikes_pt2(analyzer, service, bike_id, ver1, ver2)

def bikes_pt2(analyzer, service, bike_id, ver1, ver2):

    exist_bike_out = mp.get(analyzer["bike_out_pq"], bike_id)    

    if exist_bike_out is None: 
        new_heap = inpq.newIndexMinPQ(minpq_compare)
        mp.put(analyzer["bike_out_pq"], bike_id, new_heap)
        exist_bike_out = mp.get(analyzer["bike_out_pq"], bike_id)

    bike_out_heap = exist_bike_out["value"]

    if not inpq.contains(bike_out_heap,ver1):
        inpq.insert(bike_out_heap, ver1,0)
    
    inpq.increaseKey2(bike_out_heap,ver1)


    exist_bike_in = mp.get(analyzer["bike_in_pq"], bike_id)    

    if exist_bike_in is None: 
        new_heap = inpq.newIndexMinPQ(minpq_compare)
        mp.put(analyzer["bike_in_pq"], bike_id, new_heap)
        exist_bike_in = mp.get(analyzer["bike_in_pq"], bike_id)

    bike_in_heap = exist_bike_in["value"]

    if not inpq.contains(bike_in_heap,ver2):
        inpq.insert(bike_in_heap, ver2, 0)
    
    inpq.increaseKey2(bike_in_heap,ver2)


def carga_R7(analyzer, service):
    RBT_fechas = analyzer['date_tree_2']
    fecha = service['Start Time']

    #Revisar si está, si no, agregar una lt como valor
    exist_fecha = om.get(RBT_fechas, fecha)
    if exist_fecha is None:
        lista_fecha = lt.newList('ARRAY_LIST')
        om.put(RBT_fechas, fecha, lista_fecha)
        exist_fecha = om.get(RBT_fechas, fecha)
    #Agregar el servicio a la lista
    lista_fecha = exist_fecha['value']
    lt.addLast(lista_fecha, service)

# Funciones para creacion de datos

# Funciones de consulta
def R1_answer(analyzer):
    top_5_list = lt.newList("ARRAY_LIST") 
    
    while lt.size(top_5_list) < 5:
        max_key = om.maxKey(analyzer["in_n_out_trips_tree"])
        vert_list = om.get(analyzer["in_n_out_trips_tree"], max_key)["value"]
        for vert in lt.iterator(vert_list):
            if lt.size(top_5_list) < 5:
                lt.addLast(top_5_list, (vert,max_key))
        om.deleteMax(analyzer["in_n_out_trips_tree"])
    
    for vert, count  in lt.iterator(top_5_list):
        in_trips, out_trips = mp.get(analyzer["in_n_out_trips_hash"],vert)["value"]

        exist_out = om.get(analyzer["in_n_out_trips_tree"], out_trips)
        if exist_out is None:
            new_lt = lt.newList("ARRAY_LIST")
            mp.put(analyzer["in_n_out_trips_tree"], out_trips, new_lt)
            exist_out = om.get(analyzer["in_n_out_trips_tree"], out_trips)
        
        out_trips_vert_list = exist_out["value"]
        lt.addLast(out_trips_vert_list, vert)

    return top_5_list

def R2_answer(analyzer, v_start, limite_estaciones_min, limite_tiempo, limite_estaciones_maximo):
    
    rsp_list = lt.newList('ARRAY_LIST')
    do_the_dijkstraN2(analyzer, v_start)
    lt_vertices = gr.vertices(analyzer['graph'])
    limite_recorrido = limite_tiempo/2
    

    for vertex in lt.iterator(lt_vertices):
        if dj.hasPathTo(analyzer['dijkstraN2'], vertex):
            tiempo_recorrido = dj.distTo(analyzer["dijkstraN2"], vertex)
            camino = dj.pathTo(analyzer["dijkstraN2"],   vertex)
            if stack.isEmpty(camino):
                continue
            if tiempo_recorrido <= limite_recorrido and stack.size(camino) > limite_estaciones_min and stack.size(camino) <= limite_estaciones_maximo:
                tupla_camino = (camino,stack.size(camino), tiempo_recorrido)
                lt.addLast(rsp_list, tupla_camino)
    
    return rsp_list       


def do_the_dijkstraN2(analyzer, v_start):
    analyzer['dijkstraN2'] = dj.Dijkstra(analyzer['graph'], v_start)


def Create_R3(analyzer):

    num_Stron_Con_Com = scc.connectedComponents(analyzer["kosaraju"])
    
    mapa_SCC = analyzer["kosaraju"]["idscc"]

    mapa_scc_minpq_out = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)
    mapa_scc_minpq_in = mp.newMap(numelements= 770,
                                                 maptype='PROBING',
                                                 loadfactor=our_loadfactor,
                                                 prime=our_prime)

    for vert in lt.iterator(analyzer["vertices_list"]):
        scc_num = mp.get(mapa_SCC, vert)["value"]
        
        exist_heap_scc_out = mp.get(mapa_scc_minpq_out, scc_num)

        if exist_heap_scc_out is None:
            new_heap = inpq.newIndexMinPQ(minpq_compare)
            mp.put(mapa_scc_minpq_out, scc_num, new_heap)
            exist_heap_scc_out = mp.get(mapa_scc_minpq_out, scc_num)
        heap_scc_out = exist_heap_scc_out["value"]

        in_index, out_index = mp.get(analyzer["in_n_out_trips_hash"],vert)["value"]

        inpq.insert(heap_scc_out, vert, -out_index)

        exist_heap_scc_in = mp.get(mapa_scc_minpq_in, scc_num)
        if exist_heap_scc_in is None:
            new_heap = inpq.newIndexMinPQ(minpq_compare)
            mp.put(mapa_scc_minpq_in, scc_num, new_heap)
            exist_heap_scc_in= mp.get(mapa_scc_minpq_in, scc_num)
        
        heap_scc_in = exist_heap_scc_in["value"]

        inpq.insert(heap_scc_in, vert, -in_index)

    resp_list = lt.newList("ARRAY_LIST")
    
    for valor in range(1, num_Stron_Con_Com+1):
        out_pq= mp.get(mapa_scc_minpq_out,valor)["value"]
        max_out = inpq.min(out_pq)
        in_pq= mp.get(mapa_scc_minpq_in,valor)["value"]
        max_in = inpq.min(in_pq)

        lt.addLast(resp_list, (valor, max_out, max_in, inpq.size(out_pq)))
    
    analyzer["R3_answer"] = (num_Stron_Con_Com,  resp_list)

def R3_answer(analyzer):
    return analyzer["R3_answer"]
    

def R4_answer(analyzer,origen, destination):

    do_the_dijsktra(analyzer, origen)

    if dj.hasPathTo(analyzer["dijsktra"],destination):
        distance = dj.distTo(analyzer["dijsktra"],destination)
        camino = dj.pathTo(analyzer["dijsktra"],destination)
        return distance, camino
    else:
        return "No hay camino", None

def do_the_dijsktra(analyzer, origen):
        analyzer["dijsktra"] = dj.Dijkstra(analyzer["graph"], origen)

def R5_answer(analyzer, fecha_inicial, fecha_final):

    RBT_fechas = analyzer['Arbol_fechas_usuarios_anuales']
    # Extraemos las fechas que están en [fecha_inicial, fecha_final]
    lista_fechas_que_cumplen = om.keys(RBT_fechas, fecha_inicial, fecha_final)

    # Ahora inicializamos las variables
    out_total_viajes = 0
    out_total_tiempo = 0

    for fecha in lt.iterator(lista_fechas_que_cumplen):

        lista_de_la_fecha = om.get(RBT_fechas, fecha)['value']
        # Analizar cada servicio en la lista
        for service in lt.iterator(lista_de_la_fecha):

            out_total_viajes += 1
            out_total_tiempo += service['Trip  Duration']
            actualizar_viajes_anuales_InOut(analyzer, service)
            actualizar_viajes_anuales_hora(analyzer, service)

    
    # Fin de la iteración

    # Ahora, vamos a buscar el mayor para: estación de salida, estación de llegada 

    maximo_salida  = 0
    maximo_llegada = 0
    for key in lt.iterator(mp.keySet(analyzer['viajes_InOut_por_vertice'])):
        tupla_in_out = mp.get(analyzer['viajes_InOut_por_vertice'], key)['value']
        
        n_salida = tupla_in_out[1]
        n_llegada = tupla_in_out[0]
        if n_salida > maximo_salida:
            maximo_v_salida = (key, n_salida)
            maximo_salida = n_salida
        if n_llegada > maximo_llegada:
            maximo_v_llegada = (key, n_llegada)
            maximo_llegada = n_llegada


    maximo_salida  = 0
    maximo_llegada = 0
    # Finalmente, calcular la hora en que salen y llegan más viajes
    for key in lt.iterator(mp.keySet(analyzer['viajes_por_hora_anuales'])):
        tupla_in_out_hora = mp.get(analyzer['viajes_por_hora_anuales'], key)['value']
        
        n_salida = tupla_in_out_hora[1]
        n_llegada = tupla_in_out_hora[0]
        if n_salida > maximo_salida:
            maximo_hora_salida = (key, n_salida)
            maximo_salida = n_salida
        if n_llegada > maximo_llegada:
            maximo_hora_llegada = (key, n_llegada)
            maximo_llegada = n_llegada
    
    return (out_total_tiempo, out_total_viajes, maximo_v_salida, maximo_v_llegada, maximo_hora_salida, maximo_hora_llegada)

def actualizar_viajes_anuales_InOut(analyzer, service):

    # Primero, necesitamos reconstruir los vértices
    ver1 = "{0}-{1}".format(service['Start Station Id'], service['Start Station Name'])
    ver2 = "{0}-{1}".format(service['End Station Id'], service['End Station Name'])
    map = analyzer["viajes_InOut_por_vertice"]

    # Luego, podemos guardar la tupla con los services que entran
    exist_ver1 = mp.get(map, ver1)
    if exist_ver1 is None:
        mp.put(map, ver1, (0,0))
        exist_ver1 = mp.get(map, ver1)

    in_trips1, out_trips1 = exist_ver1["value"]
    out_trips1 += 1

    mp.put(map, ver1,(in_trips1, out_trips1))
    
    # Y los que salen
    exist_ver2 = mp.get(map, ver2)
    if exist_ver2 is None:
        mp.put(map, ver2, (0,0))
        exist_ver2 = mp.get(map, ver2)

    in_trips2, out_trips2 = exist_ver2["value"]
    in_trips2 += 1

    mp.put(map, ver2,(in_trips2, out_trips2)) 

def actualizar_viajes_anuales_hora(analyzer, service):
    # En la llave, está la hora y como valor una tupla (n_inicio, n_final)
    horaInicio = hour_determiner(service['Start Time'])
    horaFin = hour_determiner(service['End Time'])
    map = analyzer['viajes_por_hora_anuales']

    exist_ver1 = mp.get(map, horaInicio)
    if exist_ver1 is None:
        mp.put(map, horaInicio, (0,0))
        exist_ver1 = mp.get(map, horaInicio)

    in_hora, out_hora = exist_ver1["value"]
    out_hora += 1

    mp.put(map, horaInicio,(in_hora, out_hora))
    
    # Y los que salen
    exist_ver2 = mp.get(map, horaFin)
    if exist_ver2 is None:
        mp.put(map, horaFin, (0,0))
        exist_ver2 = mp.get(map, horaFin)

    in_hora, out_hora = exist_ver2["value"]
    in_hora += 1

    mp.put(map, horaFin,(in_hora, out_hora))

def R6_answer(analyzer, bike_inp):
    num_viajes, timpo_rec = mp.get(analyzer["bikes_info"], bike_inp)["value"]
    vert_max_out = inpq.min2(mp.get(analyzer["bike_out_pq"], bike_inp)["value"])
    vert_max_in = inpq.min2(mp.get(analyzer["bike_in_pq"], bike_inp)["value"])

    return num_viajes, timpo_rec, vert_max_out, vert_max_in



def R7_answer(analyzer, vert_inp, date1, date2):
    RBT_fechas = analyzer['date_tree_2']
    
    lista_fechas_que_cumplen = om.keys(RBT_fechas, date1, date2)

    
    analyzer["R7_vert_pq"] = inpq.newIndexMinPQ(minpq_compare) 
    analyzer["in_n_out_trips_hash2"] = None

    for fecha in lt.iterator(lista_fechas_que_cumplen):

        lista_de_la_fecha = om.get(RBT_fechas, fecha)['value']
        
        for service in lt.iterator(lista_de_la_fecha):
            vert1, vert2 = vert_names(analyzer, service)
            addTo_in_n_out_trips_hash2(analyzer, vert1, vert2, vert_inp)

            if vert1 == vert_inp:
                update_heap_vert(analyzer, vert2, service)
    

    in_trips, out_trips = analyzer["in_n_out_trips_hash2"]
    most_trips_ended = inpq.min2(analyzer["R7_vert_pq"])

    return in_trips, out_trips, most_trips_ended

def update_heap_vert(analyzer, vert, service):
    heap = analyzer["R7_vert_pq"]
    if not inpq.contains(heap, vert):
        inpq.insert(heap,vert,0)

    inpq.increaseKey2(heap, vert)



    
def addTo_in_n_out_trips_hash2(analyzer, ver1, ver2, vert_inp):

    if analyzer["in_n_out_trips_hash2"] == None:
        analyzer["in_n_out_trips_hash2"] = (0,0)

    in_trips, out_trips = analyzer["in_n_out_trips_hash2"]
    if ver1 == vert_inp:
        out_trips += 1
    
    if ver2 == vert_inp:
        in_trips +=1
    
    analyzer["in_n_out_trips_hash2"] = (in_trips, out_trips)


def vert_names(analzer, service):
    map = analzer["name_to_vertice"]

    start_name = service["Start Station Name"]
    end_name = service["End Station Name"]

    if start_name == "":
        start_name = "Unknown Station"
    
    if end_name == "":
        end_name = "Unknown Station"
    
    start_id = service["Start Station Id"]
    end_id = service["End Station Id"]

    vertice1 = "{0}-{1}".format(start_id, start_name)
    vertice2 = "{0}-{1}".format(end_id, end_name)

    return (vertice1, vertice2)

# Funciones utilizadas para comparar elementos dentro de una lista




