import time
from Grafo import Grafo

def permutacao_com_grafo(grafo: Grafo, n: int):
    solucao = []

    def backtrack():
        # Caso base: se o caminho contém todas as cidades
        if len(solucao) == n:
            print(solucao)
            return
        
        for prox_cidade in range(n):
            # Verifica se a cidade ainda não foi visitada
            if prox_cidade not in solucao:
                # Verifica se há uma conexão entre a última cidade do caminho e a próxima cidade
                if not solucao or grafo.matriz_adjacencia[solucao[-1]][prox_cidade] != 0:
                    solucao.append(prox_cidade)
                    backtrack()
                    solucao.pop()  # Backtrack para explorar outras possibilidades

    # Medir o tempo de execução
    start_time = time.time()
    backtrack()
    end_time = time.time()
    print(f'Tempo de processamento = {end_time - start_time:.4f} segundos')

# Leitura do arquivo de entrada para criar o grafo
grafo = None
with open('in.txt', 'r') as f:
    for idx, line in enumerate(f):
        nodes = line.strip().split()
        if idx == 0:
            grafo = Grafo(nodes[0])  # Inicializa o grafo com o número de vértices (cidades)
        else:
            grafo.add_aresta(nodes[0], nodes[1], nodes[2])

# Exibir a matriz de adjacência para verificação (opcional)
grafo.visualizar_matriz()

# Número de cidades no grafo
n = grafo.vertices
permutacao_com_grafo(grafo, n)
