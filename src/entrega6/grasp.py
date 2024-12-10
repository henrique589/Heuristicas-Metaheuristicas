import random

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

def main():
    distancias = [
        [0, 65, 66, 43, 52],  
        [65, 0, 15, 49, 11], 
        [66, 15, 0, 54, 20],  
        [43, 49, 54, 0, 24], 
        [52, 11, 20, 24, 0]   
    ]

    alpha = 0.5
    max_iteracoes = 10

    melhor_solucao = None
    menor_custo = float('inf')

    for _ in range(max_iteracoes):
        solucao_inicial = construir_solucao(distancias, alpha)

        solucao_refinada, custo_refinado = busca_local(solucao_inicial, distancias)

        if custo_refinado < menor_custo:
            melhor_solucao = solucao_refinada
            menor_custo = custo_refinado

    print("Melhor solução encontrada:", melhor_solucao)
    print("Custo da melhor solução:", menor_custo)

main()