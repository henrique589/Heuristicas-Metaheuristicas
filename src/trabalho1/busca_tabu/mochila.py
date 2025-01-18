import random
import time
from pathlib import Path
import json

TESTE_FILE = Path(__file__).parent / 'mochila_100_1000_1'
OUTPUT_FILE = Path(__file__).parent

def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    n, wmax = map(int, linhas[0].split())
    itens = [tuple(map(int, linha.split())) for linha in linhas[1:]]
    return n, wmax, itens

def funcao_objetivo(solucao, itens, capacidade, penalidade):
    valor_total = sum(itens[i][0] for i in range(len(solucao)) if solucao[i] == 1)
    peso_total = sum(itens[i][1] for i in range(len(solucao)) if solucao[i] == 1)
    excesso = max(0, peso_total - capacidade)
    return valor_total - penalidade * excesso

def gerar_solucao_inicial(n):
    return [random.choice([0, 1]) for _ in range(n)]

def gerar_vizinhos(solucao):
    vizinhos = []
    for i in range(len(solucao)):
        vizinho = solucao[:]
        vizinho[i] = 1 - vizinho[i]  
        vizinhos.append(vizinho)
    return vizinhos

def busca_tabu(n, capacidade, itens, iteracoes_max, tamanho_tabu, penalidade):
    solucao_atual = gerar_solucao_inicial(n)
    melhor_solucao = solucao_atual[:]
    melhor_valor = funcao_objetivo(melhor_solucao, itens, capacidade, penalidade)
    lista_tabu = []

    for iteracao in range(iteracoes_max):
        vizinhos = gerar_vizinhos(solucao_atual)
        melhores_vizinhos = []

        for vizinho in vizinhos:
            valor = funcao_objetivo(vizinho, itens, capacidade, penalidade)
            if vizinho not in lista_tabu:
                melhores_vizinhos.append((vizinho, valor))

        melhores_vizinhos.sort(key=lambda x: x[1], reverse=True)

        if melhores_vizinhos:
            melhor_vizinho, valor_vizinho = melhores_vizinhos[0]
            solucao_atual = melhor_vizinho

            lista_tabu.append(solucao_atual)
            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0)

            if valor_vizinho > melhor_valor:
                melhor_solucao = solucao_atual[:]
                melhor_valor = valor_vizinho

        print(f"Iteração {iteracao + 1}: Melhor valor = {melhor_valor}")

    return melhor_solucao, melhor_valor

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_mochila.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

n, capacidade, itens = ler_arquivo(TESTE_FILE)

ITERACOES_MAX = 50
TAMANHO_TABU = 5
PENALIDADE = 10 

start_time = time.time()
melhor_solucao, melhor_valor = busca_tabu(n, capacidade, itens, ITERACOES_MAX, TAMANHO_TABU, PENALIDADE)
end_time = time.time()
tempo_execucao = end_time - start_time

resultado = {
        "melhor_custo": melhor_valor,
        "tempo_execucao": tempo_execucao,
    }
salvar_resultados(resultado)

print("\nMelhor solução encontrada:")
print(f"Itens selecionados: {melhor_solucao}")
print(f"Valor total: {melhor_valor}")
