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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from time import time
from App.controller import get_Val
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack as stk

from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mrg

from DISClib.Algorithms.Graphs import bfs,dfo,dfs,scc,prim
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bll
from DISClib.Algorithms.Graphs import cycles as cl


import customDfs
from Docs import Doc as asdf
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
##########################
# Construccion del modelo#
##########################

class estaciones: 
    """
    Clase que hace referencia a los vertices de los arcos, 
    contiene toda la información y opciones que se requieran los vertices 
    """
    def __init__(self,_Id,_Name,) -> None:
        self.id=  float(_Id)     #Es la id, no unica de las estaciones
        self.smart= "- SMART" in _Name 
        self.name=_Name     #Es le nombre, teoricamente único
        self.start=0        #Cuantos empiezan 
        self.finish=0       #Cuantos Terminan wow
        self.date= {"Hora":{},"Dia":{}}  #Datos prelimnares apra encotnrar las horas y fechas pico
        self.hpico= {"Hora":None,"Cant":0} #Hora pico
        self.dpico= {"Dia":None,"Cant":0}   #Dia pico en la estacion
        self.long= {"Len":0,"Estation":None} #Viaje más largo de salida ?      
       
        #Arboles para cargar rango de fechas
        self.hour= {"llegadas":om.newMap("RBT",cmp_fechas), 
                    "Salidas":om.newMap("RBT",cmp_fechas)}
        self.ready= False 
        self.user= {"Annual Member":0,"Casual Member":0}#Cantidad de viajes por tipo de ususario
        
        #Mapas, lista o estructuras para después cargar el arbol
        """
        self.map_hour= {"llegadas": mp.newMap(numelements=6000,
                                    comparefunction=cmp_maps,
                                    maptype="PROBING"),
                        "Salidas":mp.newMap(numelements=6000,
                                    comparefunction=cmp_maps,
                                    maptype="PROBING")}
        Carga segura, pero muyyy lenta 
        """
        self.list_hour={"llegadas": lt.newList(),"Salidas":lt.newList()}
        
        self.limits= None 
        #self.end= mp.newMap(maptype="PROBING",
        #                   numelements=621,
        #                  comparefunction= cmp_maps)
        #self.max= {"Length":-1}
        
    def ini(self,hour,date) -> None :
        """
        Añade uno a las veces que la estación es de salida
        """
        self.start +=1

        recorrer= [("Hora",hour),("Dia",date)]
        for llave,tiempo in  recorrer: 
         dat=self.date[llave].get(tiempo)
         if dat:
           dat+=1
         else:
           dat= 1
         self.date[llave][tiempo]= dat         

    def max_hour(self):
        """
        Carga los picos en las horas
        """
        info=self.hpico
        base= info["Cant"]
        for hora,cant in self.date["Hora"].items():
           if cant > base: 
               info["Hora"]= datetime.datetime.strftime(hora,"%H:%M")  
               info["Cant"]= cant
               base= cant 
           if cant == base : 
               info["Hora"]= info["Hora"]+ " &/ "+ datetime.datetime.strftime(hora,"%H:%M")
        
        self.hpico= info

    def max_date(self):
        """
        Carga los picos en las fechas
        """
        info=self.dpico
        base= info["Cant"]
        for hora,cant in self.date["Dia"].items():
          
           if cant > base: 
               info["Dia"]= datetime.datetime.strftime(hora,"%m/%d/%Y")  
               info["Cant"]= cant
               base= cant
           if cant == base : 
               info["Dia"]= info["Dia"] + " &/ " + datetime.datetime.strftime(hora,"%m/%d/%Y") 

        self.dpico= info


    def fin(self) -> None :
        """
        Añade uno a las veces que la estación es de entrada
        """
        self.finish +=1

    def client(self,type) -> None :
        """
        Añade el tipo de clientes que pasan por la estación y la cantidad
        """  
        val=self.user.get(type)
        if val: 
            self.user[type] += 1
        else: 
            self.user[type] = 1    
    
    def arrive(self,hour) -> None :
        """
        Añade información respecto las horas que llegan viajes 
        """ 
        lt.addLast(self.list_hour["llegadas"],hour)
        
    def left (self,hour,estat,trip,id) -> None: 
        """
        Añade información por la hora que salen los viajes        
        """
        add={"hora":hour,"fin":estat,"Len":trip,"Id":id}
        
        lt.addLast(self.list_hour["Salidas"],add)
    
    def load_hours(self):
        """
        Carga los arboles a partir de las listas
        armadas en la carga de datos, 
        se ejectua individualmente por estación
        """
        llegar=self.list_hour["llegadas"]
        arbol1=self.hour["llegadas"]
        salir=self.list_hour["Salidas"]
        arbol2=self.hour["Salidas"]
        
        if not lt.isEmpty(llegar):   
         for hour in lt.iterator(llegar):
            cant= getval_arb(arbol1,hour)
            if cant: 
               cant+= 1
            else:
               cant= 1 
            om.put(arbol1,hour,cant)     

        if not lt.isEmpty(salir):
         for info in lt.iterator(salir):
            hora=info["hora"]
            estat=info["fin"]
            leng=info["Len"]
            id=info["Id"]
            datos= getval_arb(arbol2,hora)
            if datos:
               datos["Cant"]+= 1
               di= datos["estaciones"]
               if estat in di:
                  di[estat]+= 1
               else: 
                  di[estat] = 1     
               if datos["trips"]["Len"] < leng:
                  datos["trips"]["Len"] = leng
                  datos["trips"]["Trip"]= id  
            else: 
               largo={"Len":leng,"Trip":id}
               datos={"estaciones":{estat:1},
               "trips":largo,"Cant":1}          
            om.put(arbol2,hora,datos)
        
        self.hour["llegadas"]= arbol1
        self.hour["Salidas"]= arbol2 
        self.ready= True      
        mayor= max([om.maxKey(self.hour["llegadas"]),om.maxKey(self.hour["Salidas"])])     
        menor= min([om.minKey(self.hour["llegadas"]),om.minKey(self.hour["Salidas"])])
        
        self.limits= (mayor,menor)
        

    def get_range(self,up,down):             
        """
        Consigue el rango y el máximo len y fecha de todo :)
        """
        a=1
        b=1
        arbol=self.hour["llegadas"]
        left= self.hour["Salidas"]
        vals= om.values(left,down,up)
        valores= om.values(arbol,down,up)
        if not lt.isEmpty(vals) and not lt.isEmpty(valores): 
         arrive= 0 
         for i in lt.iterator(valores):
            arrive += i
     
         est_max= {"Estacion":None,"Cant":0}
         cant_total= 0 
         long_len={"Id":None,"Len":0}
         
         for i in lt.iterator(vals):
             info=i["trips"]
             cant_total += i["Cant"]   
             estacione=i["estaciones"] 
             for estat,cant in estacione.items():    
                
                if cant > est_max["Cant"]:
                   est_max["Cant"]= cant 
                   est_max["Estacion"]= estat
                   b= 1 
                else:
                 if cant == est_max["Cant"]:
                   if len(est_max["Estacion"]) < 300:
                     est_max["Estacion"]= estat + " &y " + est_max["Estacion"]   
                   else:
                    if b == 1: 
                     b= 2      
                     est_max["Estacion"]= est_max["Estacion"] + " y muchos mas..."   
           
             if info["Len"]> long_len["Len"]:
                long_len["Len"]=info["Len"]
                long_len["Id"]=info["Trip"]
                a=1 
             else:
              if info["Len"]== long_len["Len"]:
                if len(long_len["Id"]) < 300:
                 long_len["Id"]=info["Trip"] +" &y "+ long_len["Id"] 
                 
                else:
                 if a==1:    
                  long_len["Id"]=long_len["Id"] + " y muchos más..."
                  a= 2  
         return arrive,est_max,long_len,cant_total              
        else: 
         return None    
   
    """ #Creo que no tiene utilidad, pero no la borro del todo 
    def add_dest(self,dest,length,id,type) -> None:
        
        Añade información respecto los destinos
        
        map=self.end
        info=getVal(map,dest)
        if info: 
            info["Cant"]+=1
            info["Duration"]=(info["Duration"] + length)/2  

        else:    
           info= {"Cant":1,"Duration":length} 
        mp.put(map,dest,info)
        if self.max["Length"] < length :
            self.max= {"Destiny":dest,"Length":length,
                       "Id":id,"type":type}
    """

