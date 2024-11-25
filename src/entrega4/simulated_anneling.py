import random
import math

def distancia_total(solucao, matriz_distancia):
    distancia = 0
    for i in range(len(solucao)):
        distancia += matriz_distancia[solucao[i - 1]][solucao[i]]
    return distancia

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

matriz_distancias = [
    [0, 10, 15, 20, 10],
    [10, 0, 35, 25, 17],
    [15, 35, 0, 30, 28],
    [20, 25, 30, 0, 11],
    [10, 17, 28, 11, 0]
]

T0 = 1000
SA_MAX = 100
ALPHA = 0.95
T_MIN = 1e-3

melhor_solucao, melhor_custo = simulated_annealing(matriz_distancias, T0, SA_MAX, ALPHA, T_MIN)
print("Melhor solução:", melhor_solucao)
print("Custo da melhor solução:", melhor_custo)
