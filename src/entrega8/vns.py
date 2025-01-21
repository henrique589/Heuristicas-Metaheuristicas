import math
import random
from pathlib import Path

ARQUIVO_TESTE = Path(__file__).parent / 'tsp_5'

def distancia_euclidiana(cidade1, cidade2):
    xd = cidade1[0] - cidade2[0]
    yd = cidade1[1] - cidade2[1]
    return int(math.sqrt(xd ** 2 + yd ** 2) + 0.5)

def calcular_custo_total(rota, cidades):
    custo = 0
    for i in range(len(rota)):
        custo += distancia_euclidiana(cidades[rota[i]], cidades[rota[(i + 1) % len(rota)]]);
    return custo

def busca_local(rota, cidades):
    melhor_rota = rota[:]
    melhor_custo = calcular_custo_total(rota, cidades)

    for i in range(len(rota) - 1):
        for j in range(i + 1, len(rota)):
            nova_rota = rota[:i] + rota[i:j + 1][::-1] + rota[j + 1:]
            novo_custo = calcular_custo_total(nova_rota, cidades)
            if novo_custo < melhor_custo:
                melhor_rota, melhor_custo = nova_rota, novo_custo
    return melhor_rota, melhor_custo

def alterar_vizinhanca(rota):
    nova_rota = rota[:]
    i, j = random.sample(range(len(rota)), 2)
    nova_rota[i], nova_rota[j] = nova_rota[j], nova_rota[i]
    return nova_rota

def vns(cidades, maximo_sem_melhora):
    n = len(cidades)
    rota_atual = list(range(n))
    random.shuffle(rota_atual)
    custo_atual = calcular_custo_total(rota_atual, cidades)

    melhor_rota, melhor_custo = rota_atual[:], custo_atual
    contador_sem_melhora = 0

    while contador_sem_melhora < maximo_sem_melhora:
        k = 1 

        while k <= n:
            nova_rota = alterar_vizinhanca(rota_atual)

            rota_local, custo_local = busca_local(nova_rota, cidades)

            if custo_local < custo_atual:
                rota_atual, custo_atual = rota_local, custo_local
                if custo_atual < melhor_custo:
                    melhor_rota, melhor_custo = rota_atual[:], custo_atual
                    contador_sem_melhora = 0  
                break
            else:
                k += 1

        contador_sem_melhora += 1

    return melhor_rota, melhor_custo

def carregar_cidades(nome_arquivo):
    cidades = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.split()
            if len(partes) == 3:
                _, x, y = map(int, partes)
                cidades.append((x, y))
    return cidades

cidades = carregar_cidades(ARQUIVO_TESTE)
maximo_sem_melhora = 100

melhor_rota, melhor_custo = vns(cidades, maximo_sem_melhora)

print("Melhor rota:", melhor_rota)
print("Custo da melhor rota:", melhor_custo)