class Grafos: 
    """
    Acorta las operaciones para los grafos
    """
    def __init__(self,_size,_direct=True,_type="ADJ_LIST") -> None:
        """
        Inicializa el grafo con valores predeterminados, menos el tamaño
        """
        self.graf= gp.newGraph(_type,_direct,_size,cmp_grafos)
        self.last= None
        self.first= None
        self.type= _direct

    def count (self):
        """
        Cuenta el número de vertices y arcos
        """
        self.vertex= gp.numVertices(self.graf)
        self.arcos= gp.numEdges(self.graf)

    def put(self,vertex):
        """
        Agrega un vertice
        """
        if not gp.containsVertex(self.graf,vertex):
         gp.insertVertex(self.graf,vertex)

    def conect(self,a,b,cost=1):
        """
        Crea una conexión entre dos vertices
        """  
        gp.addEdge(self.graf,a,b,cost)


    def values(self):
        """
        Carga a una lista los 5 ultimos vertices 
        
        """
        lista= gp.vertices(self.graf)
        if not lt.isEmpty(lista) : 
         self.last =lt.subList(lista,lt.size(lista)-5,5)
         self.first=lt.subList(lista,1,5) 
    
    def degree (self,vertex):
        """
        Consigue el indegree y out degree de un grafo 
        """
        if self.type:
         return gp.indegree(self.graf,vertex),gp.outdegree(self.graf,vertex)
        else: 
         return gp.degree(self.graf,vertex)   

