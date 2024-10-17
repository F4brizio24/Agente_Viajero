import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Generar matriz aleatoriamente
def generar_matriz(n):
    matriz = np.random.randint(1, 20, size=(n, n)) # Valores entre 1 y 20
    matriz = (matriz + matriz.T) // 2 # Matriz simétrica
    np.fill_diagonal(matriz, 0) # Diagonal principal con ceros
    return matriz # Matriz de adyacencia

# Generar matriz manualmente
def mostrar_campos_matriz(n):
    global entradas # Matriz de entrada
    entradas = []
    
    # Crear campos de entrada
    for i in range(n):
        fila_entradas = tk.Frame(estilo_interfaz)  # Fila de entradas
        fila_entradas.pack(pady=5) # Espacio entre filas
        fila = [] # Fila de valores
        
        # Crear campos de entrada
        for j in range(n):
            entrada = tk.Entry(fila_entradas, width=5) # Entrada de valores
            entrada.pack(side=tk.LEFT)  # Espacio entre columnas
            fila.append(entrada) # Agregar a la fila
        entradas.append(fila) # Agregar a la matriz de entradas

    ejec_matriz = tk.Button(interfaz, text="Ejecutar matriz", command=ejecutar_matriz) # Botón de ejecución
    ejec_matriz.pack(pady=10) # Espacio entre botones

# Ejecuta la matriz ingresada manualmente
def ejecutar_matriz():
    n = len(entradas) # Tamaño de la matriz
    matriz = np.zeros((n, n), dtype=int) # Matriz de adyacencia
    
    # Obtener valores de las entradas
    try:
        for i in range(n): # Recorrer filas
            for j in range(n): # Recorrer columnas
                if i == j: # Diagonal principal
                    continue # No se toma en cuenta
                valor = entradas[i][j].get() # Obtener valor
                if valor: # Si hay valor
                    valor = int(valor) # Convertir a entero
                    if 0 < valor < 20:  # Valores entre 1 y 20
                        matriz[i][j] = valor # Asignar valor
                        matriz[j][i] = valor # Asignar valor
                    else: # Valores no válidos
                        messagebox.showerror("Error", "Los valores deben ser positivos y menores a 20.") 
                        return # Salir de la función

        matriz = (matriz + matriz.T) // 2 # Matriz simétrica
        ejecutar_ciclo(matriz) # Ejecutar ciclo hamiltoniano
    except ValueError: # Valores no válidos
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# Calcula las distancias
def calcular_distancia(ciclo, matriz):
    distancia_total = 0 # Distancia total
    # Calcular la distancia total
    for i in range(len(ciclo)):
        distancia_total += matriz[ciclo[i]][ciclo[(i + 1) % len(ciclo)]] # Distancia
    return distancia_total

# Genera las permutaciones para el ciclo hamiltoniano
def generar_permutaciones(nodos, inicio, resultado):
    # Caso base
    if inicio == len(nodos) - 1:
        resultado.append(nodos[:]) # Agregar nodos
        return
    
    # Generar permutaciones
    for i in range(inicio, len(nodos)):
        nodos[inicio], nodos[i] = nodos[i], nodos[inicio] # Intercambiar nodos
        generar_permutaciones(nodos, inicio + 1, resultado) # Generar permutaciones
        nodos[inicio], nodos[i] = nodos[i], nodos[inicio] # Intercambiar nodos

# Ciclo hamiltoniano
def ciclo_hamiltoniano(matriz):
    n = len(matriz) # Tamaño de la matriz
    nodos = list(range(n)) # Nodos
    ciclos_posibles = [] # Ciclos posibles
    
    generar_permutaciones(nodos, 0, ciclos_posibles) # Generar permutaciones

    mejor_ciclo = None # Mejor ciclo
    mejor_distancia = float('inf') # Mejor distancia
    
    # Recorrer ciclos
    for ciclo in ciclos_posibles: 
        distancia = calcular_distancia(ciclo, matriz) # Calcular distancia
        # Actualizar mejor ciclo
        if distancia < mejor_distancia:
            mejor_distancia = distancia # Mejor distancia
            mejor_ciclo = ciclo # Mejor ciclo
            
    return mejor_ciclo, mejor_distancia # Mejor ciclo y distancia

# Muestra el grafo en la pantalla
def mostrar_grafo(matriz, ciclo):
    grafo = nx.Graph() # Grafo
    n = len(matriz) # Tamaño de la matriz
    
    # Agregar nodos y aristas
    for i in range(n):
        grafo.add_node(i) # Agregar nodo
        # Agregar aristas
        for j in range(i + 1, n):
            grafo.add_edge(i, j, weight=matriz[i][j]) # Agregar arista
    
    posicion = nx.spring_layout(grafo) # Posición del grafo
    nodos = ['red' if i == ciclo[0] else 'lightblue' for i in range(n)] # Colores de los nodos
    nx.draw(grafo, posicion, with_labels=True, node_color=nodos, node_size=800) # Dibujar grafo
    aristas = nx.get_edge_attributes(grafo, 'weight') # Aristas
    nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=aristas) # Etiquetas de las aristas

    arista_marca = [(ciclo[i], ciclo[(i + 1) % len(ciclo)]) for i in range(len(ciclo))] # Aristas del ciclo
    nx.draw_networkx_edges(grafo, posicion , edgelist=arista_marca, edge_color='red',  
                             width=2, style='dashed') # Dibujar aristas del ciclo

    plt.title("Grafo del Agente Viajero")
    plt.show()

