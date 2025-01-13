import random
import time
from pathlib import Path
import json

TESTE_FILE = Path(__file__).parent / 'mochila_100_1000_1'
OUTPUT_FILE = Path(__file__).parent

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

def construir_solucao(itens, capacidade, alpha):
    solucao = []
    capacidade_restante = capacidade
    nao_selecionados = itens[:]

    while nao_selecionados and capacidade_restante > 0:
        candidatos = [
            (i, valor / peso) for i, (peso, valor) in enumerate(nao_selecionados)
            if peso <= capacidade_restante
        ]

        if not candidatos:
            break

        candidatos.sort(key=lambda x: x[1], reverse=True)
        valor_min = candidatos[-1][1]
        valor_max = candidatos[0][1]

        limite = valor_min + alpha * (valor_max - valor_min)
        lrc = [i for i, valor in candidatos if valor >= limite]

        escolhido_idx = random.choice(lrc)
        escolhido = nao_selecionados.pop(escolhido_idx)
        solucao.append(escolhido)
        capacidade_restante -= escolhido[0]

    return solucao

def funcao_avaliacao(solucao):
    valor_total = sum(valor for _, valor in solucao)
    peso_total = sum(peso for peso, _ in solucao)
    return valor_total, peso_total

def busca_local(solucao, itens, capacidade):
    melhor_solucao = solucao[:]
    melhor_valor, _ = funcao_avaliacao(melhor_solucao)

    melhorou = True
    while melhorou:
        melhorou = False
        for item in itens:
            if item not in melhor_solucao and item[0] <= capacidade - sum(peso for peso, _ in melhor_solucao):
                nova_solucao = melhor_solucao + [item]
                novo_valor, _ = funcao_avaliacao(nova_solucao)
                if novo_valor > melhor_valor:
                    melhor_solucao = nova_solucao
                    melhor_valor = novo_valor
                    melhorou = True
    return melhor_solucao

def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_mochila.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

itens, capacidade = carregar_itens(TESTE_FILE)
resultados = []

alpha = 0.8
max_iteracoes = 20
melhor_solucao = None
melhor_custo = 0

for i in range(10):
    start_time = time.time()
    for _ in range(max_iteracoes):
        solucao_inicial = construir_solucao(itens, capacidade, alpha)
        solucao_refinada = busca_local(solucao_inicial, itens, capacidade)
        valor_refinado, _ = funcao_avaliacao(solucao_refinada)

        if valor_refinado > melhor_custo:
            melhor_solucao = solucao_refinada
            melhor_custo = valor_refinado

    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
        "execucao": i + 1,
        "melhor_custo": melhor_custo,
        "tempo_execucao": tempo_execucao,
    }
    resultados.append(resultado)
    salvar_resultados(resultados)

    print(f"Execução {i + 1}:")
    print("Melhor solução:", melhor_solucao)
    print("Melhor custo:", melhor_custo)
    print(f"Tempo de execução: {tempo_execucao:.4f} segundos")