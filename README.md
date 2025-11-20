# Proyecto: Visualizador de Grafos con Caminos Eulerianos y Ruta Más Corta

Proyecto en Python que permite **dibujar un grafo a mano** sobre la pantalla, y luego:

- Encontrar y animar un **camino/circuito euleriano** (si existe).
- Encontrar la **ruta más corta entre dos vértices** usando el algoritmo de **Dijkstra**.

El proyecto usa **Pygame** para la parte gráfica y un módulo propio `backend.py` para la lógica de grafos y algoritmos.

---

## Estructura del proyecto

- `main.py` 
  Contiene:
  - La ventana y el loop principal de Pygame.
  - El dibujo de vértices y aristas.
  - La interacción con el usuario (teclado y mouse).
  - Las llamadas a las funciones del `backend`.

- `backend.py`  
  Contiene:
  - Estructuras de datos del grafo (`vertices`, `edges`, `degrees`).
  - Implementaciones de:
    - Cálculo de pesos de aristas (distancia euclidiana).
    - **Algoritmo de Dijkstra** para ruta más corta.
    - Detección de si el grafo es **euleriano / semi-euleriano**.
    - Búsqueda de **camino/circuito euleriano** (tipo Fleury).

---

## Requisitos

- Python 3.x
- Librería `pygame`

Instalación de Pygame:

```bash
pip install pygame
```

Bibliografía:
Todos los algoritmos excepto el algoritmo para detectar si la gráfica es conexa (creado por mi) fueron tomados de "Introduction to Graph Theory - Robin.J Wilson"
https://webhomes.maths.ed.ac.uk/~v1ranick/papers/wilsongraph.pdf
