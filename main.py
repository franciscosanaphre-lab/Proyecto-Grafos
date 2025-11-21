import pygame
import backend

# Inicializa pygame y la ventana principal

pygame.init()
mouse_x, mouse_y = 0,0
screen_width = 800 
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Proyecto graficas")

# Colores y parámetros gráficos

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (52, 140, 235)
BLACK = (35, 35, 36)
DARK_BLUE = (0, 0, 255)
RADIUS = 10  # Radio de los vértices (círculos rojos/azules)

 
# Texto & instrucciones

font = pygame.font.SysFont("Arial", 20) 

# Render instruction function


def render_instructions(ilist):
    """
    Paramétro 'ilist' lista de instrucciones en texto
    Retorna el texto para renderizar con pygame.draw
    """

    start = 20 # Posición inicial en Y para el primer renglón de texto
    rlist = []
    for instruction in ilist:

        instrucciones_text_surface = font.render(instruction, True, BLACK)
        instrucciones_text_rect = instrucciones_text_surface.get_rect()
        instrucciones_text_rect.topleft = (5, start)
        start+=20 # baja 20 pixeles para la siguiente instrucción

        rlist.append((instrucciones_text_surface,instrucciones_text_rect))
    return rlist

# Conjuntos de instrucciones para distintos “modos” del programa

instructions_draw = [
    "Click derecho para moverte de vértice.",
    "Presione ENTER para terminar."
]

instructions_menu = [
    "Presione 1 si quiere encontrar un camino euleriano entre 2 puntos",
    "Presione 2 si quiere encontrar la ruta más corta entre 2 puntos"
]

instrucciones_pesos = [
    "Seleccione 2 vertices dando click en los vértices",
    "Presione R para seleccionar 2 vertices aleatoriamente"
]

reiniciar_instrucciones = [
    "Presiona R para poder buscar otro camino entre 2 puntos",
    "Presiona T para buscar camino Euleriano",
    "Presiona ENTER para volver a dibujar otra gráfica"
]

reiniciar_no_euleriana = [
    "Tu gráfica no es euleriana. Tiene más de 2 vértices de grado impar",
    "Preiona ENTER para volver a dibujar otra gráfica"
]

# Crea las listas de texto listas para renderizar

render_draw_instructions = render_instructions(instructions_draw)
render_menu_instructions = render_instructions(instructions_menu)
render_pesos_instructions = render_instructions(instrucciones_pesos)
render_reiniciar_instrucciones = render_instructions(reiniciar_instrucciones)
reiniciar_no_euleriana_instrucciones = render_instructions(reiniciar_no_euleriana)


# Vertices, Circles, Edges storage
# --------------------------------
# letras: lista de (surface, rect) con las etiquetas de los vértices (números)
# drawn_circles: lista de (center, color, radius) de todos los vértices dibujados
# drawn_lines: lista de (punto_origen, punto_fin) para las aristas dibujadas

letras = [] 
drawn_circles = []  
drawn_lines = [] 


# route_lines: aristas que forman la ruta más corta (Dijkstra)
# eulerian_lines: aristas del camino/circuito euleriano

route_lines = [] 
eulerian_lines = [] 

# Variables de estado del programa
# ----------------------------
# running: controla el loop principal
# drawing: si el usuario está en modo dibujo o en modo menú

running = True 
drawing = True


# Variables de renderización de instrucciones
# ---------------------------- 
# menu: si el usuario está en el menú principal
# pesos: si el usuario está en modo pesos (ruta más corta)
# euleriano: si el usuario está viendo el camino euleriano
# no_euleriana: muestra instrucciones si la gráfica no es euleriana
# reiniciar: se activa después de mostrar un camino; permite elegir otro camino

menu = False 
pesos = False 
euleriano = False
no_euleriana = False 
reiniciar = False

# pesos_vertices: IDs de los vértices seleccionados para Dijkstra
pesos_vertices = []

# vertices: diccionario {id: (x, y)} con la posición de cada vértice
vertices = {}

# x: contador de vértices (para asignar IDs y etiquetas)
x = 0

# CURRENT_VERTEX: vértice "actual" para conectar nuevas aristas mientras dibujas
CURRENT_VERTEX = 1



