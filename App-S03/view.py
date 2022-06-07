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


import sys
import config
import threading
from App import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from tabulate import tabulate
import time
import tracemalloc
assert config
import math as math




#___________________________________________________
#  Variables
#___________________________________________________

file = 'Bikeshare-ridership-2021-utf8-small.csv'

# ________________________________________________________________________________
#  Funciones auxiliares para imprimir y medir el tiempo y la memoria
# ________________________________________________________________________________


def printTable(lista,columnas,all):
    nuevaLista=[]
    for i in range(1,lt.size(lista)+1):
        dic={}
        elemento=lt.getElement(lista,i)
        for j in columnas:
            dic[j]=elemento[j]
        dic=fitWidth(dic,columnas,all)
        nuevaLista.append(dic)
    print("")
    print(tabulate(nuevaLista,headers="keys",tablefmt="fancy_grid"))

def fitWidth(dic,columnas,all):
    if all==False:
        if len(columnas)<10:
            maxW=40
        else:
            maxW=10
        for i in columnas:
            if type(dic[i])!=str:
                dic[i]=str(dic[i])
            if dic[i] == "":
                dic[i] = "Unknown"
            d=len(dic[i])
            if d>maxW and d<2*maxW:
                l=""
                l=dic[i]
                dic[i]=l[:maxW]+"-\n"+l[maxW:]
            elif d>=2*maxW and d<=3*maxW:
                l=""
                l=dic[i]
                dic[i]=l[:maxW]+"-\n"+l[maxW:2*maxW]+"-\n"+l[2*maxW:3*maxW]
            elif d>3*maxW:
                l=""
                l=dic[i]
                dic[i]=l[:maxW]+"-\n"+l[maxW:2*maxW]+"-\n"+l[2*maxW:(3*maxW-4)]+"..."
        return dic
    else:
        for i in columnas:
            if dic[i]=="":
                dic[i]="Unknown"
            if type(dic[i])!=str:
                dic[i]=str(dic[i])
            d=len(dic[i])
            maxW=150
            l=""
            l=dic[i]
            dic[i]=l[:maxW]
            for j in range(1,math.ceil(d/maxW)+1):
                dic[i]=dic[i]+"\n"+l[j*maxW:(j+1)*maxW]
        return dic


# ___________________________________________________________
#  Funciones asociadas al menú
# ___________________________________________________________


