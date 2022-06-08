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
from prettytable import PrettyTable
import datetime
from DISClib.ADT import list as lt
assert cf
import customDfs


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
default_limit= 1000
#sys.setrecursionlimit(default_limit*10)

###################
#Creación catálogo#
###################

def neu_catalogo():
    """
    Llama al controller apra crear un catálogo 
    """
    
    return controller.new_cata()

def asds():
    controller.asds()


##################################
#Obtención de elementos de listas#
##################################
def Primerosx(lista,elemntos):
    """
    Consigue los primeros elementos N de una lista
    """
    return controller.Conseguirelem(lista,elemntos)

def ultimosX(Lista,elem):
    """
    Consigue los primeros elementos N de una lista
    """
    return controller.Conseguirelem(Lista,elem,":P")



#################
#Ejecución menus#
#################

def cargar_csv(catalogo):
    """
    Todos las datos necesarios para ejcutar el menú 1 
    """
    size,bicis,estat= controller.caragar_csv(catalogo)
    
    null= catalogo["model"]["null"]
    graf= catalogo["model"]["grafos"]["dirigido"]
    rep= catalogo["model"]["Repetidos"]
    un,cant_unk= catalogo["model"]["Cant_desconocido"].values()
    grafi= catalogo["model"]["grafos"]["normal"]
    
    
    vertices=graf.vertex 
    arcos= graf.arcos
    arc= grafi.arcos
    vert= grafi.vertex
    last_five= graf.last
    first_five=graf.first 
    normal_f= grafi.first 
    normal_l= grafi.last
    print("Cantidad de bicicletas cargadas: {}. De estaciones: {}".format(bicis,estat))
    print('''\nTotal de datos cargados:{} y de datos no agregados por falta de información {}, datos con auto referencia {}
    La cantidad de rutas que llevan a estaciones desconocidas {} y el número de estaciones desconocidas {} ...         
    '''.format(size,null,rep,un,cant_unk))
    print("_"*50)
    print("-"*50)
    print("Grafo No dirigido")
    print("\nEl numero de vertices {} y el número de arcos {} para el grafo".format(vert,arc))
    
    print("-"*50)
    llaves= ["ID","Nombre","Salidas","Llegadas","Grado (grafo)"]
    
    fst= controller.get_print(normal_l,catalog,"normal")
    lsT= controller.get_print(normal_f,catalog,"normal")
    print("\nPrimeros 5 vertices \n")
    
    PrintList(fst,llaves,llaves)
   
    print("\nUltimoss 5 Vertices \n")
   
    PrintList(lsT,llaves,llaves)
    
    print("-"*50)
    print("Grafo Dirigido")
    print("\nEl numero de vertices {} y el número de arcos {} para el grafo".format(vertices,arcos))
    print("-"*50)
    llaves= ["ID","Nombre","Salidas","Llegadas","Grado Entradas (grafo)","Grado Salidas (grafo)"]
   
    st= controller.get_print(first_five,catalog)
    ts= controller.get_print(last_five,catalog)
    print("\nPrimeros 5 vertices \n")
   
    PrintList(st,llaves,llaves)
   
    print("\nUltimos 5 Vertices \n")
   
    PrintList(ts,llaves,llaves)
   
    
    

def menu2():
    """
    Todos las datos necesarios para ejcutar el menú 2 
    """
    top=catalog["model"]["top"]    
    llaves=["ID","Nombre","Cant-Inicio","Hora Pico","Trips",
            "Fecha Pico","Viajes","Premiun","No Premiun"]
    PrintList(top,llaves,llaves)