# Muestra el ciclo del recorrido hamiltoniano
def ejecutar_ciclo(matriz):
    ciclo, distancia = ciclo_hamiltoniano(matriz) # Ciclo y distancia
    ciclo_str = " -> ".join(map(str, ciclo))  # Ciclo como cadena
    recorrido.config(text=f"Ciclo: {ciclo_str}\nDistancia: {distancia}") # Recorrido
    recorrido.pack(pady=10) # Espacio entre recorridos
    mostrar_grafo(matriz, ciclo) # Mostrar grafo

# Permite manejar el tamaño de la matriz y ejecutar si es aleatoria o manual
def manejar_matriz():
    op = entry_opcion.get() # Opción
    if op in ["1", "2"]:
        tam_matriz.pack(pady=10) # Espacio entre tamaños
        entry_tam.pack(pady=5)   # Espacio entre entradas
        tam_matriz_confirm.pack(pady=10) # Espacio entre confirmaciones
    else: 
        print("Por favor, ingrese '1' o '2'")

# Ingreso del tamaño y ejecución la matriz
def ingreso_tam_matriz():
    op = entry_opcion.get() # Opción
    try:
        n = int(entry_tam.get()) # Tamaño de la matriz
        # Validar tamaño
        if 8 <= n <= 16:
            if op == "1":
                ejecutar_ciclo(generar_matriz(n)) # Ejecutar matriz
            elif op == "2":
                mostrar_campos_matriz(n) # Mostrar campos de la matriz
            else:
                 messagebox.showerror("Error", "Opción no válida.")
        else:
            messagebox.showerror("Error", "El tamaño debe estar entre 8 y 16.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido.")

# Reinicia la interfaz
def reiniciar():
    interfaz.destroy()
    main()

# Función principal para ejecutar la interfaz
def main():
    global interfaz, estilo_interfaz, recorrido, entry_opcion, entry_tam, tam_matriz, tam_matriz_confirm

    # Interfaz gráfica con Tkinter
    interfaz = tk.Tk()
    interfaz.title("El Agente Viajero") # Título de la ventana
    interfaz.geometry("600x500") # Tamaño de la ventana

    # Estilo de la interfaz
    estilo_interfaz = tk.Frame(interfaz, width=400, height=500) 
    estilo_interfaz.pack(pady=10)

    # Elementos de la interfaz
    titulo = tk.Label(estilo_interfaz, text="Bienvenido al programa del Agente Viajero")
    titulo.pack(pady=10)

    # Opciones de generación de la matriz
    opcion = tk.Label(estilo_interfaz, text="Ingrese la opción de generación de la matriz:")
    opcion.pack(pady=10)

    # Generar matriz aleatoria
    generar_aleatorio = tk.Label(estilo_interfaz, text="1. Generar matriz aleatoria")
    generar_aleatorio.pack(pady=5)

    # Ingresar elementos manualmente
    ingresar_manual = tk.Label(estilo_interfaz, text="2. Ingresar elementos manualmente")
    ingresar_manual.pack(pady=5)

    # Entrada de la opción
    entry_opcion = tk.Entry(estilo_interfaz)
    entry_opcion.pack(pady=10)

    # Elementos para el tamaño de la matriz
    tam_matriz = tk.Label(estilo_interfaz, text="Ingrese el tamaño de la matriz [8, 16]:")
    tam_matriz.pack_forget()  

    # Entrada del tamaño de la matriz
    entry_tam = tk.Entry(estilo_interfaz)
    entry_tam.pack_forget() 

    # Confirmación del tamaño de la matriz
    tam_matriz_confirm = tk.Button(estilo_interfaz, text="Ejecutar", 
                                   command=ingreso_tam_matriz)
    tam_matriz_confirm.pack_forget()  

    # Botón de ejecución
    ejecutar = tk.Button(estilo_interfaz, text="Ejecutar", command=manejar_matriz)
    ejecutar.pack(pady=10)

    # Recorrido del ciclo hamiltoniano
    recorrido = tk.Label(estilo_interfaz, text="")
    recorrido.pack_forget() 

    reiniciar_btn = tk.Button(estilo_interfaz, text="Reiniciar", command=reiniciar)
    reiniciar_btn.pack(pady=10)

    # Iniciar la interfaz
    interfaz.mainloop()

# Ejecutar la interfaz
main()