
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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)

##############################
# Inicialización del Catálogo#
##############################
def new_cata():
    """
    Llama al modelo y crea un catálogo
    """
    cata= {"model":None}
    cata["model"]= model.new_catalog()
    return cata


def asds():
    model.asds()


###################################
# Funciones para la carga de datos#
###################################

def caragar_csv(catalogo):
    """
    Abre el archivo csv y lo carga 
    """
    catalog= catalogo["model"]
    bikes= cf.data_dir + "Bikeshare-ridership-2021-utf8-large.csv"
    file= csv.DictReader(open(bikes, encoding= "utf_8" ))
    t1= getTime()   
    
    for route in file: 
        
        model.add_datos(catalog,route)
              
    t2= getTime()
    print("Tiempo: ", deltaT(t1,t2))
    asds()
    print("Cargando los grafos...")

    model.cargar_grafos(catalog)
    t3= getTime()
    print("Tiempo: ", deltaT(t2,t3))
    asds()
    t41= getTime()
    print("Tiempo: ", deltaT(t3,t41))
    print("Cargando los Datos parte 2 :)")
    
    model.add_datos2(catalog)
    asds()
    print("Cargando cositas de los req...")
    t4= getTime()
    model.load_visitadas(catalog)
    model.componentes_scc(catalog)
    dat= catalog["Premium_routes"]
    dat.load_tree()
    dat.max_min()
   
    sz= model.Size_tabla(catalog["tabla_general"])
    sr= catalog["Bicis"].size()
    size = model.Size(catalog["bikes_lista"])    
    print("Tiempo: ", deltaT(t41,t4))
    return  size,sr,sz 

############################
# Funciones de ordenamiento#
############################

##########################################
# Funciones de consulta sobre el catálogo#
##########################################
def get_print(vertex,catalog,dirigido= "dirigido"):
    """
    Consigue lo necesario para la impresión inicial 
    """
    return model.get_print(vertex,catalog,dirigido) 

def get_Val(map,key):
    """
    Consigue un valor de un mapa
    """
    return model.getVal(map,key)

def info_estat(estat,up,down):
    """
    Consigue la infomación de la estación para el req 7
    """
    return model.estat_info(estat,up,down)

def ruta_minima(catalogo,inicio,fin):
    """
    Consigue la información de la ruta mínima
    """
    return model.shortest_path(catalogo,fin,inicio)

def dfsss(graf,source, disponibilidad, min_estaciones, max_rutas):
    """
    Ejecuta un dfs, algo así 
    """
    return model.look_routes(graf,source, disponibilidad, min_estaciones, max_rutas)

#############
# Extras :) #
#############


def getTime():
    
    return float(time.perf_counter()*1000)

def deltaT(start,end):
    """
    Consigue el tiempo total, recibeindo un tiempo inicial y final
    """
    delta= float(end-start)
    return delta


def Conseguirelem(lista,cantidad,ultimos= "nah"):
    """
    Consigue x elementos de una lista ya definida, no de lago del catalogo,
    bueno no llama al catalogo en ningun momento
    Lista. La lsita  aconseguri los elementos
    cantidad: elementos a conseguir.
    Ultimos: Se coloca Otro valor para conseguir los elementos desde el final.
    """
    if ultimos == 'nah':
       mini=model.conseguir(lista,cantidad)
    else: 
       mini=model.conseguir(lista,cantidad,"a")
    return mini 

def contiene(map,key):
    """
    Revisa si contiene una llave un mapa
    """
    return model.contains(map,key)