def default_settings():
    """
    Restablece todos los estados globales del programa para comenzar una nueva
    gráfica desde cero.
    """

    global x

    global letras
    global drawn_circles
    global drawn_lines
    global route_lines
    global eulerian_lines
    global pesos_vertices
    global vertices
    global running
    global drawing
    global menu
    global pesos
    global euleriano
    global no_euleriana
    global reiniciar
    global CURRENT_VERTEX

    # Limpia todas las listas y estructuras relacionadas con el grafo

    eulerian_lines.clear()
    letras.clear()
    drawn_circles.clear()
    drawn_lines.clear()
    route_lines.clear()
    pesos_vertices.clear()
    vertices.clear()
    running = True
    x=0

    drawing = True 
    menu = False

    pesos = False
    euleriano = False

    no_euleriana = False

    reiniciar = False
    CURRENT_VERTEX = 1


def inside_vertex(coords):

    """
    Dado un punto (x, y) del mouse, revisa si está dentro de alguno de los
    círculos/vértices definidos en 'vertices'. Si sí, devuelve un diccionario:
    {"id": id_vertice, "coords": (cx, cy)}.
    Si no encuentra ninguno, devuelve None.
    Función usada para detectar clicks en vértices y crear ciclos en la grafica.
    """

    x = coords[0]
    y = coords[1]

    for i in vertices:
        circle_center = vertices[i]

        c_x = circle_center[0]
        c_y = circle_center[1]

        # Comprueba si la distancia al centro es menor o igual que el diámetro (2*RADIUS)

        if ((x-c_x)**2 + (y-c_y)**2)<=(RADIUS*2)**2:
            return {"id":i,"coords":circle_center}

    
    return None

def dibujar_camino_euleriano(eulerian_path):

    """
    Dada una secuencia de aristas que forman un camino o circuito euleriano,
    las dibuja una por una en la pantalla con un delay de 1 segundo entre cada una.

    eulerian_path: lista de aristas [(v1, v2), (v2, v3), ...]
    """

    global reiniciar

    for edge in eulerian_path:
        
        # Extrae los vértices de la arista
        
        v1 = edge[0]
        v2 = edge[1]

        # Extrae las coordenadas de los vértices de la arista

        v1_cords = vertices[v1]
        v2_cords = vertices[v2]

        # Pone el código listo para permitir reiniciar después de dibujar el camino

        reiniciar = True

        # Dibuja la arista en la pantalla

        pygame.draw.line(screen,DARK_BLUE, v1_cords,v2_cords,6)
        pygame.display.update()     
        pygame.event.pump()         
        pygame.time.delay(1000) 

    return

