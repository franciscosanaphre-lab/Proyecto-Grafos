import math
import random
import copy

vertices = {}
edges = []
degrees = {}

def default_settings():
    global vertices
    global edges
    global degrees

    vertices.clear()
    edges.clear()
    degrees.clear()

def add_vertex(id,coords):
    vertices[id] = coords
    print(f"Added vertex: 'id:{id} | coords: {coords}")

def add_edge(edge):
    if edge in edges:
        return 
    
    redge = (edge[1],edge[0]) # check if the same esge doesn't exist already but reversed
    if redge in edges:
        return

    
    edges.append(edge)
    print("added edge:",edge)
        
def calculate_edges_weight():
    weighted_edges = {}

    print("Edges:", edges)
    for edge in edges:

        v1 = edge[0]
        v2 = edge[1]

        print("Distance v1:",v1)
        print("Distance v2:",v2)

        distance = round(math.sqrt((vertices[v1][0]-vertices[v2][0])**2 + (vertices[v1][1]-vertices[v2][1])**2),2)
        #weighted_edges.append({"id":edge,"weight":distance})

        weighted_edges[edge] = distance
    
   
    print(weighted_edges)
    
    return weighted_edges

def select_random_vertices():
    print("vertices:",vertices)
    return random.sample(list(vertices.items()), k=2)

def get_adyacent_edges(id):
    adyacent = []
    for edge in edges:
        #print("ID:",id," in:",edge,"==",id in edge)
        if id in edge:
            adyacent.append(edge)

    return adyacent

def closest_vertices(start,adyacent, owidths, permanent_values):
    weighted_vertices= []

    pstart = permanent_values[start] # Peso del vector inicial desde donde estamo evaluando

    for edge in adyacent:

        vertex = None

        # Checa cual es el vértice adyacente de la arista | vertex es la variable del vértice adyacente
        for v in edge:
            if v != start:
                vertex = v
                break

        weighted_edge = owidths[edge] # Peso de la arista que lo conecta

        temp_weight = pstart+weighted_edge # Nuevo peso temporal (peso del vertice de donde estamos evaluando + peso de la arista que conecta al vértice adyacente)

        weighted_vertices.append((vertex,temp_weight))

    weighted_vertices.sort(key=lambda e:e[1])

    return weighted_vertices

def closest_from_temporal(temporal_values):
    values = []
    for vertex in temporal_values:
        nvertex = (vertex,temporal_values[vertex]) # (1,20)
        values.append(nvertex)
        print("appended:",nvertex)
    
    print("values:",values)
    values.sort(key=lambda e:e[1])
    return values[0]

def dijkstra_algorithm(start,end):

    vstart = start

    temporal_values = {}
    permanent_values = {}
    previous_node = {}

    weights_dic = calculate_edges_weight()

    permanent_values[start] = 0

    while len(permanent_values) < len(vertices):

        adyacent = get_adyacent_edges(start)
        new_temp_values = closest_vertices(start, adyacent,weights_dic, permanent_values)

        # Se pone el valor temporal a todos 
        print("New temporal values:", new_temp_values)

        # Actualiza los valores de temporal_values con los nuevos recien obtenidos de evaluar desde el start_vertex
        for vertex_data in new_temp_values:
            print("vertex_data:", vertex_data)
            vertex = vertex_data[0]
            vertex_weight = vertex_data[1]

            if vertex in permanent_values:
                continue
            if vertex in temporal_values:
                if temporal_values[vertex]> vertex_weight:
                    temporal_values[vertex] = vertex_weight
                    previous_node[vertex] = start
            else:
                temporal_values[vertex] = vertex_weight
                previous_node[vertex] = start

            

        print("Before deleting temporal values:",temporal_values)

        closest = closest_from_temporal(temporal_values)

        # closest[0] es el vertice
        # closest[1] es el peso
        
        # Se fija el primer permanente
        permanent_values[closest[0]] = closest[1]
        del temporal_values[closest[0]]

        

        start = closest[0]
        
        print("New Temporal: ----")
        print(temporal_values)
        print("New Permanent: ----")
        print(permanent_values)

        print("New start:",start)

    print("Todos los vertices han sido evaluados. Resultados:")
    print('Permanent values', permanent_values)
    print('Previous node map:', previous_node)


    # Ruta desde start hasta end

    ruta = []

    latest = end

    print("start:",vstart)
    print("end:", end)

    while True:
        previous = previous_node[latest]
        ruta.append((latest,previous))

        print("previus:",previous)
        if previous == vstart:
            break 

        latest = previous


    print("Ruta:", ruta)

    print(vertices)
    print(edges)
    return ruta


