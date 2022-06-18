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

from cgitb import small
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printReqOne(station):

    dates = station["dates"]
    hours = station["hours"]

    max_date_count = 0
    date_with_max_count = None
    for date, value in dates.items():
        if value > max_date_count:
            max_date_count = value
            date_with_max_count = date

    max_hour_count = 0
    hour_with_max_count = None
    for hour, value in hours.items():
        if value > max_hour_count:
            max_hour_count = value
            hour_with_max_count = hour 

    return [
        station["id"], 
        station["name"],
        station["from_count"],
        station["casuals"],
        station["annuals"],
        date_with_max_count,
        hour_with_max_count
    ]

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1: Comprar bicicletas para las estaciones con más viajes de origen")
    print("3- Requerimiento 2: Planear paseos turísticos por la ciudad")
    print("4- Requerimiento 3: Reconocer los componentes fuertemente conectados del sistema")
    print("5- Requerimiento 4: Planear una ruta rápida para el usuario")
    print("6- Requerimiento 5: Reportar rutas en un rango de fechas para los usuarios anuales")
    print("7- Requerimiento 6: Planear el mantenimiento preventivo de bicicletas")
    print("8- Requerimiento 7(b): La estación más frecuentada por los visitantes")
    print("0- salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = controller.newController()
        print("Cargando información de los archivos ....")
        file_size = "small"
        controller.loadData(catalog, file_size)
        """
        Los viajes tienen una estación de origen y un destino, por lo que pueden representar arcos donde la
        estación de origen y la de destino, son los vértices del grafo; esta información puede ayudar a tener
        una visión general del uso de las bicicletas por parte de los usuarios.
        Cada arco del grafo tendrá como peso, el promedio de los tiempos reportados por todos los viajeros
        que han iniciado y terminado un viaje en un par de estaciones.
        Al final de la carga hay que reportar los siguientes datos:
            • El total de viajes obtenidos de los datos.
            • El total de vértices del grafo.
            • El total de arcos del grafo.
            • Mostrar los primeros cinco y últimos cinco vértices registrados en el grafo con las siguientes
            características:
                o ID de la estación.
                o Nombre de la estación.
                o Numero de viajes de salida y de llegada (grado de entrada y salida del vértice).
        """

    elif int(inputs[0]) == 2:
        #req1
        """
        Como el equipo de análisis deseo indicar las 5 estaciones desde donde se inician más viajes por
        parte de los usuarios para adquirir nuevas bicicletas y ponerlas a disposición de los usuarios.
        No se requieren parámetros de entrada para este requerimiento, se utiliza la totalidad del grafo.
        La respuesta esperada debe contener:
            • las 5 estaciones solicitadas con la siguiente información:
                o Identificador de la estación.
                o Nombre de la estación.
                o Cantidad de viajes que han iniciado en esa estación.
                o El total de viajes iniciados por tipo de usuario.
                o La fecha (formato “MM/DD/AAAA”) y la hora del día (0:00 - 0:59, 1:00 - 1:59 am,
                2:00 - 2:59, …, 23:00 - 23:59) en la que más viajes se inician.

        """
        stations = controller.getMostStartStations(catalog)
        stations_table = []
        for station in stations["elements"]:
            stations_table.append(printReqOne(catalog["stations_map"][station["id"]]))

        print(tabulate(stations_table, headers=["id", "name", "from_count", "casuals", "annuals", "date with max", "hour with max" ], tablefmt="grid"))
            
    elif int(inputs[0]) == 3:
        #req2
        start_station = input("El nombre de la estación de inicio: ")
        available_time = input("La disponibilidad del usuario para su paseo: ")
        min_stations = input("El número mínimo de estaciones de parada para la ruta: ")
        max_routes = input("El máximo número de rutas de respuesta: ")
        """
       Los parámetros de entrada de este requerimiento son:
        • El nombre de la estación de inicio.
        • La disponibilidad del usuario pasa su paseo.
        • El número mínimo de estaciones de parada para la ruta (sin incluir la estación de inicio)
        • El máximo número de rutas de respuesta.
            La respuesta esperada debe contener:
            • las posibles rutas (que no excedan el número máximo de respuesta, sin ningún orden en
            particular). Por cada una de ellas se debe mostrar la siguiente información:
                o El número de estaciones visitadas.
                o La secuencia de las estaciones de cada viaje (indicando el ID y nombre de cada una
                de ellas).
                o El tiempo total de la ruta.
        """

        """
        numero de estaciones visitadas
        secuencia ( id, nombre estacion)
        tiempo ruta
        """
        routes = controller.findRoutes(catalog, start_station, int(available_time), int(min_stations), int(max_routes))
        for route in routes:
            print("Estaciones visitadas: ", len(route))
            print("Secuencia: ", controller.getRouteSequence(catalog, route))
            print("Tiempo total: ", str(controller.getRouteTime(route)))

    elif int(inputs[0]) == 4:
        #req3
        """
        La respuesta esperada debe contener:
            • El total de componentes fuertemente conectadas y para cada uno de ellos se debe mostrar
            siguiente información:
                o El número de estaciones en el componente
                o El identificador y nombre de la estación donde más viajes inician.
                o El identificador y nombre de la estación donde más viajes terminan.
        """
        components = controller.strongLinked(catalog)
        print("Componentes")
        print(tabulate(controller.componentData(catalog, components), headers=["component_stations", "station_id", "station_name"], tablefmt="grid"))

    
    elif int(inputs[0]) == 5:
        #req4
        start_station = input("Nombre estación de origen: ")
        end_station = input("Nombre estación de destino: ")

        """
        Los parámetros de entrada de este requerimiento son:
            • Nombre de la estación origen.
            • Nombre de la estación destino.
                La respuesta esperada debe contener:
                    • El tiempo total que tomará el recorrido entre la estación origen y la estación destino.
                    • La ruta calculada entre las estaciones (incluyendo el origen y el destino) y para cada estación
                    en la ruta se debe mostrar la siguiente información:
                        o El número de identificación de la estación.
                        o El nombre de la estación.
                        o El tiempo promedio a la siguiente estación en la ruta.
        """
        route = controller.fastestRoute(catalog, start_station, end_station)
        print("Tiempo total: ", controller.getTotalTimeFastestRoute(route))
        print(tabulate(controller.getFastestRouteSequence(catalog, route), headers=["id", "name", "time"], tablefmt="grid"))
           
    elif int(inputs[0]) == 6:
        #req5
        start_date = input("Fecha inical de consulta (MM/DD/AAAA): ")
        end_date = input("Fecha final de consulta (MM/DD/AAAA): ")

        """
       Los parámetros de entrada de este requerimiento son:
            • Fecha inicial de consulta (formato “MM/DD/AAAA”).
            • Fecha final de consulta (formato “MM/DD/AAAA”).
                La respuesta esperada debe generar un reporte consolidado que incluya la siguiente información:
                • El total de viajes realizados.
                • El total de tiempo invertido en los viajes.
                • La estación de origen más frecuentada.
                • La estación de destino más utilizada.
                • La hora del día en la que más viajes inician (0:00-0:59, 1:00-1:59 am, 2:00-2:59, …, 23:00-23:59)
                • La hora del día en la que más viajes terminan (0:00-0:59, 1:00-1:59 am, 2:00-2:59, …, 23:00-23:59)
        """
        annual_user_report = controller.annualUserReport(catalog, start_date, end_date)
        print("Total viajes: ", annual_user_report["total_trips"])
        print("Tiempo total: ", annual_user_report["total_time"])
        print("Estación de origen más frecuentada: ", 
            catalog["stations_map"][annual_user_report["start_station"]["key"]]["name"] + " - " + str(annual_user_report["start_station"]["value"])
            )
        print("Estación de destino más frecuentada: ", 
            catalog["stations_map"][annual_user_report["end_station"]["key"]]["name"] + " - " + str(annual_user_report["end_station"]["value"])
            )
        hour = str(annual_user_report["start_hour"]["key"])
        print("Hora del día en que mas viajes inician", hour + ":00-" + hour + ":59")
        hour = str(annual_user_report["end_hour"]["key"])
        print("Hora del día en que mas viajes finalizan", hour + ":00-" + hour + ":59")
        

    elif int(inputs[0]) == 7:
        #req6
        bike_id = input("El identificador de la bicicleta en el sistema: ")

        """
        El parámetro de entrada de este requerimiento es:
            • El identificador de la bicicleta en el sistema
                La respuesta esperada debe generar un reporte consolidado que incluya la siguiente información:
                    • El total de viajes en los que ha participado dicha bicicleta.
                    • El total de horas de utilización de la bicicleta.
                    • La estación en la que más viajes se han iniciado en esa bicicleta.
                    • La estación en la que más viajes ha terminado dicha bicicleta.
        """
        usage = controller.bikeUsage(catalog, bike_id)
        print("Total viajes: ", usage["total_trips"])
        print("Total horas: ", int(usage["total_time"] / 60))
        print("Estación con más inicios: ",  
            catalog["stations_map"][usage["start_station"]["key"]]["name"] + " - " + str(usage["start_station"]["value"])
            )
        print("Estación con más terminaciones: ",  
            catalog["stations_map"][usage["end_station"]["key"]]["name"] + " - " + str(usage["end_station"]["value"])
            )

    elif int(inputs[0]) == 8:
        #req7    bono
        station = input("Nombre de la estación: ")
        start_date = input("Fecha de inicio: ")
        end_date = input("Hora de inicio: ")
       
        """
        Los parámetros de entrada de este requerimiento son:
            • Nombre de la estación.
            • Fecha y hora de inicio.
            • Fecha y hora de finalización.
                La respuesta esperada debe generar un reporte consolidado que incluya la siguiente información:
                    • El total de viajes que iniciaron en dicha estación en el rango de tiempo solicitado.
                    • El total de viajes que terminaron en dicha estación en el rango de tiempo solicitado.
                    • El viaje de mayor duración promedio saliendo de la estación de consulta.
                    • La estación donde terminaron la mayoría de los viajes que iniciaron en la estación.
        """
        frequency = controller.mostFrequentStation(catalog, station, start_date, end_date)
        print("Total viajes que iniciaron: ", frequency["total_trips_start"])
        print("Total viajes que terminaron: ", frequency["total_trips_end"])
        print("Viaje con mayor duración saliendo: ", frequency["max_average_time"]["quantity"])
        print("Estación donde terminaron la mayor canditdad de viejas: ",  
            catalog["stations_map"][frequency["end_stations"]["key"]]["name"] + " - " + str(frequency["end_stations"]["value"])
            )



    else:
        print("Adios")
        sys.exit(0)




sys.exit(0)



