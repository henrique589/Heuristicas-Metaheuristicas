import random
import math
import time
from pathlib import Path
import json

TESTE_FILE = Path(__file__).parent / 'tsp_51'
OUTPUT_FILE = Path(__file__).parent

T0 = 3000
SA_MAX = 100
ALPHA = 0.8
T_MIN = 1e-3

def distancia_total(solucao, matriz_distancia):
    distancia = 0
    for i in range(len(solucao)):
        distancia += matriz_distancia[solucao[i - 1]][solucao[i]]
    return distancia

def distancia_euclidiana(cidade1, cidade2):
    x1, y1 = cidade1
    x2, y2 = cidade2
    xd = x1 - x2
    yd = y1 - y2
    distancia = math.sqrt(xd * xd + yd * yd)
    return int(distancia + 0.5)

def construir_matriz_distancias(nome_arquivo):
    cidades = []
    
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.split()
            if len(partes) == 3: 
                _, x, y = partes
                cidades.append((int(x), int(y)))
    num_cidades = len(cidades)
    matriz_distancias = [[0] * num_cidades for _ in range(num_cidades)]
    
    for i in range(num_cidades):
        for j in range(num_cidades):
            if i != j:
                matriz_distancias[i][j] = distancia_euclidiana(cidades[i], cidades[j])
    return matriz_distancias

def solucao_inicial(num_cidades):
    solucao = list(range(num_cidades))
    random.shuffle(solucao)
    return solucao

def gerar_vizinho(solucao):
    nova_solucao = solucao[:]
    i, j = random.sample(range(len(solucao)), 2)
    nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
    return nova_solucao

def simulated_annealing(matriz_distancias, t0, sa_max, alpha, t_min):
    num_cidades = len(matriz_distancias)
    solucao_atual = solucao_inicial(num_cidades)
    custo = distancia_total(solucao_atual, matriz_distancias)
    melhor_solucao = solucao_atual[:]
    melhor_custo = custo
    T = t0
    
    while T > t_min:
        for _ in range(sa_max):
            nova_solucao = gerar_vizinho(solucao_atual)
            novo_custo = distancia_total(nova_solucao, matriz_distancias)
            
            if novo_custo < custo or random.random() < math.exp((custo - novo_custo) / T):
                solucao_atual = nova_solucao
                custo = novo_custo
                if custo < melhor_custo:
                    melhor_solucao = solucao_atual
                    melhor_custo = custo 
        T *= alpha  
    return melhor_solucao, melhor_custo

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_tsp.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

matriz_distancias = construir_matriz_distancias(TESTE_FILE)
resultados = []

for i in range(10):
    start_time = time.time()
    melhor_solucao, melhor_custo = simulated_annealing(matriz_distancias, T0, SA_MAX, ALPHA, T_MIN)
    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
        "execucao": i + 1,
        "melhor_custo": melhor_custo,
        "tempo_execucao": tempo_execucao
    }
    resultados.append(resultado)
    salvar_resultados(resultados)

    print("Melhor solução:", melhor_solucao)
    print("Custo da melhor solução:", melhor_custo)
    print(f'Tempo de execução: {tempo_execucao:.4f} segundos')