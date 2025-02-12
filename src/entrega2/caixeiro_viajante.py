import random
import math

class CaixeiroViajante:
    def __init__(self, coordenadas, max_iteracoes=1000):
        self.coordenadas = coordenadas  
        self.num_cidades = len(coordenadas)
        self.max_iteracoes = max_iteracoes
        self.distancias = self.calcular_matriz_distancias()
        self.solucao_atual = list(range(self.num_cidades))
        random.shuffle(self.solucao_atual) 
        self.melhor_distancia = self.avaliar_solucao(self.solucao_atual)
        self.iteracao_atual = 0

    def calcular_matriz_distancias(self):
        distancias = [[0] * self.num_cidades for _ in range(self.num_cidades)]
        for i in range(self.num_cidades):
            for j in range(i + 1, self.num_cidades):
                xd = self.coordenadas[i][0] - self.coordenadas[j][0]
                yd = self.coordenadas[i][1] - self.coordenadas[j][1]
                distancia = math.sqrt(xd * xd + yd * yd)
                distancias[i][j] = distancias[j][i] = int(distancia + 0.5)
        return distancias

    def avaliar_solucao(self, solucao):
        distancia_total = 0
        for i in range(len(solucao) - 1):
            distancia_total += self.distancias[solucao[i]][solucao[i + 1]]
        distancia_total += self.distancias[solucao[-1]][solucao[0]]  
        return distancia_total

    def gerar_solucao_inicial(self):
        self.solucao_atual = list(range(self.num_cidades))
        random.shuffle(self.solucao_atual)
        self.melhor_distancia = self.avaliar_solucao(self.solucao_atual)

    def criterio_parada(self):
        return self.iteracao_atual >= self.max_iteracoes

    def troca_2_opt(self, solucao, i, j):
        nova_solucao = solucao[:]
        nova_solucao[i:j + 1] = reversed(nova_solucao[i:j + 1])
        return nova_solucao

    def busca_local(self):
        self.gerar_solucao_inicial() 
        melhorou = True

        while not self.criterio_parada() and melhorou:
            melhorou = False

            for i in range(1, self.num_cidades - 1):
                for j in range(i + 1, self.num_cidades):
                    solucao_vizinha = self.troca_2_opt(self.solucao_atual, i, j)
                    distancia_vizinha = self.avaliar_solucao(solucao_vizinha)

                    if distancia_vizinha < self.melhor_distancia:
                        self.solucao_atual = solucao_vizinha
                        self.melhor_distancia = distancia_vizinha
                        melhorou = True
                        break  
                if melhorou:
                    break

            self.iteracao_atual += 1

        return self.solucao_atual, self.melhor_distancia

def ler_arquivo_coordenadas(nome_arquivo):
    coordenadas = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()
            if len(partes) == 3: 
                _, x, y = map(int, partes)
                coordenadas.append((x, y))
    return coordenadas

coordenadas = ler_arquivo_coordenadas("tsp_5")
tsp = CaixeiroViajante(coordenadas)

melhor_rota, menor_distancia = tsp.busca_local()

print("Melhor Rota:", melhor_rota)
print("Menor Distância:", menor_distancia)
