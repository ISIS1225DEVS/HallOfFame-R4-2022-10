"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib.ADT import stack
from DISClib.ADT import indexminpq as inpq
from datetime import datetime as dt
assert cf




"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printTiempo_Memoria(tiempo, memoria): 
    mensaje = "****  Tiempo [ms]: {0} | Memoria [kb]: {1}  ****".format(round(tiempo,2), round(memoria,2))
    print(mensaje)


def print_Carga(analyzer, Total_trips):
    print("\nEl total de viajes en el archivo son: {0}".format(Total_trips))

    #En small debe ser 709
    print("El total de vertices en el grafo es: {0}".format(lt.size(analyzer["vertices_list"])))

    #En small debe ser 24 056 o 24 113
    print("El total de arcos es: {0}".format(mp.size(analyzer["edge_map"])))
    
    vert_list = lt.newList("ARRAY_LIST")
    for i in range(1,11):
        if i < 6:
            lt.addLast(vert_list, lt.getElement(analyzer["vertices_list"], i))
        else:
            lt.addLast(vert_list, lt.getElement(analyzer["vertices_list"], lt.size(analyzer["vertices_list"])-(10-i)))
    

    vert_num = 1
    print("\nPrimeros 5 Vertices registrados: \n")
    for vert in lt.iterator(vert_list):
        in_trips, out_trips = mp.get(analyzer["in_n_out_trips_hash"], vert)["value"]
        in_degree = gr.indegree(analyzer["graph"], vert)
        out_degree = gr.outdegree(analyzer["graph"], vert)
        print(
            "Id y Nombre de la estación: " + vert + "\n" +
            "# de Viajes de salida: " + str(out_trips) + "\n" +
            "# de Viajes de llegada: " + str(in_trips) + "\n" +
            "Out Degree del Vertice: " + str(out_degree) + "\n" + 
            "In Degree del Vertice: " + str(in_degree) + "\n" )
        vert_num +=1
        if vert_num == 6:
            print("Últimos 5 Vertices registrados: \n")

def print_R1(top_5_list):
    for vert, count in lt.iterator(top_5_list):
        rush_hour = inpq.min(mp.get(analyzer["vert_rush_hour"], vert)["value"])
        rush_day = inpq.min((mp.get(analyzer["vert_rush_day"], vert)["value"]))
        casual, annual =mp.get(analyzer["member_vert"],vert)["value"]
        print(
            "Id y Nombre de la estación: " + vert + "\n" +
            "# de Viajes de iniciados: " + str(count) + "\n"+
            "# de Viajes por usuarios Casuales: " + str(casual) + "\n"+
            "# de Viajes por usuarios Anuales: " + str(annual) + "\n"+
            "Rush day: " + rush_day + "\n"
            "Rush hour: "+ rush_hour +"\n"
        )
def print_R2(limite_estaciones, limite_tiempo_min, limite_estaciones_maximo, FittingPaths):
    tam = lt.size(FittingPaths)
    print("====="*20)
    print(' |   Para un recorrido total (ida y regreso) de: {0} minutos'.format(limite_tiempo_min))
    print(' |   para un máximo de {0} estaciones diferentes a la inicial, '.format(limite_estaciones_maximo))
    print(' |   y para un mínimo de {0} estaciones diferentes a la inicial, '.format(limite_estaciones))
    print(  "\033[1m" +
            ' |   el número de rutas que cumplen es de: {0}'.format(tam) +
            "\033[0m" 
    )
    print('\n')
    print(' >>>       Primeros tres caminos:')
    for i in [1,2,3, tam-2, tam-1, tam]:
        elemento = lt.getElement(FittingPaths, i)
        if i == tam-2:
            print(' >>>      Últimos tres caminos:')
        string = '\033[1m Recorrido: \033[0m '
        
        pila_camino = elemento[0]
        while not (stack.isEmpty(pila_camino)):
            stop = stack.pop(pila_camino)
            string += stop['vertexA'] + '  ->  '
            
        print(string[:-4])

        print('\033[1m # Estaciones: \033[0m ' + str(elemento[1]))
        print('\033[1m # Tiempo (ida) [min]: \033[0m ' + str(round(elemento[2]/60, 2)))
        print('\033[1m # Tiempo (ida y vuelta) [min]: \033[0m ' + str(round(elemento[2]/60, 2)*2))
        print("\n")
def print_R3(num_scc):
    num_scc,  resp_list = answer
    print("\nSe han encontrado {0} componentes fuertemente conectados".format(num_scc))
    

    for tupla in lt.iterator(resp_list):
        
        valor, max_out, max_in, size = tupla

        nada1, out_trips = mp.get(analyzer["in_n_out_trips_hash"], max_out)["value"]
        in_trips, nada2 = mp.get(analyzer["in_n_out_trips_hash"], max_in)["value"]

        print(
            "ID del Componente: " + str(valor) + "\n"+ 
            "Tamaño del Componente: " + str(size) + "\n"+
            "Vertice con más viajes iniciados: " + max_out +", " + str( out_trips) + "\n"+ 
            "Vertice con más viajes terminados: " + max_in +", " + str(in_trips) + "\n"
        )


