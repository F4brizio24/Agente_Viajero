import tkinter as tk
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Generar matriz aleatoriamente
def generar_matriz(n):
    matriz = np.random.randint(1, 20, size=(n, n))
    matriz = (matriz + matriz.T) // 2
    np.fill_diagonal(matriz, 0)
    return matriz

# Generar matriz manualmente
def mostrar_campos_matriz(n):
    global entradas
    entradas = []
    
    for i in range(n):
        fila_entradas = tk.Frame(estilo_interfaz) 
        fila_entradas.pack(pady=5)  
        fila = []
        
        for j in range(n):
            entrada = tk.Entry(fila_entradas, width=5)
            entrada.pack(side=tk.LEFT) 
            fila.append(entrada)
        entradas.append(fila)

    ejec_matriz = tk.Button(interfaz, text="Ejecutar matriz", command=ejecutar_matriz)
    ejec_matriz.pack(pady=10)

# Ejecuta la matriz ingresada manualmente
def ejecutar_matriz():
    n = len(entradas)
    matriz = np.zeros((n, n), dtype=int)
    
    try:
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                valor = entradas[i][j].get()
                if valor:
                    valor = int(valor)
                    if 0 < valor < 20:
                        matriz[i][j] = valor
                        matriz[j][i] = valor
                    else:
                        print("Los valores deben ser positivos y menores a 20.")
                        return

        matriz = (matriz + matriz.T) // 2
        ejecutar_ciclo(matriz)
    except ValueError:
        print("Por favor, ingrese valores válidos.")

# Calcula las distancias
def calcular_distancia(ciclo, matriz):
    distancia_total = 0
    for i in range(len(ciclo)):
        distancia_total += matriz[ciclo[i]][ciclo[(i + 1) % len(ciclo)]]
    return distancia_total

# Genera las permutaciones para el ciclo hamiltoniano
def generar_permutaciones(nodos, inicio, resultado):
    if inicio == len(nodos) - 1:
        resultado.append(nodos[:])
        return
    
    for i in range(inicio, len(nodos)):
        nodos[inicio], nodos[i] = nodos[i], nodos[inicio]
        generar_permutaciones(nodos, inicio + 1, resultado)
        nodos[inicio], nodos[i] = nodos[i], nodos[inicio]

# Ciclo hamiltoniano
def ciclo_hamiltoniano(matriz):
    n = len(matriz)
    nodos = list(range(n))
    ciclos_posibles = []
    
    generar_permutaciones(nodos, 0, ciclos_posibles)

    mejor_ciclo = None
    mejor_distancia = float('inf')
    
    for ciclo in ciclos_posibles:
        distancia = calcular_distancia(ciclo, matriz)
        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_ciclo = ciclo
            
    return mejor_ciclo, mejor_distancia

# Muestra el grafo en la pantalla
def mostrar_grafo(matriz, ciclo):
    grafo = nx.Graph()
    n = len(matriz)
    
    for i in range(n):
        grafo.add_node(i)
        for j in range(i + 1, n):
            grafo.add_edge(i, j, weight=matriz[i][j])
    
    posicion = nx.spring_layout(grafo)
    nodos = ['red' if i == ciclo[0] else 'lightblue' for i in range(n)]
    nx.draw(grafo, posicion, with_labels=True, node_color=nodos, node_size=800)
    aristas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=aristas)

    arista_marca = [(ciclo[i], ciclo[(i + 1) % len(ciclo)]) for i in range(len(ciclo))]
    nx.draw_networkx_edges(grafo, posicion , edgelist=arista_marca, edge_color='red', 
                             width=2, style='dashed')

    plt.title("Grafo del Agente Viajero")
    plt.show()

# Muestra el ciclo del recorrido hamiltoniano
def ejecutar_ciclo(matriz):
    ciclo, distancia = ciclo_hamiltoniano(matriz)
    ciclo_str = " -> ".join(map(str, ciclo))
    recorrido.config(text=f"Ciclo: {ciclo_str}\nDistancia: {distancia}")
    recorrido.pack(pady=10)
    mostrar_grafo(matriz, ciclo)

# Permite manejar el tamaño de la matriz y ejecutar si es aleatoria o manual
def manejar_matriz():
    op = entry_opcion.get()
    if op in ["1", "2"]:
        tam_matriz.pack(pady=10)
        entry_tam.pack(pady=5)  
        tam_matriz_confirm.pack(pady=10)
    else:
        print("Por favor, ingrese '1' o '2'")

# Ingreso del tamaño y ejecución la matriz
def ingreso_tam_matriz():
    op = entry_opcion.get()
    try:
        n = int(entry_tam.get())
        if 8 <= n <= 16:
            if op == "1":
                ejecutar_ciclo(generar_matriz(n))
            elif op == "2":
                mostrar_campos_matriz(n)
            else:
                print("Opción no válida.")
        else:
            print("El tamaño debe estar entre 8 y 16.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

# Interfaz gráfica con Tkinter
interfaz = tk.Tk()
interfaz.title("El Agente Viajero")
interfaz.geometry("600x400")

estilo_interfaz = tk.Frame(interfaz, width=400, height=300)
estilo_interfaz.pack(pady=10)

titulo = tk.Label(estilo_interfaz, text="Bienvenido al programa del Agente Viajero")
titulo.pack(pady=10)

opcion = tk.Label(estilo_interfaz, text="Ingrese la opción de generación de la matriz:")
opcion.pack(pady=10)

generar_aleatorio = tk.Label(estilo_interfaz, text="1. Generar matriz aleatoria")
generar_aleatorio.pack(pady=5)

ingresar_manual = tk.Label(estilo_interfaz, text="2. Ingresar elementos manualmente")
ingresar_manual.pack(pady=5)

entry_opcion = tk.Entry(estilo_interfaz)
entry_opcion.pack(pady=10)

tam_matriz = tk.Label(estilo_interfaz, text="Ingrese el tamaño de la matriz [8, 16]:")
tam_matriz.pack_forget()  

entry_tam = tk.Entry(estilo_interfaz)
entry_tam.pack_forget() 

tam_matriz_confirm = tk.Button(estilo_interfaz, text="Ejecutar", 
                               command=ingreso_tam_matriz)
tam_matriz_confirm.pack_forget()  

ejecutar = tk.Button(estilo_interfaz, text="Ejecutar", command=manejar_matriz)
ejecutar.pack(pady=10)

recorrido = tk.Label(estilo_interfaz, text="")
recorrido.pack_forget() 

interfaz.mainloop()