# Loop principal de la interfaz (pygame)
# ====================
while running:
    # Manejo de eventos de pygame (teclado, mouse, cierre de ventana, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Cerrar la ventana
            running = False

        elif event.type == pygame.KEYDOWN:
            
            # ENTER/RETURN: depende del modo (dibujando o reiniciando)

            if event.key == pygame.K_RETURN: 

                # Si drawing==true (modo dibujo), termina el dibujo y va al menú.
                if drawing:
                    
                    # Si no hay suficientes vértices no permite continuar
                    if len(letras)<2:
                        print("no cumple el mínimo de vértices (2)")
                        continue
                    
                    # Pasa del modo de dibujo al menú principal
                    drawing = False
                    menu = True

                    continue

                # Si no estás dibujando y estás en modo reinicio o no_euleriana,
                # reinicia toda la gráfica y el backend.

                if reiniciar or no_euleriana:
                    default_settings()
                    backend.default_settings()

            # T: sólo tiene efecto si estás en modo reiniciar
            # -----------------------------
            # Permite buscar otro camino euleriano sin redibujar toda la gráfica
            elif event.key == pygame.K_t:
                if reiniciar == False:
                    continue 
                reiniciar = False
                print("reiniciando")
                route_lines.clear()
                pesos_vertices.clear()
                eulerian_lines.clear()

                drawn_circles = [
                    (center, color, radius)
                    for center, color, radius in drawn_circles
                    if color == RED
                ]

                menu = False
                euleriano = True

                # Redibujar la pantalla limpia antes de animar el camino euleriano
                screen.fill(WHITE)

                # Dibuja los nombres de los vértices
                for letra in letras:
                    screen.blit(letra[0], letra[1])

                # Vuelve a dibujar los círculos (vértices)
                for center, color, radius in drawn_circles:
                    pygame.draw.circle(screen, color, center, radius)

                # Dibuja las aristas originales
                for origin, end in drawn_lines:
                    pygame.draw.line(screen, BLACK, origin, end, 3)

                # Actualiza la pantalla con todos los cambios.
                pygame.display.flip()

                # Checa si el grafo es euleriano.
                is_eulerian, start = backend.is_eulerian()

                # Valores de is_eulerian:
                # 0 = no euleriano
                # 1 = circuito euleriano
                # 2 = camino euleriano

                print("Is eulerian:",is_eulerian)

                if is_eulerian ==0:
                    no_euleriana = True
                    print("No euleriana:", no_euleriana)
                    continue
                elif is_eulerian ==1 or is_eulerian ==2:\
                    # Sí tiene camino/circuito euleriano
                    no_euleriana = False
                    eulerian_path = backend.find_eulerian_path(is_eulerian,start)
                    print("eulerian path:",eulerian_path)

                    # Dibuja el camino euleriano arista por arista, con un delay

                    dibujar_camino_euleriano(eulerian_path)
                    
                    


            # 1: desde el menú, entra en modo “Euleriano”

            elif event.key == pygame.K_1: 
                if menu:
                    
                    # Actualiza el estado de las instrucciones
                    menu = False
                    euleriano = True 

                    is_eulerian, start = backend.is_eulerian()

                    if is_eulerian ==0:
                        no_euleriana = True
                        print("No euleriana:", no_euleriana)
                        continue
                    elif is_eulerian ==1 or is_eulerian ==2:
                        # Sí tiene camino/circuito euleriano
                        no_euleriana = False
                        eulerian_path = backend.find_eulerian_path(is_eulerian,start)
                        print("eulerian path:",eulerian_path)

                        # Dibuja el camino euleriano arista por arista, con un delay

                        dibujar_camino_euleriano(eulerian_path)

            # 2: desde el menú, entra en modo selección de pesos (ruta más corta)
            elif event.key == pygame.K_2:
                if menu:
                    menu = False
                    pesos = True
                    

            elif event.key == pygame.K_r:

                # R en modo ‘reiniciar’: limpia rutas y vuelve a modo pesos=True

                if reiniciar:
                    reiniciar = False
                    route_lines.clear()
                    pesos_vertices.clear()
                    eulerian_lines.clear()

                    drawn_circles = [(center, color, radius)  # Filtra solo los circulos rojos
                        for center, color, radius in drawn_circles 
                        if color == RED]
                    
                    pesos = True
                    continue
                        
                

                if pesos == False:
                    continue

                pesos = False 

                # R en modo pesos: selecciona 2 vértices aleatorios para Dijkstra
                
                rvertices = backend.select_random_vertices()
                print("RANDOM VERTICES:",rvertices)

                # Dibuja los vértices seleccionados en azul
                for vertex in rvertices:
                    print("Random vertex:",vertex)
                    drawn_circles.append((vertex[1], BLUE, RADIUS)) 

                # Genera la ruta más corta entre los 2 vértices seleccionados
                    
                route = backend.dijkstra_algorithm(rvertices[0][0], rvertices[1][0])

                # Dibuja la ruta más corta arista por arista

                for edge in route:

                    # Extrae los vertices de cada arista
                    # v1: Vertice de origen
                    # v2: Vertice de destino

                    v1 = edge[0]
                    v2 = edge[1]

                    v1_cords = vertices[v1]
                    v2_cords = vertices[v2]

                    reiniciar = True

                    # Guarda las aristas en route_lines para ser dibujadas en el loop principal

                    route_lines.append((v1_cords, v2_cords))
            
        elif event.type == pygame.MOUSEMOTION:
            # Actualiza la posición del mouse en todo momento
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click derecho: "moverte" a otro vértice (cambia CURRENT_VERTEX y marca en rojo)
            if event.button == 3:  
                pos = event.pos


                # Omite si no estas dibujando
                if drawing == False:
                    continue


                # Obtiene el vértice dentro del cual se hizo click 
                # Pos: Posicion del mouse al hacer click derecho

                vertex = inside_vertex(pos)

                # Si no hizo click dentro de un vértice, omite
                if vertex == None:
                    continue

                # Cambia el vértice actual 
                CURRENT_VERTEX = vertex["id"]
                drawn_circles.append((vertex["coords"], RED, RADIUS)) 
                

            # Click izquierdo: agregar vértice nuevo o conectar aristas

            elif event.button == 1:

                # Obtiene la posición del mouse al hacer click izquierdo
                mouse_pos = event.pos

                # Si estás en modo pesos, selecciona vértices para Dijkstra
                if pesos:

                    """
                    vertex: diccionario {"id": id_vertice, "coords": (cx, cy)}
                    1. Revisa si el click fue dentro de un vértice
                    2. Si ya fue seleccionado, omite
                    3. Si no, lo agrega a la lista de vértices seleccionados
                    """
                    vertex = inside_vertex(mouse_pos)
                    

                    if vertex == None:
                        continue

                    vid = vertex["id"]

                    if vid in pesos_vertices:
                        continue
                    
                    pesos_vertices.append(vid)
                    drawn_circles.append((vertex["coords"], BLUE, RADIUS)) 

                    # Si ya hay 2 vértices seleccionados, calcula y dibuja la ruta más corta

                    if len(pesos_vertices)>=2:

                        # Pesos = False para evitar seleccionar más vértices
                        pesos = False
                        route = backend.dijkstra_algorithm(pesos_vertices[0], pesos_vertices[1])

                        for edge in route:

                            v1 = edge[0]
                            v2 = edge[1]

                            v1_cords = vertices[v1]
                            v2_cords = vertices[v2]

                            reiniciar = True

                            route_lines.append((v1_cords, v2_cords))

                    
                    continue

                
                #Si estás en modo dibujo, agrega un nuevo vértice o conecta con otro
                #vértice si el click fue dentro de uno existente.
                
                # Omite si no estás en modo dibujo
                if drawing == False: 
                    continue
                
                vertex = inside_vertex(mouse_pos)

                if vertex != None:
                    if CURRENT_VERTEX == vertex["id"]:
                        continue
                    
                    # Añade arista desde CURRENT_VERTEX hasta el vértice clickeado
                    backend.add_edge((CURRENT_VERTEX,vertex["id"]))
                    drawn_lines.append((drawn_circles[len(drawn_circles)-1][0],vertex["coords"]))
                    break
                
                # Si no hizo click dentro de un vértice existente, crea uno nuevo
                # Genera un nuevo ID para el vértice (letra)
                # x es una variable global que se incrementa cada vez que se crea un vértice

                x +=1

                text_surface = font.render(str(x), True, BLACK)
                text_rect = text_surface.get_rect()

                x_coordinate = mouse_pos[0]+10
                y_coordinate = mouse_pos[1]+10
                text_rect.topleft = (x_coordinate, y_coordinate)

                letras.append((text_surface, text_rect))

                backend.add_vertex(x,mouse_pos)

                # Si ya había al menos un círculo, conectas el último vértice con éste

                if len(drawn_circles)>0:

                    backend.add_edge((CURRENT_VERTEX,x))
                    CURRENT_VERTEX = x

                    origin_vertex = drawn_circles[len(drawn_circles)-1][0]

                    print("drawn circle origin:",origin_vertex)
                    drawn_lines.append((origin_vertex,mouse_pos))

                # Guarda posición del vértice en el diccionario local
                vertices[x] = mouse_pos
                
                # Dibuja el nuevo vértice en rojo
                drawn_circles.append((mouse_pos, RED, RADIUS)) 
        

    # ---------------------------
    # RENDERIZADO DE LA ESCENA
    # ---------------------------

    screen.fill(WHITE)  

    # Renderiza los nombres de los vértices

    for letra in letras:
        screen.blit(letra[0], letra[1])

    # Renderiza instruccioness

    if drawing:
        for instruction in render_draw_instructions:
            screen.blit(instruction[0], instruction[1])

    if menu:
        for instruction in render_menu_instructions:
            screen.blit(instruction[0], instruction[1])

    if pesos:
        for instruction in render_pesos_instructions:
            screen.blit(instruction[0], instruction[1])

    if reiniciar:
        for instruction in render_reiniciar_instrucciones:
            screen.blit(instruction[0], instruction[1])

    if no_euleriana:
        for instruction in reiniciar_no_euleriana_instrucciones:
            screen.blit(instruction[0], instruction[1])

    # Renderiza linea que sigue el mouse (arista temporal) y el circulo que sigue al mouse

    if drawing:
        
        if len(drawn_circles)>0:
            # Arista temporal
            pygame.draw.line(screen,BLACK, drawn_circles[len(drawn_circles)-1][0],(mouse_x,mouse_y),3)

        # Renderiza el circulo que sigue al mouse

        pygame.draw.circle(screen, BLUE, (mouse_x,mouse_y), 5)

    # Renderiza todos los vertices

    for center, color, radius in drawn_circles:
        pygame.draw.circle(screen, color, center, radius)

    # Renderiza todas las aristas actuales

    for origin,end in drawn_lines:
        pygame.draw.line(screen,BLACK, origin,end,3)

    # Renderiza la trayectoria de pesos

    for origin,end in route_lines:
        pygame.draw.line(screen,DARK_BLUE, origin,end,6)

    for origin,end in eulerian_lines:
        pygame.draw.line(screen,DARK_BLUE, origin,end,6)

    pygame.display.flip()

pygame.quit()