def printMenu0():
    print("\n")
    print("*************************************************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("*************************************************************************")

def printMenu():
    print("\n")
    print("*************************************************************************")
    print("Bienvenido")
    print("1- REQUERIMIENTO 1: Indicar estaciones donde se inician más viajes")
    print("2- REQUERIMIENTO 2: Planear paseos turísticos por la ciudad")
    print("3- REQUERIMIENTO 3: Obtener componentes conectados")
    print("4- REQUERIMIENTO 4: Planear ruta rápida")
    print("5- REQUERIMIENTO 5: Viajes en un rango de fechas")
    print("6- REQUERIMIENTO 6: Obtener información de una bicicleta")
    print("*************************************************************************")


# ___________________________________________________________
#  Funciones para cargar, limpiar y organizar información
# ___________________________________________________________

def optionTwo(cont):
    print("")
    print("###"*50)
    print("")        
    print("\nCargando, limpiando y organizando información ...")
    cont,k=controller.loadAndCleanData(cont, file)
    numTrips = controller.totalTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStations(cont)
    print("")
    print("###"*50)
    print("")   
    print("\nNúmero total de viajes cargados: " + str(k))
    print("Número total de viajes utilizados: " + str(numTrips))
    print('Número de vertices: ' + str(numvertex))
    print('Número de arcos: ' + str(numedges))
    vertices=controller.getVertices(cont)
    firstAndLast5=controller.firstAndLast5(vertices)
    firstAndLast5=controller.getInfoVert(cont,firstAndLast5)
    colums=["station","inEdges","outEdges","inTrips","outTrips"]
    printTable(firstAndLast5,colums,False)

# ___________________________________________________________
#  REQUERIMIENTO 1: ESTACIONES CON MÁS VIAJES DE SALIDA
# ___________________________________________________________

def req1(cont):
    print("")
    print("###"*50)
    print("")   
    print("Analizando datos ...")    
    orderedVert=controller.orderVerticesByEdgeOuts(cont)
    colums=["vertice","numOutTrips","Casual Member","Annual Member","mostFrequentDate","mostFrequentHour"]
    print("")
    print("###"*50)
    print("")   
    print("\nLas 5 estaciones con más viajes de salida:")
    printTable(orderedVert,colums,False)

# _______________________________________________________________
#  REQUERIMIENTO 2: PLANEAR PASEOS TURÍSTICOS
# _______________________________________________________________

def req2(cont,initialStationName,maxTime,minStations,numAnswers):   
    print("")
    print("###"*50)
    print("")
    print("Identificando el vértice asociado a la estación de inicio ...")
    initialStation=controller.getVertFromNameStation(cont,initialStationName)
    print("Calculando caminos de búsqueda ...")
    controller.searchPaths(cont,initialStation)
    print("Filtrando caminos de acuerdo con el tiempo disponible y cantidad de estaciones...")
    paths=controller.filterPathsByTimeAndNumStations(cont,maxTime,minStations)
    print("Preparando el número de alternativas a imprimir")
    paths=controller.preparElementsForPrint(cont,paths,numAnswers)
    print("")
    print("###"*50)
    print("")   
    if lt.size(paths)==0:
        print("No se encontraron resultados")
    else:
        print("Posibles recorridos: ")
        columns=["time","numStations","tourInfo"]
        printTable(paths,columns,True)

# _______________________________________________________________
#  REQUERIMIENTO 3: COMPONENTES FUERTEMENTE CONECTADOS
# _______________________________________________________________

def req3(cont):   
    print("")
    print("###"*50)
    print("")
    print("Calculando componentes conectados")
    controller.searchComponents(cont)
    print("Obteniendo el número de componentes")
    numComponents=controller.getNumComponents(cont)
    print("Obteniendo los vertices de cada componente")
    components=controller.getComponents(cont)
    print("Preparando elementos para imprimir...")
    components=controller.preparComponentsForPrint(cont,components)
    columns=["componentId","numStations","mostStartStation","mostEndStation"]
    print("")
    print("###"*50)
    print("")   
    print("El número de componentes conectados hallados es:",str(numComponents))
    printTable(components,columns,False)

# ___________________________________________________________
#  REQUERIMIENTO 4: RUTA RÁPIDA
# ___________________________________________________________

def req4(cont,startStation,endStation):   # REQUERIMIENTO 4: RUTA RÁPIDA
    print("")
    print("###"*50)
    print("")
    print("Calculando costo de caminos...")
    controller.minimumCostPaths(cont,startStation)
    print("Obteniendo camino mínimo...")
    path=controller.getMinimumPath(cont,endStation)
    print("")
    print("###"*50)
    print("")  
    if path==None:
        print("\nNo se encontraron caminos.")
    else:
        print("Preparando elementos para imprimir...")
        print("\nEl camino mínimo camino es:")
        path=controller.getTimeAndInfoPath(cont,path)
        columns=["time","info"]
        printTable(path,columns,True)

# ___________________________________________________________
#  REQUERIMIENTO 5: RUTAS EN UN RANGO DE FECHAS
# ___________________________________________________________

def req5(cont,startDate,endDate):  
    print("")
    print("###"*50)
    print("")
    print("Identificando los viajes realizados en el rango ...")
    trips,totalTime=controller.getTripsByDate(cont,startDate,endDate)
    print("Identificando las estaciones de origen y llegada más frecuentes ...")
    originStation,destStation=controller.getFrequentStations(trips)
    print("Identificando las horas de inicio y fin más usuales ...")
    mostStartHour,mostEndHour=controller.getFrequentHours(trips)
    print("Preparando elementos para imprimir")
    info={"Date Range":startDate+"\n"+endDate,
          "Total Trips":str(lt.size(trips)),
          "Total Time (h)":str(round(totalTime/3600,2)),
          "Most Frequent \nStart Station":originStation,
          "Most Frequent \nEnd Station":destStation,
          "Most Frequent \nStart Hour":mostStartHour,
          "Most Frequent \nEnd Hour":mostEndHour}
    lst=lt.newList("ARRAY_LIST")
    lt.addLast(lst,info)
    columns=["Date Range","Total Trips","Total Time (h)","Most Frequent \nStart Station","Most Frequent \nEnd Station","Most Frequent \nStart Hour","Most Frequent \nEnd Hour"]
    print("")
    print("###"*50)
    print("")  
    print("\nResultados para viajes entre",startDate,"y",endDate)
    printTable(lst,columns,False)
    

# ___________________________________________________________
#  REQUERIMIENTO 6: INFORMACIÓN DE BICICLETA
# ___________________________________________________________

def req6(cont,bikeId):
    print("")
    print("###"*50)
    print("")  
    print("\nIdentificando los viajes realizados con bicicleta ...")
    trips,numTrips,totalTime=controller.getTripsByBikeId(cont,bikeId)
    print("Identificando las estaciones de origen y llegada más usuales de la bicicleta ...")
    originStation,destStation=controller.getFrequentStations(trips)
    lst=lt.newList("ARRAY_LIST")
    info={"Bike Id":bikeId,
          "Total Trips":numTrips,
          "Total Time (h)":str(round(totalTime/3600,2)),
          "Most Frequent \nStart Station":originStation,
          "Most Frequent \nEnd Station":destStation}
    lt.addLast(lst,info)
    columns=["Bike Id","Total Trips","Total Time (h)","Most Frequent \nStart Station","Most Frequent \nEnd Station"]
    print("")
    print("##"*50)
    print("")  
    print("\nInformación sobre la bicicleta con id",bikeId)
    printTable(lst,columns,False)
# ___________________________________________________
# Ejecución del programa
# ___________________________________________________



def execute(loadInitialMenu):

    while True:
        if loadInitialMenu:
            print("")
            printMenu0()
            inputs = input('Seleccione una opción para continuar\n>')
            print("")
            if int(inputs) == 1:
                print("\nInicializando....")
                cont = controller.init()
            elif int(inputs) == 2:
                loadInitialMenu=False    
                
                optionTwo(cont)
                
        else:
            print("")
            printMenu()
            inputs = input('Seleccione una opción para continuar\n>')
            print("")
            if int(inputs) == 1:
                
                try:
                    req1(cont)
                except:
                    print("")
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
                

            elif int(inputs) == 2:
                print("")
                initialStationName=input("Indique el nombre de la estación de inicio: ")
                maxTime=str(float(input("Indique el tiempo máximo de la ruta (min): "))*60/2)
                minStations=input("Indique la mínima cantidad de estaciones a visitar: ")
                numAnswers=input("Indique el número de alternativas que quiere visualizar: ")
                
                try:  
                    req2(cont,initialStationName,maxTime,minStations,numAnswers)
                except:
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
                

            elif int(inputs) == 3:
                
                try:
                    req3(cont)
                except:
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
            
            elif int(inputs) == 4:
                print("")
                startStation=input("Indique el nombre de la estación de inicio: ")
                endStation=input("Indique el nombre de la estación de destino: ")
                
                try:
                    req4(cont,startStation,endStation)
                except:
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
                

            elif int(inputs) == 5:
                print("")
                startDate=input("Indique la fecha inicial de consulta (MM/DD/AAAA): ")
                endDate=input("Indique la fecha final de consulta (MM/DD/AAAA): ")
                
                try:
                    req5(cont,startDate,endDate)
                except:
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
                

            elif int(inputs) == 6:
                print("")
                bikeId=input("Indique el id de la bicicleta: ")
                
                try:
                    req6(cont,bikeId)
                except:
                    print("\nError. Verifique los parámetros de entrada e intentelo de nuevo.")
                
        
 
        
loadInitialMenu=True
execute(loadInitialMenu)      # :D  .-.  ._.  :)   :(  :o  