class ciclas: 
    """
    Clase que hace referencia a las bicicletas usadas en los viajes
    """
    def __init__(self) -> None:
        
        self.mapa= mp.newMap(numelements=10000,loadfactor= 5,comparefunction= cmp_maps)   
        

    def size(self):
        """
        Consigue la cantidad de bicicletas 
        """
        return mp.size(self.mapa)

    def create(self,id,duration,end,start):
        """
        Crea o añade la información 
        de bicicletas a un mapa 
        """
        cicla=getVal(self.mapa,id)
        if cicla:
         cicla["Segundos"]+= duration 
         cicla["Viajes"]+= 1
         lt.addLast(cicla["End"],end)
         lt.addLast(cicla["Start"],start)    
        else: 
         cicla={"ID":id,"Segundos":duration,"Viajes" :1,
                "Inicio":None,"Cant_inicio":0,
                "Fin":None,"Cant_fin":0,
                "End":lt.newList(),"Start":lt.newList()}
        
         lt.addLast(cicla["End"],end)
         lt.addLast(cicla["Start"],start)
        
        mp.put(self.mapa,id,cicla)        
              
    
    
    def count_Start(self,cicla):
        """
        Cuenta las estaciones más frecuentes de llegada
        a partir de un diccionario que ya le mandaron
        """
        if cicla["Inicio"] is None:   
         estat={}
         estacion={"Nom":None,"Cant":-1}
               
         for est in lt.iterator(cicla["Start"]):
            if est in estat:
             estat[est]+=1
            else: 
             estat[est]=1
        
         for nom,cant in estat.items():
            if estacion["Cant"] < cant:
               estacion["Cant"] = cant 
               estacion["Nom"]  = nom 
               a=1            
            else: 
             if estacion["Cant"] == cant:              
                if len(estacion["Nom"]) < 300:
                    estacion["Nom"]= estacion["Nom"] +" &y "+ nom 
                else: 
                   if a==1:
                    a=2
                    estacion["Nom"]= estacion["Nom"] +" y muchas más " 

        
         cicla["Inicio"]=estacion["Nom"]
         cicla["Cant_inicio"]= estacion["Cant"]
        

    def count_end(self,cicla):
        """
        Cuenta las estaciones más frecuentes de salida
        """   
        if cicla["Fin"] is None:   
         estat={}
         estacion={"Nom":None,"Cant":-1}
        
        
         for est in lt.iterator(cicla["End"]):
            if est in estat:
             estat[est]+=1
            else: 
             estat[est]=1
        
        for nom,cant in estat.items():
            if estacion["Cant"] < cant:
               estacion["Cant"] = cant 
               estacion["Nom"]  = nom 
               a=1            
            else: 
             if estacion["Cant"] == cant:              
                if len(estacion["Nom"]) < 300:
                    estacion["Nom"]= estacion["Nom"] +" &y "+ nom 
                else: 
                   if a==1:
                    a=2
                    estacion["Nom"]= estacion["Nom"] +" y muchas más " 

        cicla["Fin"]= estacion["Nom"]
        cicla["Cant_fin"]=estacion["Cant"]
   