def menu3():
    """
    Todos los datos necesarios para ejcutar el menú 3 
    """
    map=catalog["model"]["tabla_general"]
    grafoNoDirigido = catalog["model"]["grafos"]["normal"]
    sirve =False 
    sigue= True 
    while sigue:
        source=input("Ingrese el nombre de la estación de inicio: ")
        if source =="Fad":
           break 
        else: 
         obj=controller.get_Val(map,source)
         if obj: 
           while True: 
            try:
             disponibilidad=input("Ingrese la disponibilidad: ")
             if disponibilidad == "Fad":
                sigue= False 
                break                
             else: 
                disponibilidad=int(disponibilidad)        
            except: 
              print("Es un número _o_")      
            if sigue: 
             try: 
               min_estaciones=input("Ingrese el número mínimo de estaciones: ")
               if min_estaciones == "Fad":
                sigue= False 
                break                 
               else:
                 min_estaciones=int(min_estaciones)   
                 
             except: 
              print("Es un número _o_")      
            if sigue: 
             try: 
               max_rutas=input("Ingrese el máximo número de rutas: ")
               if max_rutas == "Fad":
                sigue= False 
                break                 
               else:
                max_rutas= int(max_rutas)    
                sigue= False 
                sirve= True 
                break
             except: 
              print("Es un número _o_")      
                         
         else: 
           asds() 
           print("No se encontró la estación")     

    if sirve:
     source = (obj.name,obj.id) 
     rutas = controller.dfsss(
        grafoNoDirigido.graf, source, disponibilidad, min_estaciones, max_rutas)
     print('TODAS LAS RUTAS:')
    
     a=0
     for x in rutas:
        a=1
        estat,time,_=x
        prin=lt.newList() 
        for e in estat:
           es,id=e 
           add={"Estacion":es,"Id":id} 
           lt.addLast(prin,add)
        print("Tiempo total de la ruta: ",time)
        PrintList(prin,["Estacion","Id"],["Saltos","Id"])    
        print('-'*10)
     if a == 0:
        asds()
        print("No hay info con esas especificaciones")   
        menu3()
   


def menu4():
    """
    Todos los datos necesarios para ejcutar el menú 4 
    """
    #Falta TODO 
    
    tamaño,dat=catalog["model"]["SCC"]
    llaves=["Componente","Tamaño","Max Out ID","Max Out Name","Out Trips","Max in ID","Max in Name","In Trips"]
    print("-+-"*30)
    print("\n"+" "*20+"Cantidad de SCC: ",tamaño,"\n")
    print("-+-"*30)
    print("\n Información respecto SCC's \n")
    PrintList(dat,llaves,llaves)

def menu5():
    """
    Todos los datos necesarios para ejcutar el menú 5 
    """
    map=catalog["model"]["tabla_general"]
    sirve= False 
    sigue= True 
    while sigue: 
        print("Escoja un estación de inicio para empezar la ruta")
        print("OJO con símbolos especiales y mayúsculas")
        inicio=input("Ingrese un nombre: ")
        if inicio == "Fad":
           break
        else: 
            obj1=controller.get_Val(map,inicio)
            if obj1:
             while True:
                  print("Escoja un estación de fin para la ruta")
                  print("OJO con símbolos especiales y mayúsculas")
                  fin=input("Ingrese un nombre: ")
                  if fin == "Fad":
                      sigue= False
                      break 
                  else: 
                      obj2= controller.get_Val(map,fin)
                      if obj2:
                         sirve= True 
                         sigue= False 
                         break 
                      else: 
                       asds()
                       print("No se encontró esa estación :(")      

            else: 
              asds()
              print("No se encontró esa estación :(") 

    if sirve: 
       base= (obj1.name,obj1.id)
       llegar= (obj2.name,obj2.id) 
       ret= controller.ruta_minima(catalog,base,llegar)
       if ret:  
          size,tiemp,rutas,info,fst,lst=ret
          
          llave_ruta=["Start Id","Start Name","End Id","End Name","Average"] 
          llave_estat=["Id","Name","Out","In","Rush H","Rush D","In degree (grafo)","Out Degree (grafo)"]
          print("="*50)
          print(" "*+15,"La primera estación:"," "*15) 
          print("="*50,"\n")  
          PrintList(fst,llave_estat,llave_estat)
          print("\n","="*50)
          print(" "*+15,"La última estación:"," "*15) 
          print("="*50,"\n")  
          PrintList(lst,llave_estat,llave_estat)
          
          print("\n","/---\---"*10,"/---\-")
          print("El total de paradas: {} ".format(size+1))
          print("El total de 'rutas': {}".format(size))
          print("El total de tiempo: {}".format(tiemp))
          print("/---\---"*10,"/---\-","\n")
          print("Detalles de la ruta: \n")
          PrintList(rutas,llave_ruta,llave_ruta) 
          print("+---+"*15,"\n")
          print("Detalles de las estaciones: \n")
          PrintList(info,llave_estat,llave_estat)
           

          
       else:
          asds() 
          print("No se encontró ruta alguna entre las dos estaciones")  
          menu5()  


