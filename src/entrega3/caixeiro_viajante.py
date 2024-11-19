import math

class CaixeiroViajante:
    def __init__(self, coordenadas):
        self.coordenadas = coordenadas  
        self.num_cidades = len(coordenadas)
        self.distancias = self.calcular_matriz_distancias()
        self.solucao_atual = [] 
        self.melhor_distancia = float('inf') 

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
        distancia_total += self.distancias[solucao[-1]][solucao[0]]  # Retorna à cidade inicial
        return distancia_total

    def gerar_solucao_inicial_gulosa(self):
        solucao = [0]  
        cidade_atual = 0
        nao_visitadas = list(range(1, self.num_cidades))

        while nao_visitadas:
            cidade_mais_proxima = min(
                nao_visitadas,
                key=lambda cidade: self.distancias[cidade_atual][cidade]
            )
            solucao.append(cidade_mais_proxima)
            nao_visitadas.remove(cidade_mais_proxima)
            cidade_atual = cidade_mais_proxima

        self.solucao_atual = solucao
        self.melhor_distancia = self.avaliar_solucao(self.solucao_atual)


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

tsp.gerar_solucao_inicial_gulosa()
print("Melhor Rota:", tsp.solucao_atual)
print("Menor Distância:", tsp.melhor_distancia)