class anual_routes:
    """
    Clase especifica para el requerimeinto 5 que tiene en cuenta las rutas
    """
    def __init__(self) -> None:
        self.map= mp.newMap(maptype="PROBING",numelements=370,comparefunction=cmp_maps)
        self.arb= om.newMap("RBT",cmp_fechas)
        self.range= None
        self.max= None
        self.low= None  
           
    def add_hour(self,date,hour,end,origen,dest,len):
        """
        Añade la fecha, pero solo 
        la parte del mes a la tabla para después armar un arbol
        """
        map=self.map
        key= date
        hora= hour
        arrive= end
        
        info= getVal(map,key)
        if info: 
        
              info["Cant"]+=1
              info["Len"] +=int(len) 
              val= ["Origen","Destino","inicio","fin"]
              lla=[origen,dest,hora,arrive]

              for keya,val in zip(val,lla):
                  ad = info[keya].get(val,0)
                  ad+= 1
                  info[keya][val]=ad  
        else: 
            info= {"Cant":1,"Len":int(len),
                   "Origen":{origen:1},
                   "Destino":{dest:1},
                   "inicio":{hora:1},"fin":{arrive:1}}
        
        mp.put(map,key,info)

    def load_tree(self):
        """
        Carga el arbol para después encontrar el rango
        """
        map=self.map
        arb= self.arb
        for i in lt.iterator(mp.keySet(map)):
            add= getVal(map,i)
            om.put(arb,i,add) 
        
    def max_min(self):
        """
        Ya después de cargar el arbol consige el mayor y menor
        """
        if not om.isEmpty(self.arb):
           now= datetime.datetime.utcnow().date()
           grater= om.maxKey(self.arb)
           lower=  om.minKey(self.arb)
           self.max= grater
           self.low= lower 

    def get_range(self,ma,mi):
        """
        Consigue el rango y consigue lo deaseado de estos es decir:
        • El total de viajes realizados.
        • El total de tiempo invertido en los viajes.
        • La estación de origen más frecuentada.
        • La estación de destino más utilizada.
        • La hora del día en la que más viajes inician 
        • La hora del día en la que más viajes terminan  
        """ 
        run= om.values(self.arb,mi,ma)
        vacio= lt.isEmpty(run)
        if not vacio:
         total= 0 
         ime= 0 
         origin= {"Origen":{},
                  "Destino":{},
                  "inicio":{},
                  "fin":{}}
         get= ["Origen","Destino","inicio","fin"]    
         for info in lt.iterator(run):
             total += info["Cant"] 
             ime   += info["Len"]
             for valor in get: 
              for nom,cant in info[valor].items(): 
                can= origin[valor].get(nom)
                if can:
                   origin[valor][nom]+= cant
                else: 
                   origin[valor][nom] = cant   
         valo=["Org Común","Fin Común","Hora Ini","Hora Fin"]
         add={"Total Viajes":total,"Tiempo Total":ime}
         for cantidades,val in zip(origin.values(),valo):
            base= 0 
            for estat,num in cantidades.items():
               if type(estat) is not int and type(estat) is not str :
                  estat= datetime.datetime.strftime(estat,"%H:%M") 
               if num == base: 
                   add[val]= estat + " y " +add[val] 
               if num > base:
                   add[val]= estat + " con: "+ str(num) 
                   base= num
               
        
         ret=lt.newList()
              
         lt.addFirst(ret,add)
        else: 
           ret= None 
        return ret 

########################################################################################################################
################################################Inicio del catálogo#####################################################
########################################################################################################################

def new_catalog():
    """
    Crea un catálogo vacío 
    """

    catalog={ "bikes_lista" :None ,
              "tabla_general": None,
              "null": 0,
              "Repetidos":0,
              "conexiones":None,
              "grafos":{"dirigido":None,"normal":None},
              "Bicis":ciclas(),
              "Premium_routes":anual_routes(),
              "Desconocido":{},
              "SCC":None,
              "top":None,
              "Cant_desconocido":{"Rutas":0,"Estaciones":0}}

    #Creación lista base para todos los datos 
    catalog["bikes_lista"]= lt.newList("SINGLE_LINKED",cmp_lista)
    #Tabla de Id 
    catalog["tabla_general"]=mp.newMap(maptype="PROBING",numelements=750,comparefunction=cmp_maps)
    #Creación grafo 
    catalog["conexiones"]= mp.newMap(maptype="PROBING",numelements=20000,comparefunction=cmp_maps)

    
    
    return catalog

#################################################
# Funciones para agregar informacion al catalogo#
#################################################