def menu6():
    """
    Todos los datos necesarios para ejcutar el menú 6 
    """
    rutas=catalog["model"]["Premium_routes"]
    rango=rutas.range
    max= rutas.max
    min= rutas.low
    sirve= False 
    sigue= True
    now= datetime.datetime.utcnow()
    while sigue:
        print("Fecha mayor: {} , Fecha menor {} .".format(max,min))
        print("Utilice el formato “MM/DD/AAAA” profa ")
        print("Salir: Fad")
        date=input("Escoja una fecha mayor: " )
        if date == "Fad":
            break
        else: 
         try: 
           date= datetime.datetime.strptime(date,"%m/%d/%Y")    
           while True: 
            print("Utilice el formato “MM/DD/AAAA” profa ")
            date2=input("Escoja una fecha menor: ")
            if date2== "Fad":
                sigue= False 
                break
            try:
             date2= datetime.datetime.strptime(date2,"%m/%d/%Y")    
             
             if date2 > date:
                 mayor= date2
                 menor=date
             else: 
                 mayor= date
                 menor= date2    

             sigue= False 
             
             sirve= True
             break
                                                
            except:
               
             asds()
             print("Ese no es el formato.... _o_")     
                   
         except: 
          
           asds()
           print("Ese no es el formato.... _-_")     
   
    if sirve:
     all= rutas.get_range(mayor,menor)
     if all:
      llaves=["Total Viajes","Tiempo Total",
            "Org Común","Fin Común","Hora Ini","Hora Fin"]
      PrintList(all,llaves,llaves)
     else: 
         asds()
         print("No encontramos fechas en ese rango :( ")
         menu6()

def menu7():
    """
    Todos los datos necesarios para ejcutar el menú 7 
    """
    obj= catalog["model"]["Bicis"]
    mapa=obj.mapa
    sirve= False
    while True:
        print("Ingrese un identificador para la cicla:")
        id= input("ID: ")
        if id == "Fad":
           break     
        else: 
         try: 
           cicla=controller.get_Val(mapa,id) 
           if obj: 
              sirve= True
              break 
           else: 
               print("O no! \nNo está :O") 
         except:
           asds() 
           print("Como es que lo haces fallar :/ \n \n") 

    if sirve: 
       obj.count_Start(cicla)
       obj.count_end(cicla)
       cicla["Horas"]=round(cicla["Segundos"]/3600,2)
       prin=lt.newList()
       lt.addFirst(prin,cicla) 
       llaves= ["ID","Viajes","Segundos","Horas","Inicio","Cant_inicio","Fin","Cant_fin"]
       PrintList(prin,llaves,llaves)


def menu8():
    """
    Todos los datos necesarios para ejecutar el menú 8 
    """
    sirve= False 
    sigue =True
    dos= True
    map=catalog["model"]["tabla_general"]
    while sigue: 
        print("Ojo con las mayusculas y singos especiales")
        estat= input("Ingrese el nombre de la estación: ")
        if estat== "Fad":
         break
        else: 
         esacion=controller.get_Val(map,estat)
         if esacion:
           if not esacion.ready:
              esacion.load_hours()   
           up,down=esacion.limits 
           while dos: 
            print("EL rango de fechas disponible es desde {} , hasta {}".format(up,down))
            print("Salir: Fad")
            print("Utilice el formato “MM/DD/AAAA HH:MM” profa ")
            date=input("Escoja una fecha mayor: " )
            if date == "Fad":
             sigue =False 
             break
            else: 
             try: 
              date= datetime.datetime.strptime(date,"%m/%d/%Y %H:%M")    
              while True: 
               print("Utilice el formato “MM/DD/AAAA HH:MM” profa ")
               date2=input("Escoja una fecha menor: ")
               if date2== "Fad":
                 sigue= False 
                 dos= False 
                 break
               try :
                date2= datetime.datetime.strptime(date2,"%m/%d/%Y %H:%M")    
             
                if date2 > date:
                  mayor= date2
                  menor=date
                else: 
                  mayor= date
                  menor= date2    
                dos= False 
                sigue= False 
             
                sirve= True
                break
                                                
               except:
               
                asds()
                print("Ese no es el formato.... _o_")     
                   
             except: 
          
              asds()
              print("Ese no es el formato.... _-_")
         else: 
            asds()
            print("No encontramos esa estación. \n\n") 
    if sirve: 
       lista= controller.info_estat(esacion,mayor,menor) 
      
       if lista:  
        llaves= ["Total inicio","Canitad fin","Viaje Tiempo Mayor","Mayor estación fin"] 
        PrintList(lista,llaves,llaves) 
       else: 
         asds()
         print("No encontramos información dentro de es rango de fechas \n \n")
         menu8()


