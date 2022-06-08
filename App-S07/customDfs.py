from DISClib.ADT import graph as g
from DISClib.ADT import list as lt
from DISClib.ADT import map as map
from DISClib.Utils import error as error

def obtenerRutas(graph, source, disponibilidad, min_estaciones, max_rutas):
    try:
        search = {
            'source': source,
            'visited': None,
        }
        search['visited'] = map.newMap(numelements=g.numVertices(graph),
                                       maptype='PROBING',
                                       comparefunction=graph['comparefunction']
                                       )
        map.put(search['visited'], source, {'marked': True, 'edgeTo': None})
        return dfsVertex(search, graph, source, disponibilidad, min_estaciones, source, [source], [], max_rutas)
    except Exception as exp:
        error.reraise(exp, 'dfs:DFS')

def dfsVertex(search, graph, vertex, disponibilidad, estaciones, source, rutaActual, totalRutas, maxRutas):
    try:
        if(len(totalRutas)>= maxRutas): return totalRutas
        adjlst = g.adjacentEdges(graph, vertex)
        if adjlst is None: return search
        for edge in lt.iterator(adjlst):
            w = edge['vertexB']
            visited = map.get(search['visited'], w)
            nuevaDisponibilidad = disponibilidad - edge['weight']
            nuevasEstaciones = estaciones - 1
            nuevaRuta = list(rutaActual)
            nuevaRuta.append(w)
            if visited is None and nuevaDisponibilidad > 0:
                map.put(search['visited'],
                        w, {'marked': True, 'edgeTo': vertex})
                dfsVertex(search, graph, w, nuevaDisponibilidad,
                          nuevasEstaciones, source, nuevaRuta, totalRutas, maxRutas)
            elif visited is not None and nuevaDisponibilidad >= 0 and w == source and estaciones <= 0:
                totalRutas.append((nuevaRuta, disponibilidad, nuevasEstaciones))
        return totalRutas
    except Exception as exp:
        error.reraise(exp, 'dfs:dfsVertex')