def add_datos(catalogo,ruta):
    """
    Añade la ruta a los datos deseados
    """
    limpio= limpiar(ruta,catalogo)
    if limpio:  
    
     lista= catalogo["bikes_lista"]
     create_stops(ruta,catalogo)
     
     lt.addLast(lista,ruta)
    
    else:
      if limpio is None: 
       catalogo["null"]= catalogo["null"]+1
      else:  
       catalogo["Repetidos"]=catalogo["Repetidos"] +1 

    return "ʕಠ ͟ʖಠʔ"

def add_datos2(catalogo):
    """
    Añade los datos parte 2
    """
    lista=catalogo["bikes_lista"]
    for ruta in lt.iterator(lista): 
     add_ciclas(ruta,catalogo)
     routes(ruta,catalogo)
    
    return "ᗒ ͟ʖᗕ"  
###################################
# Funciones para creacion de datos#
###################################

def create_stops(ruta,catalogo):
    """
    Crea el objeto de las estaciones
    """
    
    map= catalogo["tabla_general"]
    conec= catalogo["conexiones"]
    objs=()
    duracion= int(ruta["Trip  Duration"])
    viaje= ruta["Trip Id"]
    user= ruta["User Type"]

    
    for i in ["Start", "End"]:
      
        name=ruta[i + " Station Name"]
        id= ruta[i + " Station Id"]
        tiempo= datetime.datetime.strptime(ruta[i + " Time"],"%m/%d/%Y %H:%M")
        dia,hora=ruta[i + " Time"].split(" ")
        
        dia= datetime.datetime.strptime(dia,"%m/%d/%Y") 
        hora=datetime.datetime.strptime(hora,"%H:%M")
       
        estat=getVal(map,name)
        if estat is None: 
            estat= estaciones(id,name)
           
        if i == "Start":  
             estat.ini(hora,dia)  
             estat.client(user)
             if user == "Casual Member":          #estat.add_dest(ruta["End Station Id"],duracion,viaje,user)      
              estat.left(tiempo,ruta["End Station Name"],duracion,viaje)   
                        
        else: 
             estat.fin()
             if user == "Casual Member":          #estat.add_dest(ruta["End Station Id"],duracion,viaje,user)      
              estat.arrive(tiempo) 
        
        objs=objs + (estat,)    
        mp.put(map,name,estat)
   
    obj1,obj2= objs
    add=((obj1.name,obj1.id),(obj2.name,obj2.id))
  
    prom=getVal(conec,add)
    if prom:
       prom["total"]+=1
       prom["Viajes total"]+= duracion 
       prom["promedio"]= ( prom["Viajes total"] ) / prom["total"]
    else: 
       prom= {"Estación A":obj1,"Estación B":obj2,"total":1,"Viajes total":duracion,"promedio":int(duracion)}
    
    mp.put(conec,add,prom)
   
    return "⤜(⪧ ³⪦)⤏"

def routes(ruta,catalogo):
    """
    Añade información respecto 
    las rutas de los usuarios de sus anual
    """
    if  ruta["User Type"] == "Annual Member":
        obj=   catalogo["Premium_routes"]
        ini,ed= ruta["Start Time"].split(" ")
        hour=  datetime.datetime.strptime(ed,"%H:%M") 
        date= datetime.datetime.strptime(ini,"%m/%d/%Y") 

        _,fin= ruta["End Time"].split(" ")
        end=   datetime.datetime.strptime(fin,"%H:%M") 
        origen=ruta["Start Station Name"]
        dest=  ruta["End Station Name"]
        len=   ruta["Trip  Duration"]
        obj.add_hour(date,hour,end,origen,dest,len)
   
    return "╭∩╮(ʘᗝʘ)╭∩╮"

def add_ciclas(ruta,catalogo):
    """
    Añade la información en relación a las bicicletas     
    """
    id= ruta["Bike Id"].replace(".0","")
    start=ruta["Start Station Name"]
    end= ruta["End Station Name"]
    duration= int(ruta["Trip  Duration"])
    obj= catalogo["Bicis"]
    
    obj.create(id,duration,end,start)

    return "(づóᗝò)づ"
          

