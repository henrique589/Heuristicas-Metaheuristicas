import random
import math
import time
from pathlib import Path
import json

TESTE_FILE = Path(__file__).parent / 'tsp_51'
OUTPUT_FILE = Path(__file__).parent

def construir_solucao(distancias, alpha):
    solucao = []
    tam = len(distancias)
    nao_visitados = list(range(tam))
    atual = random.choice(nao_visitados)
    solucao.append(atual)
    nao_visitados.remove(atual)

    while nao_visitados:
        candidatos = [(cidade, distancias[atual][cidade]) for cidade in nao_visitados]
        candidatos.sort(key=lambda x: x[1])
        cus_min = candidatos[0][1]
        cus_max = candidatos[-1][1]

        valor = cus_min + alpha * (cus_max - cus_min)
        lrc = [cidade for cidade, custo in candidatos if custo <= valor]

        prox_cidade = random.choice(lrc)
        solucao.append(prox_cidade)
        nao_visitados.remove(prox_cidade)
        atual = prox_cidade
    return solucao

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

def funcao_avaliacao(solucao, distancias):
    custo_final = 0
    for i in range(len(solucao) - 1):
        custo_final += distancias[solucao[i]][solucao[i+1]]
    custo_final += distancias[solucao[-1]][solucao[0]]
    return custo_final

def busca_local(solucao, distancias):
    solucao_inicial = solucao[:]
    s_best = solucao_inicial
    melhor_custo = funcao_avaliacao(s_best, distancias)

    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(1, len(solucao) - 1):
            for j in range(i + 1, len(solucao)):
                nova_solucao = s_best[:]
                nova_solucao[i:j] = reversed(nova_solucao[i:j])

                novo_custo = funcao_avaliacao(nova_solucao, distancias)

                if novo_custo < melhor_custo:
                    s_best = nova_solucao
                    melhor_custo = novo_custo
                    melhorou = True    
    return s_best, melhor_custo

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_tsp.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

matriz_distancias = construir_matriz_distancias(TESTE_FILE)
resultados = []

alpha = 0.8
max_iteracoes = 20
melhor_solucao = None
custo = float('inf')

for i in range(10):
    start_time = time.time()
    for _ in range(max_iteracoes):
        solucao_inicial = construir_solucao(matriz_distancias, alpha)
        solucao_refinada, custo_refinado = busca_local(solucao_inicial, matriz_distancias)
        if custo_refinado < custo:
            melhor_solucao = solucao_refinada
            custo = custo_refinado
    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
        "execucao": i + 1,
        "melhor_custo": custo,
        "tempo_execucao": tempo_execucao
    }
    resultados.append(resultado)
    salvar_resultados(resultados)

    print("Melhor solução:", melhor_solucao)
    print("Custo da melhor solução:", custo)
    print(f'Tempo de execução: {tempo_execucao:.4f} segundos')    