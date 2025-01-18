import random
import math
import time
from pathlib import Path
import json

TESTE_FILE = Path(__file__).parent / 'tsp_51'
OUTPUT_FILE = Path(__file__).parent

def ler_arquivo_tsp(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    cidades = []
    for linha in linhas:
        _, x, y = map(float, linha.split())
        cidades.append((x, y))
    return cidades

def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0]) ** 2 + (cidade1[1] - cidade2[1]) ** 2)

def funcao_objetivo_tsp(solucao, cidades):
    custo_total = 0
    for i in range(len(solucao) - 1):
        custo_total += distancia(cidades[solucao[i]], cidades[solucao[i + 1]])
    custo_total += distancia(cidades[solucao[-1]], cidades[solucao[0]])
    return custo_total

def gerar_solucao_inicial_tsp(n):
    solucao = list(range(n))
    random.shuffle(solucao)
    return solucao

def gerar_vizinhos_tsp(solucao):
    vizinhos = []
    for i in range(len(solucao)):
        for j in range(i + 1, len(solucao)):
            vizinho = solucao[:]
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]  
            vizinhos.append(vizinho)
    return vizinhos

def busca_tabu_tsp(cidades, iteracoes_max, tamanho_tabu):
    n = len(cidades)
    solucao_atual = gerar_solucao_inicial_tsp(n)
    melhor_solucao = solucao_atual[:]
    melhor_custo = funcao_objetivo_tsp(melhor_solucao, cidades)
    lista_tabu = []

    for iteracao in range(iteracoes_max):
        vizinhos = gerar_vizinhos_tsp(solucao_atual)
        melhores_vizinhos = []

        for vizinho in vizinhos:
            custo = funcao_objetivo_tsp(vizinho, cidades)
            if vizinho not in lista_tabu:
                melhores_vizinhos.append((vizinho, custo))

        melhores_vizinhos.sort(key=lambda x: x[1])

        if melhores_vizinhos:
            melhor_vizinho, custo_vizinho = melhores_vizinhos[0]
            solucao_atual = melhor_vizinho

            lista_tabu.append(solucao_atual)
            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0)

            if custo_vizinho < melhor_custo:
                melhor_solucao = solucao_atual[:]
                melhor_custo = custo_vizinho

        print(f"Iteração {iteracao + 1}: Melhor custo = {melhor_custo:.2f}")

    return melhor_solucao, melhor_custo

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_tsp.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

cidades = ler_arquivo_tsp(TESTE_FILE)
ITERACOES_MAX = 50
TAMANHO_TABU = 5

start_time = time.time()
melhor_solucao, melhor_custo = busca_tabu_tsp(cidades, ITERACOES_MAX, TAMANHO_TABU)
end_time = time.time()
tempo_execucao = end_time - start_time

resultado = {
    "melhor_custo": melhor_custo,
    "tempo_execucao": tempo_execucao
}
salvar_resultados(resultado)

print("\nMelhor solução encontrada:")
print(f"Rota: {melhor_solucao}")
print(f"Custo total: {melhor_custo:.2f}")
print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