# Parte de eulerianos

def is_eulerian():
    degrees.clear() 

    for edge in edges:
        for vertex in edge:
            if vertex in degrees:
                degrees[vertex] +=1
            else:
                degrees[vertex] = 1
    
    odd = 0
    odd_vertices = []
    for vertex in degrees:
        if degrees[vertex] %2 != 0:
            odd +=1 
            odd_vertices.append(vertex)

    print(degrees)
    if odd == 0:
        return 1,None # Euleriana
    elif odd == 2:
        return 2,odd_vertices # Semi-euleriana
    else:
        return 0,None # No eulerian

def get_adyacent_edges_specific(id,edges):
    adyacent = []
    for edge in edges:
        #print("ID:",id," in:",edge,"==",id in edge)
        if id in edge:
            adyacent.append(edge)

    return adyacent


def degree(vertex,edges):
    degree = 0
    for edge in edges:
        if vertex in edge:
            degree+=1
    
    return degree

def is_connected(edges, vertices):
    if len(edges) == 0:
        print("Edges vacio")
        return False
    redge = edges[0]
    rvertex = redge[0]
    
    t_map = []
    print(rvertex)

    trayectoria(rvertex, t_map,edges)
    
    print("T map",t_map)

    print(vertices)
    

    for v in vertices:
            if v not in t_map:
                print(f"V: {v} no está en t_map, por lo tanto la gráfica es disconexa")
                return False
    
    #print("G es conexa")
    return True
        

def trayectoria(original_vertex, t,edges):
    if original_vertex not in t:
        t.append(original_vertex)


    aedges = get_adyacent_edges_specific(original_vertex,edges)

    for edge in aedges:
        adyacent_vertex = None 
        
        for vertex in edge:
            if vertex != original_vertex and vertex not in t:
                adyacent_vertex = vertex
                break 

        if adyacent_vertex != None:
            #print('Adyacent vertex:',adyacent_vertex)
            t.append(adyacent_vertex)  
            trayectoria(adyacent_vertex,t,edges)

def get_vertex_from_edge(edge, ignore_vertex):
    for vertex in edge:
        if vertex != ignore_vertex:
            return vertex

def eulerian_circut(etype,start):

    start_vertex = None
    print(etype)
    if etype == 1:
        start_vertex = edges[0][0]
    else:
        start_vertex = start[0]
        end_vertex = start[1]

    print("Start:",start)


    #real_start = start_vertex
    temporal_edges = copy.deepcopy(edges)
    temporal_vertices = copy.deepcopy(vertices)
    

    deleted = []
    
    while True:
        found = False
        print("Starting loop again at:",start_vertex)
        adyacent = get_adyacent_edges(start_vertex)

        for edge in adyacent:
            if edge in deleted:
                continue

            new_edges = copy.deepcopy(temporal_edges)
            new_edges.remove(edge)

            connected = is_connected(new_edges, temporal_vertices) # Checa si despues de quitar la arista el grafo sigue conexo
            print("connected:", connected, edge)
            
            deg = degree(start_vertex, temporal_edges) 
            print("deg:",deg, edge)
            if connected or deg ==1 : 
                if deg == 1:
                    temporal_vertices.pop(start_vertex)
                temporal_edges.remove(edge)
                deleted.append(edge)
                print("connected edge:",edge)
                old_start_vertex = start_vertex
                found = True
                start_vertex = get_vertex_from_edge(edge,old_start_vertex)
                break 
        
        print("new data",found, start_vertex)
        if found == False:
            print('end')
           # print(deleted)
            return deleted


def find_eulerian_path(etype,start):
    if etype == 1 or etype ==2:
        return eulerian_circut(etype,start)