def cargar_grafos(catalogo):
    """
    recore el mapa de conexiones y crea los grafos necesarios.....    
    """
    conections=catalogo["conexiones"]
    size=Size_tabla(conections)
    
    grafos=catalogo["grafos"]
    dirigido=Grafos(size)
    normal=  Grafos(size,False)
    
    for vertexs in lt.iterator(mp.valueSet(conections)):
     
     est1=vertexs["Estación A"]   
     est2=vertexs["Estación B"]
     cost=vertexs["promedio"]

     normal.put((est1.name,est1.id)) 
     normal.put((est2.name,est2.id)) 
     
     dirigido.put((est1.name,est1.id))
     dirigido.put((est2.name,est2.id))
     
     dirigido.conect((est1.name,est1.id),(est2.name,est2.id),cost)

    
    done= {}
    
    for vertex in lt.iterator(mp.keySet(conections)):
     b,a= vertex 
     vertexs=getVal(conections,(a,b))
     vete= getVal(conections,(b,a))
     if  vete and vertexs : 
       
       if (b,a) not in done  and (a,b) not in done: 
             
        cost1=vete["total"] 
        cost0=vertexs["total"]
        total1= vertexs["Viajes total"]
        total= vete["Viajes total"]
        est1=vertexs["Estación A"]   
        est2=vertexs["Estación B"]   
     
        cost= (total1 + total)/(cost1 + cost0)  
     
        normal.conect((est1.name,est1.id),(est2.name,est2.id),cost)       
        done[(a,b)]= (a,b)
        done[(b,a)]= (a,b) 

    dirigido.count()
    normal.count()
    dirigido.values()
    normal.values()

    grafos["dirigido"]=dirigido
    grafos["normal"]= normal
    
    return "ヽ(ཀ ͟ʖཀ)ﾉ"

###############
#Limpiar Datos#
###############

def limpiar(ruta,catalogo):
    """
    Limpia todos los datos
    """
    if ruta["End Station Name"] == "":
           ruta["End Station Name"]= clean_unknown(ruta["End Station Id"],catalogo)
            
    if ruta["Start Station Name"]== "":
           ruta["Start Station Name"]= clean_unknown(ruta["Start Station Id"],catalogo)
           
    copy= ruta.copy()
    
    del copy["Start Station Name"]
    del copy["End Station Name"] 
    
    if  "" in list(copy.values()) or "0" in list(ruta.values() ):
        return None
        
    else: 
        if ruta["End Station Name"] == ruta["Start Station Name"]:
           return False 
    return True 

def clean_unknown(id,catalogo):
    """
    Limpia los desconocuidos 
    agregandole números dependiendo de la ID
    """
    
    catalogo["Cant_desconocido"]["Rutas"] += 1
      
    mirar= catalogo["Desconocido"]
    name= mirar.get(id)
    
    if name is None : 
    
       num= len(mirar)
       name= "Unknown "+ str(num) 
       catalogo["Desconocido"][id]=name    
       catalogo["Cant_desconocido"]["Estaciones"] += 1

    
    return name 

###########
#Pre loads#
###########


def load_visitadas(catalogo):
    """
    Carga las 5 estaciones más visitadas y ya
    """
    lista= mp.valueSet(catalogo["tabla_general"])
    order= merge_sort(lista,cmp_ord)
    run= lt.subList(order,1,5)
    top= lt.newList()
    for obj in lt.iterator(run):
#Sé que está largo pero no puedo hacer un recorrido cambindo los metodos, creo...
        add={}
        obj.max_hour()
        obj.max_date()
        add["ID"]=obj.id
        add["Nombre"]=obj.name
        add["Cant-Inicio"]=obj.start
        pro,no=obj.user.values()
        our,cant= obj.hpico.values()
        date,qant=obj.dpico.values()
        add["Premiun"]= pro
        add["No Premiun"]= no
        add["Hora Pico"]= our
        add["Trips"]=cant
        add["Fecha Pico"]= date
        add["Viajes"]= qant

        lt.addLast(top,add)

    catalogo["top"]= top

