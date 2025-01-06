import random

ILSMax = 1000

def gerar_solucao_inicial(n):
    solucao = list(range(n))
    random.shuffle(solucao)
    return solucao

def calcular_distancia_total(matriz_distancias, solucao):
    distancia_total = 0
    n = len(matriz_distancias)
    for i in range(n):
        distancia_total += matriz_distancias[solucao[i]][solucao[(i + 1) % n]]
    return distancia_total

def busca_local(matriz_distancias, solucao):
    n = len(solucao)
    melhor_solucao = solucao[:]
    melhor_distancia = calcular_distancia_total(matriz_distancias, melhor_solucao)

    melhor_encontrado = True

    while melhor_encontrado:
        melhor_encontrado = False
        melhor_distancia_atual = melhor_distancia

        for i in range(n):
            for j in range(i + 1, n):
                nova_solucao = melhor_solucao[:]
                nova_solucao[i:j + 1] = reversed(nova_solucao[i:j + 1])

                nova_distancia = calcular_distancia_total(matriz_distancias, nova_solucao)

                if nova_distancia < melhor_distancia_atual:
                    melhor_distancia_atual = nova_distancia
                    melhor_solucao = nova_solucao[:]
                    melhor_encontrado = True

        melhor_distancia = melhor_distancia_atual
    return melhor_solucao, melhor_distancia 

def perturbacao(solucao, d):
    n = len(solucao)
    nova_solucao = solucao[:]

    for _ in range(d):
        i, j = random.sample(range(n), 2)
        nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]
    return nova_solucao

def ils(matriz_distancias, n):
    s0 = gerar_solucao_inicial(n)
    s, melhor_distancia = busca_local(matriz_distancias, s0)
    melhor_solucao = s[:]
    iter = 0
    d = 1
    while iter < ILSMax:
        iter += 1
        s1 = perturbacao(s, d)
        s2, nova_distancia = busca_local(matriz_distancias, s1)
        if nova_distancia < melhor_distancia:
            melhor_solucao = s2[:]
            melhor_distancia = nova_distancia
            s = s2[:]
            iter = 0
            d = 1
        else:
            d += 1
    return melhor_solucao, melhor_distancia

def ler_matriz_distancias_do_arquivo(nome_arquivo):
    matriz_distancias = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            distancias = list(map(int, linha.split()))
            matriz_distancias.append(distancias)
    return matriz_distancias

if __name__ == "__main__":
    nome_arquivo = 'in.txt'
    matriz_distancias = ler_matriz_distancias_do_arquivo(nome_arquivo)
    n = len(matriz_distancias)
    
    solucao, distancia = ils(matriz_distancias, n)
    print(f'Solução: {solucao}, Distância: {distancia}')