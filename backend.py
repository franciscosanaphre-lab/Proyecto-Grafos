import math
import random
import copy

# Diccionario de vértices: {id: (x, y)}
vertices = {}
# Lista de aristas: [(u, v), (u2, v2), ...]
edges = []
# Diccionario de grados de cada vértice: {id: grado}
degrees = {}

def default_settings():
    """
    Reinicia el estado interno del backend:
    - Limpia vértices, aristas y grados.
    Se usa cuando quieres empezar una nueva gráfica desde cero.
    """
    global vertices
    global edges
    global degrees

    vertices.clear()
    edges.clear()
    degrees.clear()

def add_vertex(id,coords):
    """
    Agrega un vértice al grafo.

    Parámetros
    ----------
    id : int
        Identificador del vértice.
    coords : tuple(int, int)
        Coordenadas (x, y) del vértice en la pantalla.
    """
    vertices[id] = coords
    print(f"Added vertex: 'id:{id} | coords: {coords}")

def add_edge(edge):
    """
    Agrega una arista (u, v) al grafo si no existe ya.
    También evita agregar la arista si existe la versión invertida (v, u).

    Parámetros
    ----------
    edge : tuple(int, int)
        Par (u, v) que representa la arista.
    """
    if edge in edges:
        return 
    
    redge = (edge[1],edge[0]) # check if the same esge doesn't exist already but reversed
    if redge in edges:
        return

    
    edges.append(edge)
    print("added edge:",edge)
        
def calculate_edges_weight():
    """
    Calcula la longitud (peso) de cada arista usando distancia euclidiana
    entre las coordenadas de sus vértices.

    Retorna
    -------
    dict
        Diccionario { (u, v): distancia } con dos decimales.
    """
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
    """
    Selecciona 2 vértices aleatorios del diccionario 'vertices'.

    Retorna
    -------
    list
        Lista de 2 elementos, cada uno es (id, (x, y)) como item() de un dict.
    """
    print("vertices:",vertices)
    return random.sample(list(vertices.items()), k=2)

def get_adyacent_edges(id):
    """
    Obtiene todas las aristas adyacentes a un vértice dado.

    Parámetros
    ----------
    id : int
        Identificador del vértice.

    Retorna
    -------
    list
        Lista de aristas (u, v) donde 'id' aparece en la arista.
    """
    adyacent = []
    for edge in edges:
        #print("ID:",id," in:",edge,"==",id in edge)
        if id in edge:
            adyacent.append(edge)

    return adyacent

def closest_vertices(start,adyacent, owidths, permanent_values):
    """
    Dado un vértice 'start', sus aristas adyacentes y los pesos de las aristas,
    calcula el peso temporal de cada vértice adyacente (Dijkstra).

    Parámetros
    ----------
    start : int
        Vértice desde el cual se evalúa.
    adyacent : list
        Aristas adyacentes a 'start'.
    owidths : dict
        Diccionario {(u, v): peso} de las aristas.
    permanent_values : dict
        Distancias definitivas ya fijadas para ciertos vértices.

    Retorna
    -------
    list
        Lista de tuplas (vertex, peso_temporal) ordenada por peso.
    """
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

    # Ordena por el peso (segunda componente)
    weighted_vertices.sort(key=lambda e:e[1])

    return weighted_vertices

def closest_from_temporal(temporal_values):
    """
    A partir del diccionario de valores temporales (Dijkstra),
    obtiene el vértice con menor peso.

    Parámetros
    ----------
    temporal_values : dict
        {vertex: peso_temporal}

    Retorna
    -------
    tuple
        (vertex, peso) con el menor peso.
    """
    values = []
    for vertex in temporal_values:
        nvertex = (vertex,temporal_values[vertex]) # (1,20)
        values.append(nvertex)
        print("appended:",nvertex)
    
    print("values:",values)
    values.sort(key=lambda e:e[1])
    return values[0]

