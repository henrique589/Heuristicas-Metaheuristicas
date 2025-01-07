import random
import math
import time
from pathlib import Path

TESTE_FILE = Path(__file__).parent / 'mochila_100_1000_1'

T0 = 1000
SA_MAX = 100
ALPHA = 0.95
T_MIN = 1e-3

def carregar_itens(nome_arquivo):
    itens = []
    capacidade = 0
    with open(nome_arquivo, 'r') as arquivo:
        for i, linha in enumerate(arquivo):
            if i == 0:
                _, capacidade = map(int, linha.split()) 
            else:
                valor, peso = map(int, linha.split())
                itens.append((valor, peso))
    return itens, capacidade

def calcular_valor(solucao, itens, capacidade):
    valor_total = 0
    peso_total = 0
    
    for i, selecionado in enumerate(solucao):
        if selecionado == 1:
            valor_total += itens[i][0]
            peso_total += itens[i][1]
    if peso_total > capacidade:
        valor_total -= (peso_total - capacidade) * 100  
    return valor_total

def solucao_inicial(num_itens):
    return [random.randint(0, 1) for _ in range(num_itens)]

def gerar_vizinho(solucao):
    nova_solucao = solucao[:]
    i = random.randint(0, len(solucao) - 1)
    nova_solucao[i] = 1 - nova_solucao[i]  
    return nova_solucao

def simulated_annealing(itens, capacidade, t0, sa_max, alpha, t_min):
    num_itens = len(itens)
    solucao_atual = solucao_inicial(num_itens)
    custo = calcular_valor(solucao_atual, itens, capacidade)
    melhor_solucao = solucao_atual[:]
    melhor_custo = custo
    T = t0

    while T > t_min:
        for _ in range(sa_max):
            nova_solucao = gerar_vizinho(solucao_atual)
            novo_custo = calcular_valor(nova_solucao, itens, capacidade)
            
            if novo_custo > custo or random.random() < math.exp((novo_custo - custo) / T):
                solucao_atual = nova_solucao
                custo = novo_custo
                if custo > melhor_custo:
                    melhor_solucao = solucao_atual
                    melhor_custo = custo
        T *= alpha
    return melhor_solucao, melhor_custo

itens, capacidade = carregar_itens(TESTE_FILE)

for i in range(10):
    start_time = time.time()
    melhor_solucao, melhor_custo = simulated_annealing(itens, capacidade, T0, SA_MAX, ALPHA, T_MIN)
    end_time = time.time()
    tempo_execucao = end_time - start_time

    print(f"Execução {i + 1}:")
    print("Melhor solução:", melhor_solucao)
    print("Melhor custo:", melhor_custo)
    print(f"Tempo de execução: {tempo_execucao:.4f} segundos")