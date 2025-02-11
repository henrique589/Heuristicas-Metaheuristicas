import numpy as np
import random
import time
import math
import json
from pathlib import Path

ARQUIVO_TESTE = Path(__file__).parent / 'tsp_51'
OUTPUT_FILE = Path(__file__).parent

# Carregar os dados das cidades
def load_cities():
    cities = []
    with open(ARQUIVO_TESTE, "r") as file:
        for line in file:
            _, x, y = map(int, line.split())
            cities.append((x, y))
    return np.array(cities)

# Calcular matriz de distâncias
def compute_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                xd = cities[i][0] - cities[j][0]
                yd = cities[i][1] - cities[j][1]
                distance_matrix[i][j] = int(math.sqrt(xd * xd + yd * yd) + 0.5)
    return distance_matrix

# Inicializar trilhas de feromônio
def initialize_pheromones(num_cities, tau_0=1.0):
    return np.full((num_cities, num_cities), tau_0)

# Escolha da próxima cidade via método da roleta
def select_next_city(probabilities):
    return np.random.choice(len(probabilities), p=probabilities)

# Atualização dos feromônios
def update_pheromones(pheromones, ant_paths, distances, rho=0.1, Q=100):
    pheromones *= (1 - rho)  # Evaporação
    for path, length in zip(ant_paths, distances):
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            pheromones[a][b] += Q / length
            pheromones[b][a] += Q / length

def ant_colony_tsp(num_ants, num_iterations, alpha=1.0, beta=2.0, rho=0.1, Q=100):
    cities = load_cities()
    num_cities = len(cities)
    distance_matrix = compute_distance_matrix(cities)
    pheromones = initialize_pheromones(num_cities)

    best_distance = float("inf")
    best_path = None
    
    for iteration in range(num_iterations):
        ant_paths = []
        distances = []
        
        for ant in range(num_ants):
            visited = [random.randint(0, num_cities - 1)]
            
            while len(visited) < num_cities:
                current = visited[-1]
                probabilities = []
                total = 0
                
                for j in range(num_cities):
                    if j not in visited:
                        tau_eta = (pheromones[current][j] ** alpha) * ((1.0 / distance_matrix[current][j]) ** beta)
                        probabilities.append(tau_eta)
                        total += tau_eta
                    else:
                        probabilities.append(0)
                
                probabilities = np.array(probabilities) / total
                next_city = select_next_city(probabilities)
                visited.append(next_city)
            
            visited.append(visited[0]) 
            path_distance = sum(distance_matrix[visited[i]][visited[i+1]] for i in range(num_cities))
            
            if path_distance < best_distance:
                best_distance = path_distance
                best_path = visited
            
            ant_paths.append(visited)
            distances.append(path_distance)
        
        update_pheromones(pheromones, ant_paths, distances, rho, Q)
        # print(f"Iteração {iteration + 1}: Melhor distância encontrada = {best_distance}")
    
    return best_path, best_distance

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_tsp.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

resultados = []

for i in range(10):
    start_time = time.time()
    best_path, best_distance = ant_colony_tsp(num_ants=200, num_iterations=20)
    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
        "execucao": i + 1,
        "melhor_distancia": best_distance,
        "tempo_execucao": tempo_execucao,
    }
    resultados.append(resultado)
    salvar_resultados(resultados)

    print()
    print("Melhor Caminho:", best_path)
    print("Melhor Distância:", best_distance)
    print("Tempo de Execução:", tempo_execucao)