def print_R4(distance, path):
    print("\nEl tiempo total del recorrido es: {0} s.".format(distance))
    print("Se encontró el siguiente camino:")
    pathlen = stack.size(path)
    print('El camino es de longitud: ' + str(pathlen))
    while (not stack.isEmpty(path)):
        stop = stack.pop(path)
        print(stop)

def print_R5(tupla_completa, fecha_inicial, fecha_final):
    (out_total_tiempo, out_total_viajes, maximo_v_salida, maximo_v_llegada, maximo_hora_salida, maximo_hora_llegada) = tupla_completa 
    total_tiempo_h = round(out_total_tiempo/3600, 2)
    print('     Entre las fechas {0} y {1} se encontraron \033[1m {2} viajes \033[0m'.format(fecha_inicial, fecha_final, out_total_viajes))
    print('     Estos viajes suman un acumulado de \033[1m {0} segundos o {1} horas \033[0m'.format(out_total_tiempo, total_tiempo_h))
    print("\n")
    print('     La estación de origen más frecuentada corresponde con: \033[1m {0} y {1} viajes de salida\033[0m'.format(maximo_v_salida[0], maximo_v_salida[1]))
    print('     La estación de llegada más frecuentada corresponde con: \033[1m {0} y {1} viajes de salida\033[0m'.format(maximo_v_llegada[0], maximo_v_llegada[1]))
    print("\n")
    print('     La hora de salida más común corresponde con:  \033[1m {0} y {1} viajes de salida\033[0m'.format(maximo_hora_salida[0], maximo_hora_salida[1]))
    print('     La hora de llegada más común corresponde con: \033[1m {0} y {1} viajes de llegada\033[0m'.format(maximo_hora_llegada[0], maximo_hora_llegada[1]))

def print_R6(num_viajes, timpo_rec, vert_max_out, vert_max_in, bike_inp):
    print(
        "\nSe realizaron {0} viajes con la bicicleta de ID {1}. \n".format(num_viajes, bike_inp) + 
        "El tiempo total de recorrido son {0}s o {1} horas. \n".format(timpo_rec, round(timpo_rec/3600, 2)) + 
        "La estación que más salidas con la bicicleta fue: \n "+
        "{0} con un total de {1} viajes\n".format(vert_max_out["key"], -vert_max_out["index"]) + 
        "La estación que más llegadas con la bicicleta fue: \n "+
        "{0} con un total de {1} viajes. \n".format(vert_max_in["key"], -vert_max_in["index"]) 
    )

def print_R7(in_trips, out_trips, most_trips_ended, vert_inp):
    print(
        "\nEn la estación {0}: \n".format(vert_inp) +
        "Se iniciaron {0} viajes. \n".format(out_trips) + 
        "Se terminaron {0} viajes. \n".format(in_trips) + 
        "El camino de mayor recorrido fue: NONE :´) \n" +
        "Y la mayoria de viajes terminaron en la estación: \n" +
        "{0} con un total de {1} viajes. \n".format(most_trips_ended["key"], -most_trips_ended["index"])
    )

def printMenu():
    print("====="*20)
    print("          >>               Bienvenido                    <<     ")
    print("  [R0]   q- Cargar información al analizador.")
    print("  [R1]   1- Comprar bicicletas para las estaciones con más viajes de origen.")
    print("  [R2]   2- Planear paseos turísticos por la ciudad.")
    print("  [R3]   3- Reconocer los componentes fuertemente conectados del sistema.")
    print("  [R4]   4- Planear una ruta rápida para el usuario. ")
    print("  [R5]   5- Reportar rutas en un rango de fechas para los usuarios anuales.")
    print("  [R6]   6- Planear el mantenimiento preventivo de bicicletas.")
    print("  [R7]   7- La estación más frecuentada por los visitantes.")
    print("         0- Salir")
    print("====="*20)