def componentes_scc(catalogo):
    """
    Retorna los componentes fuertemente conectados    
    """  
    graf=catalogo["grafos"]["dirigido"].graf
    dic= scc.KosarajuSCC(graf)
    cant= dic["components"]
    map=dic["idscc"]
    components={}
    for llave,val in zip(lt.iterator(mp.keySet(map)),lt.iterator(mp.valueSet(map))):
        if not  val in components: 
           components[val]=lt.newList() 
        lt.addLast(components[val],llave)
    ret=lt.newList()
    estaciones= catalogo["tabla_general"]
    for componente,lista in components.items():
        add={"Componente":componente,
        "Tamaño":lt.size(lista),"Max Out ID":None,"Max Out Name":None,"Out Trips":0,"Max in ID":None,"Max in Name":None,"In Trips":0}
        for estat in lt.iterator(lista):
            nom,id=estat
            obj=getVal(estaciones,nom)
            salir=obj.start    
            if salir >0:
             if salir > add["Out Trips"]:
                add["Max Out ID"]= str(id) 
                add["Max Out Name"]= nom
                add["Out Trips"]= salir   
             else: 
              if salir == add["Out Trips"]:
                add["Max Out ID"]= add["Max Out ID"]+ " y " +str(id) 
                add["Max Out Name"]= add["Max Out Name"] + " y " +nom
            fin=obj.finish   
            if fin >0: 
             if fin > add["In Trips"]:
                add["Max in ID"]= str(id) 
                add["Max in Name"]= nom 
                add["In Trips"]=fin  
             else:   
              if salir == add["In Trips"]:
                add["Max in ID"]= add["Max in ID"]+ " y " +str(id) 
                add["Max in Name"]= add["Max in Name"] + " y " +nom
        lt.addLast(ret,add)    
    ret=merge_sort(ret,cmp_scc)
    catalogo["SCC"]= (cant,ret)

def look_routes(graf,source, disponibilidad, min_estaciones, max_rutas):
    """
    Busca las rutas desde una estacion 
    y una disponibilidad de tiempo
    y una cantidad maxima
    """
    return customDfs.obtenerRutas(graf,source, disponibilidad, min_estaciones, max_rutas)




def shortest_path(catalogo,end,start):
    """
    Busca el camino más corto entre dos estaciones
    """    
    grafo= catalogo["model"]["grafos"]["dirigido"]
    graf=grafo.graf
    busqueda=djk.Dijkstra(graf,start)
    
    if djk.hasPathTo(busqueda,end):
       nam_init,_=start
       nam_fin,_ =end 
       map=catalogo["model"]["tabla_general"]
       total_time= 0 

       objs  = lt.newList()
       obj_i = getVal(map,nam_init)
       obj_l = getVal(map,nam_fin)

       path  = djk.pathTo(busqueda,end)
       size  = stk.size(path)
       routes= lt.newList()
       while not(stk.isEmpty(path)):
         estat= stk.pop(path)
         namea,ida=estat["vertexA"]
         nameb,idb=estat["vertexB"]
         total_time+= estat["weight"]
         add={"Start Id":ida,
              "Start Name":namea,"End Id":idb,
              "End Name":nameb,"Average":estat["weight"]}
         lt.addLast(routes,add) 
         if nameb != nam_fin:
            obj= getVal(map,nameb)
            lt.addLast(objs,obj)
      
       lt.addFirst(objs,obj_i)
       lt.addLast(objs,obj_l)
       info=lt.newList()
       fst=lt.newList()
       lst=lt.newList()
       s= lt.size(objs)
       #Buscar como concatenar
       for ob in lt.iterator(objs):
           ob.max_hour()
           ob.max_date()
           nam=ob.name
           id= ob.id
           out=ob.start
           fin=ob.finish
           a1 =ob.hpico["Hora"]
           a2 =ob.dpico["Dia"]
           if len(a1) > 114:
              a1=a1[:114]+"..."
           if len(a2) > 114: 
              a2= a2[:114]+"..."

           rush_h= a1 + " con: " + str(ob.hpico["Cant"] )
           rush_d= a2 + " con: " + str(ob.hpico["Cant"])
           in_d,out_d=grafo.degree((nam,id))
           ad={"Id":id,"Name":nam,"Out":out,
               "In":fin,"Rush H":rush_h,"Rush D":rush_d,
               "In degree (grafo)":in_d,"Out Degree (grafo)":out_d} 
           if nam == nam_init: 
              lt.addFirst(fst,ad)
           else:
               if nam == nam_fin:
                  lt.addFirst(lst,ad)
           lt.addLast(info,ad)
                                      
       ret=size,total_time,routes,info,fst,lst 

    else: 
       ret= None  
    return ret 


########################
# Funciones de consulta#
########################

def get_print(vertex,catalog,dirigido="dirigido"):
    """
    Consigue todo lo necesario para el primer print
    """
    map= catalog["model"]["tabla_general"]
    grafos= catalog["model"]["grafos"][dirigido]
    grafo= grafos.graf
  
    lista= lt.newList()
    for ve in lt.iterator(vertex):
        nom,id=ve
                     
        estat=getVal(map,nom)
        id= estat.id
        start= estat.start 
        end= estat.finish
        if dirigido == "dirigido":
         degree,out=grafos.degree(ve)
        
       
         add= {"ID":id,"Nombre":nom,"Salidas":start,"Llegadas":end
              ,"Grado Entradas (grafo)":degree,
              "Grado Salidas (grafo)":out}
        else: 
         degree= grafos.degree(ve)
         add= {"ID":id,"Nombre":nom,"Salidas":start,"Llegadas":end
              ,"Grado (grafo)":degree,
              }
            
        lt.addLast(lista,add)
    
    return lista   