def dijkstra_algorithm(start,end):
    """
    Implementación del algoritmo de Dijkstra para encontrar el camino más corto
    entre 'start' y 'end' en el grafo actual.

    Parámetros
    ----------
    start : int
        Vértice origen.
    end : int
        Vértice destino.

    Retorna
    -------
    list
        Lista de aristas (v_actual, v_anterior) que representan la ruta desde
        'start' hasta 'end' (reconstruida hacia atrás).
    """
    vstart = start

    temporal_values = {}
    permanent_values = {}
    previous_node = {}

    # Calcula los pesos de todas las aristas
    weights_dic = calculate_edges_weight()

    # El vértice de inicio tiene distancia 0
    permanent_values[start] = 0

    # Continúa hasta que todos los vértices hayan sido fijados como permanentes
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

    # Reconstrucción de la ruta desde 'end' hacia 'start' usando previous_node
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
    """
    Determina si el grafo actual es:
    - Euleriano (todos los vértices de grado par),
    - Semi-euleriano (exactamente 2 vértices de grado impar),
    - O no euleriano.

    Retorna
    -------
    (int, None | list)
        1, None        -> Grafo euleriano (circuito euleriano).
        2, [v1, v2]    -> Grafo semi-euleriano (camino euleriano entre v1 y v2).
        0, None        -> No euleriano.
    """
    degrees.clear() 

    # Calcula el grado de cada vértice
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
    """
    Versión local de get_adyacent_edges pero recibiendo la lista 
    de aristas como parámetro.

    Parámetros
    ----------
    id : int
        Vértice para el que se buscan aristas adyacentes.
    edges : list
        Lista de aristas a considerar.

    Retorna
    -------
    list
        Lista de aristas donde aparece 'id'.
    """
    adyacent = []
    for edge in edges:
        #print("ID:",id," in:",edge,"==",id in edge)
        if id in edge:
            adyacent.append(edge)

    return adyacent


def degree(vertex,edges):
    """
    Calcula el grado de un vértice en una lista de aristas dada.

    Parámetros
    ----------
    vertex : int
        Vértice cuyo grado se quiere calcular.
    edges : list
        Lista de aristas.

    Retorna
    -------
    int
        Grado del vértice.
    """
    degree = 0
    for edge in edges:
        if vertex in edge:
            degree+=1
    
    return degree

def is_connected(edges, vertices):
    """
    Verifica si el grafo es conexo usando un recorrido recursivo
    (basado en trayectoria).

    Parámetros
    ----------
    edges : list
        Lista de aristas.
    vertices : dict
        Diccionario de vértices {id: coords} solo para saber qué vértices hay.

    Retorna
    -------
    bool
        True si el grafo es conexo, False si es disconexo.
    """
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
    """
    Recorre recursivamente el grafo desde 'original_vertex',
    añadiendo vértices alcanzables a la lista t.

    Parámetros
    ----------
    original_vertex : int
        Vértice desde el que se inicia o continúa el recorrido.
    t : list
        Lista que acumula los vértices visitados.
    edges : list
        Lista de aristas a considerar.
    """
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
    """
    Dada una arista (u, v) y un vértice a ignorar (por ejemplo el vértice
    actual), devuelve el otro vértice de la arista.

    Parámetros
    ----------
    edge : tuple(int, int)
        Arista (u, v).
    ignore_vertex : int
        Vértice que queremos ignorar.

    Retorna
    -------
    int
        El otro vértice de la arista.
    """
    for vertex in edge:
        if vertex != ignore_vertex:
            return vertex

def eulerian_circut(etype,start):
    """
    Implementa el algoritmo tipo Fleury para encontrar un circuito/camino
    euleriano, dependiendo de 'etype':

    etype = 1  -> grafo euleriano (se espera un circuito que inicia y termina en el mismo vértice).
    etype = 2  -> grafo semi-euleriano (camino que inicia y termina en vértices de grado impar).

    Parámetros
    ----------
    etype : int
        Tipo de grafo (1 o 2, según is_eulerian).
    start : None | list
        Si etype = 2, contiene [v1, v2] con los vértices de grado impar.
        Si etype = 1, se ignora y se arranca con la primera arista.

    Retorna
    -------
    list
        Lista de aristas (u, v) en el orden en que se recorre el camino/circuito euleriano.
    """
    start_vertex = None
    print(etype)
    if etype == 1:
        # Empieza en el primer vértice de la primera arista
        start_vertex = edges[0][0]
    else:
        # Para semi-euleriano: empieza en uno de los vértices impares
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
                # Si deg == 1, es la única arista posible para salir
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
    """
    Función de conveniencia que llama a eulerian_circut si el grafo
    es euleriano o semi-euleriano.

    Parámetros
    ----------
    etype : int
        Tipo de grafo (1 = euleriano, 2 = semi-euleriano).
    start : None | list
        Vértices de grado impar si etype = 2, o None si etype = 1.

    Retorna
    -------
    list | None
        Camino/circuito euleriano como lista de aristas, o None si no aplica.
    """
    if etype == 1 or etype ==2:
        return eulerian_circut(etype,start)