############
#Print Menú#
############

def PrintList(lista,valores,llaves):
    """
    Imprime unalista, idealmente una sublista.
    Valores: referencia al nombre de las llaves a coneguir para conseguir los valores
    Llaves:  El nombre con el cual van a salir impresos los valores
    """
    x= len(valores)
    y= len(llaves)

    if x == y:
         
        table= PrettyTable()
        
        table.field_names=llaves
        for i in lt.iterator(lista):
            agregar= []
            for j in valores:
                car= i[j]
                if car is None:
                   car= "Ni idea ¯\_(ツ)_/¯ " 
                agregar.append(car)
            table.add_row(agregar)
        table.max_width=20
        print(table)         
    else: 
      print("No hay el mismo numero de llaves y valores, _-_")
      1/0 

def PrintList_Obj(lista,llaves):
    """
    Imprime unalista, idealmente una sublista, pero los valores son objectos.
    Atributos: referencia al nombre de los atributos a  coneguir para conseguir los datos
    Llaves:  El nombre con el cual van a salir impresos los valores
    """
    table= PrettyTable()
    table.field_names=llaves
    
    for i in lt.iterator(lista):
        
        agregar= [i.id,i.name,i.start,i.end]
         
        table.add_row(agregar)
    
    table.max_width=20
    print(table)         
   
def printMenu():
    print("-"*75)
    print(" "*30,"Bienvenido")
    print("-"*75)
    print("\n")
    print("#"*75)
    print("1- Cargar información en el catálogo")
    print("2- REQ. 1: Comprar bicicletas para las estaciones con más viajes de origen ")
    print("3- REQ. 2: Planear paseos turísticos por la ciudad ")
    print("4- REQ. 3: Reconocer los componentes fuertemente conectados ")
    print("5- REQ. 4: Planear una ruta rápida para el usuario ")
    print("6- REQ. 5: Reportar rutas en un rango de fechas para los usuarios anuales.")
    print("7- REQ. 6: Planear el mantenimiento preventivo de bicicletas ")
    print("8- REQ  7: La estación más frecuentada por los visitantes ")
    print("0- Salir")
    print("#"*75,"\n")

catalog = neu_catalogo()

"""
Menu principal
"""
carga= False 
while True:
    printMenu()

    inputs = input('Seleccione una opción para continuar\n')
    val=["1","2","3","4","5","6","7","8","0"]
    if inputs in val:
     if int(inputs[0]) == 1:
       if not carga:  
        print("Cargando información de los archivos ....")
        cargar_csv(catalog)
        carga= True
     else:
      if inputs == "0":
          break
      else:
       
       if carga:    
       
        if int(inputs[0]) == 2:
         menu2()
        else: 
       
           if inputs == "3":
               menu3()
           else: 
       
               if inputs == "4":
                   menu4()
               else: 
       
                    if inputs == "5":
                        menu5()
                    else: 
       
                        if inputs == "6":
                            menu6()
                        else: 
       
                            if inputs == "7":
                                menu7()    
                            else: 
                                if inputs== "8":
                                    menu8()
       else:
          print("Carga los datos antes de-.") 
    else:
        print("Escoja una opción valida... ")
sys.exit(0)

sys.exit(0)