def estat_info(estat,up,down):
    """
    Consigue el rango de fechas y la información de una estación 
    """
    datos= estat.get_range(up,down)
    if datos: 
     ar,emax,leng,cant= datos  
     emax= emax["Estacion"] + " Con: " + str(emax["Cant"])
     
     leng= leng["Id"] + " Con: " + str(leng["Len"])
      
     add={"Total inicio":ar,
          "Mayor estación fin":emax,
          "Viaje Tiempo Mayor":leng,
          "Canitad fin":cant}
     ret= lt.newList() 
     lt.addFirst(ret,add)  
    else: 
     ret= None 

    return ret            
        

def Size (lista):
    """
    Consigue el tamaño de una lista deseada
    """
    return lt.size(lista)

def Size_tabla(table):
    """
    COnsigue el tamaño de una tabla de hash
    """
    return mp.size(table)

def may(arb):
    """
    Consigue el maximo de un arbol
    """
    return om.maxKey(arb)

def men(arb):
    """
    Consigue el minimo de un arbol
    """
    return om.minKey(arb)

def Size_arbol(arbol):
    """
    Consigue el tamaño de un arbol
    """
    return om.size(arbol)

def contains(map,key):
    """
    Verifica si existe una llave en un mapa, tabla de hash
    """
    return mp.contains(map,key)

def getVal(map,key):
    """
    Retrina el VALOR de una llave de una TABLA de hash deseada
    """
  
    pair=mp.get(map,key)
           
    val= None
    if pair:
     val= me.getValue(pair)
    
    return val

def getval_arb(arb,key):
    """
    Retorna el valor de una llave de un arbol
    """
    pair= om.get(arb,key)
    if pair:
        val= me.getValue(pair)
    else: 
        val= None 

    return val 

def asds():
    asdf.asds()

def merge_sort(lista,cmp):
    """
    Ejecuta el merge sort basado en una cmp envíada 
    """
    return mrg.sort(lista,cmp)

def conseguir(lista,elem,parametro= 0):
    """
    Consigue n elem dentro de un lista a abuscar dependiendo del parametro.
    Catalogo: El conjunto de adts.
    Abuscar: El str del adt que se desea conseguir datos.
    Elem: Cantidad de elementos a conceguir
    Parametro: SI es diferente a 0 se consigue el top, pero de atras hacia adelante 
    """   
    size= lt.size(lista)
    maxix= 1
    if parametro !=0 : 
     maxix= size - elem 
     elem= elem +1 
    mini= lt.subList(lista,maxix,elem)
    return mini

#################################################################
# CMPS binarias, es decir para creació0n de estructuras de datos#
#################################################################

def cmp_grafos(stop, keyvaluestop):
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


def cmp_lista(viaje1,viaje2):
    """
    Un cmp function  a partir de id de un viaje 
    """
    id1= viaje1["Trip Id"]
    id2= viaje2["Trip Id"]

    if id1 > id2:
        val= 1
    if id2 > id1:
        val= -1  
    if id1 == id2:
        val= 0     
    return val   

def cmp_fechas(fech1,fech2):
    """
    Una cmp apra las fechas     
    """
    if fech1 == fech2 :
        return 0 
    if fech1 > fech2 :
        return 1
    if fech1< fech2 :
        return -1 

def cmp_maps(id,key):
    """
    Un cmp para los mapas en general
    """
    try:
     tagentry = me.getKey(key)
    
     if (id == tagentry):
        return 0
     elif (id > tagentry):
        return 1
     else:
        return -1
    except: 
      print(id,key,tagentry)
      print(type(id),type(key),type(tagentry))   
      1/0
         
########################
# CMPs de ordenamiento #
########################

def cmp_ord(obj1,obj2):
    """
    Ordena los objetos por cantidad
    """
    return obj1.start > obj2.start

def cmp_scc(sc1,sc2):
    """
    Ordena los scc
    """    
    if sc1["Tamaño"]==sc2["Tamaño"]:
       return sc1["Componente"] > sc2["Componente"]
    return sc1["Tamaño"]>sc2["Tamaño"]    