analyzer = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar: ')
    if inputs == "q":
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        time, memory, Total_trips = controller.loadServices(analyzer)

        print_Carga(analyzer, Total_trips)
        printTiempo_Memoria(time, memory)



    elif inputs == "1":
        time, memory, top_5_list = controller.callR1(analyzer)
        print_R1(top_5_list)
        printTiempo_Memoria(time, memory)
    elif inputs == "2":
        origin_inp = input("Ingrese la estación de origen: ")
        estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)
        if estaciones_con_nombre is None:
            print("No se encontro la estación ingresada.")
        else:
            print("Se encontraron las siguientes estaciones: \n")
            estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)["value"]
            num_est = 1
            estaciones_show = ""
            for estacion in lt.iterator(estaciones_con_nombre):
                mensaje = "{0}. {1} \n".format(num_est, estacion)
                num_est +=1
                estaciones_show += mensaje 
            print(estaciones_show)
            origen = input("Por favor elija una: ")
            
            if origen not in estaciones_show:
                print("No eligió correctamente.")
            else:
                limite_estaciones = int(input('> # de estaciones mínimas (dif. a la inicial): '))
                limite_estaciones_maximo = int(input('> # de rutas: '))
                limite_tiempo_min = int(input('> Tiempo máximo del recorrido [min]: '))
                limite_tiempo = limite_tiempo_min*60

                time, memory, FittingPaths = controller.callR2(analyzer, origen, limite_estaciones, limite_tiempo, limite_estaciones_maximo)

                if FittingPaths is None or lt.isEmpty(FittingPaths):
                    print('Por favor, vuélvalo a intentar')


                print_R2(limite_estaciones, limite_tiempo_min, limite_estaciones_maximo, FittingPaths)
                printTiempo_Memoria(time, memory)

    elif inputs == "3":
        time, memory, answer = controller.callR3(analyzer)

        print_R3(answer)
        printTiempo_Memoria(time, memory)

    elif inputs == "4":
        origin_inp = input("Ingrese la estación de origen: ")
        estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)
        if estaciones_con_nombre is None:
            print("No se encontro la estación ingresada.")
        else:
            print("Se encontraron las siguientes estaciones: \n")
            estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)["value"]
            num_est = 1
            estaciones_show = ""
            for estacion in lt.iterator(estaciones_con_nombre):
                mensaje = "{0}. {1} \n".format(num_est, estacion)
                num_est +=1
                estaciones_show += mensaje 
            print(estaciones_show)
            origen = input("Por favor elija una: ")
            
            if origen not in estaciones_show:
                print("No eligió correctamente.")
            else:
                destination_inp = input("Ingrese la estación de destino: ")
                estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], destination_inp)
                if estaciones_con_nombre is None:
                    print("No se encontro la estación ingresada.")
                else:
                    print("Se encontraron las siguientes estaciones: \n")
                    num_est = 1
                    estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], destination_inp)["value"]
                    estaciones_show = ""
                    for estacion in lt.iterator(estaciones_con_nombre):
                        mensaje = "{0}. {1} \n".format(num_est, estacion)
                        num_est +=1
                        estaciones_show += mensaje 
                    print(estaciones_show)
                    destination = input("Por favor elija una: ")
                    
                    if destination not in estaciones_show:
                        print("No eligió correctamente.")
                    
                    elif origen == destination:
                        print("No se puede ingresar la misma estación como origen y destino")
                    else:
                        time, memory, distance, path = controller.callR4(analyzer,origen, destination)
                        if type(distance) == type(""):
                            print(distance)
                        else:
                            print_R4(distance, path)
                        printTiempo_Memoria(time, memory)


        
    elif inputs == "5":
        fecha_inicial = input('Ingrese la fecha de inicio (%m/%d/%Y): ')
        fecha_final   = input('Ingrese la fecha de fin    (%m/%d/%Y): ')

        tupla_completa = controller.callR5(analyzer, fecha_inicial, fecha_final)
        time, memory, tupla_c = tupla_completa
        print_R5(tupla_c, fecha_inicial, fecha_final)
        printTiempo_Memoria(time, memory)

    elif inputs == "6":
        bike_inp = input("Ingrese el ID de la bicicleta que desea buscar: ")

        time, memory, num_viajes, timpo_rec, vert_max_out, vert_max_in = controller.callR6  (analyzer, bike_inp)

        print_R6(num_viajes, timpo_rec, vert_max_out, vert_max_in, bike_inp)
        printTiempo_Memoria(time, memory)

    elif inputs == "7":
        date1 = input('Ingrese la fecha de inicio (%m/%d/%Y %H:%M): ')
        date2 = input('Ingrese la fecha de fin    (%m/%d/%Y %H:%M): ')
        origin_inp = input("Ingrese la estación de origen: ")
        estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)
        if estaciones_con_nombre is None:
            print("No se encontro la estación ingresada.")
        else:
            print("Se encontraron las siguientes estaciones: \n")
            estaciones_con_nombre = mp.get(analyzer["name_to_vertice"], origin_inp)["value"]
            num_est = 1
            estaciones_show = ""
            for estacion in lt.iterator(estaciones_con_nombre):
                mensaje = "{0}. {1} \n".format(num_est, estacion)
                num_est +=1
                estaciones_show += mensaje 
            print(estaciones_show)
            vert_inp = input("Por favor elija una: ")
            
            if vert_inp not in estaciones_show:
                print("No eligió correctamente.")
            else:

                time, memory, in_trips, out_trips, most_trips_ended  = controller.callR7(analyzer, vert_inp, date1, date2)
            
                print_R7(in_trips, out_trips, most_trips_ended, vert_inp)
                printTiempo_Memoria(time, memory)

    else:
        sys.exit(0)
sys.exit(0)
