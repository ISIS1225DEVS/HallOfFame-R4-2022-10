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
from DISClib.ADT import graph as gr
assert cf
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Requerimiento 1 ")
    print("2- Requerimiento 2 ")
    print("3- Requerimiento 3 ")
    print("4- Requerimiento 4 ")
    print("6- Requerimiento 6 ")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        print("Cargando información de los archivos ....")
        analizer=controller.analizerStart()
        controller.loadData(analizer)
        inicio, final=controller.createGraph(analizer)
        controller.createGraphNodir(analizer)
        print('NUMERO VERTICES DIRIJIDO: ' +str(gr.numVertices(analizer['dirGraph'])))
        print('NUMERO EDGES DIRIJIDO: ' +str(gr.numEdges(analizer['dirGraph'])))
        print('NUMERO VERTICES NO  DIRIJIDO: ' +str(gr.numVertices(analizer['dirGraph'])))
        print('NUMERO EDGES NO DIRIJIDO: ' +str(gr.numEdges(analizer['dirGraph'])))
        print('------------------------------------------------\n')
        print("PRIMEROS 5 DIRIJIDO: ")
        for valor in lt.iterator(inicio):
            print(valor)
        print('------------------------------------------------\n')
        print("Ultimos 5 No DIRIJIDO: ")
        for valor in lt.iterator(final):
            print(valor)
        print('------------------------------------------------\n')
        print("PRIMEROS 5 NO DIRIJIDO: ")
        for valor in lt.iterator(inicio):
            print(valor)
        print('------------------------------------------------\n')
        print("ULTIMOS 5 NO DIRIJIDO: ")
        for valor in lt.iterator(final):
            print(valor)
        
    elif int(inputs[0]) == 1:
        listaRespuesta=controller.repuestaReq1(analizer)
        print("")
        for elemento in lt.iterator(listaRespuesta):
            print(elemento)
    elif int(inputs[0]) == 2:
        #'Lake Shore Blvd W / Ontario Dr'
        station=str(input('estacion: '))
        llaveValor=mp.get(analizer['dictAuxiliar'], station)
        numEstaciones=int(input('NumeroParadas: '))
        duration1=int(input('duracion: '))
        duration=duration1/2
        numRutas=int(input('Num Rutas: '))
        llaveValor=mp.get(analizer['dictAuxiliar'], station)
        vertex=me.getValue(llaveValor)
        lista=controller.shortestPath(analizer, vertex, numEstaciones, duration1, numRutas)
        print('------------------------------------------------')
        print('Estacion de Inicio: '+station)
        print('Tiempo: '+str(duration))
        print('Paradas: '+str(numEstaciones))
        for respuesta in lt.iterator(lista):
            print('------------------------------------------------\n')
            totalStops, time, estaciones, size=respuesta
            print('Paradas Totales: '+str(totalStops))
            print('timepo Recorrido :'+str(time))
            print('RECORRIDO ESTACIONES ID NOMBRE: ')
            for valor in lt.iterator(estaciones):
                print(valor)
            print('------------------------------------------------\n')
    elif int(inputs[0]) == 3:
        respuesta1=controller.stronlgyConected(analizer)
        respuesta, count=respuesta1
        print('--------------------------------------------')
        print("EN ESTE GRAFO EXISTEN "+str(count)+" SCC")
        print('--------------------------------------------')
        print("PRIMEROS 3")
        print('')
        i=0

        while i<3:
            tupla=lt.getElement(respuesta, i)
            a,b,c=tupla
            print(a)
            print(b)
            print(c)
            print('')
            i+=1
        tamanio=len(respuesta)
        i=0
        inti=tamanio
        print('--------------------------------------------')
        print("UlTIMOS 3")
        print('')
        while i<=3:
            tupla=lt.getElement(respuesta, inti)
            a,b,c=tupla
            print(a)
            print(b)
            print(c)
            print('')
            i+=1
            inti-=1
        print('--------------------------------------------\n')
    elif int(inputs[0]) == 4:
        #Fort York  Blvd / Capreol Ct
        #Yonge St / St Clair Ave
        estacionI=str(input('Estacion Inincio: '))
        estacionF=str(input('Estacion Final: '))
        llaveValorI=mp.get(analizer['dictAuxiliar'], estacionI)
        vertexI=me.getValue(llaveValorI)
        llaveValorF=mp.get(analizer['dictAuxiliar'], estacionF)
        vertexF=me.getValue(llaveValorF)
        ruta, time=controller.requerimiento4(analizer, vertexI, vertexF)
        print('--------------------------------------------\n')
        print('VERTICE INICIAL CON ID'+str(vertexI))
        print('VERTICE FINAL CON ID'+str(vertexF))
        print('--------------------------------------------\n')
        print('LA RUTA ENTRE LOS VERTICES ES: ')
        for value in lt.iterator(ruta):
            print(value)
        print('\nEL TIEMPO DE LA RUTA ES: '+str(time))


    elif int(inputs[0]) == 6:
        bikeId=int(input("Ingrese Bike ID: "))
        viajes=controller.bikeNum(analizer, bikeId)
        print('--------------------------------------------\n')
        print('CON ESTA BICICLETA SE HAN EFECTUADO '+str(viajes)+' VIAJES ')
        print('--------------------------------------------\n')



    else:
        sys.exit(0)
sys.exit(0)