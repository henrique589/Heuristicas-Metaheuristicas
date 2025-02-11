import random
import time
import json
from pathlib import Path
import math

ARQUIVO_TESTE = Path(__file__).parent / 'tsp_51'
OUTPUT_FILE = Path(__file__).parent

def nint(x):
    # Arredonda para o inteiro mais próximo (equivalente a nint no enunciado
    return int(x + 0.5)

class Cidade:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, outra):
        # Calcula a distância euclidiana arredondada entre duas cidades
        xd = self.x - outra.x
        yd = self.y - outra.y
        return nint(math.sqrt(xd * xd + yd * yd))  # Usa nint para garantir valores inteiros

class CaixeiroViajanteAG:
    def __init__(self, cidades, tamanho_populacao, geracoes, taxa_crossover, taxa_mutacao):
        self.cidades = cidades
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao

    def gerar_populacao(self):
        #Cria uma população inicial com permutações aleatórias das cidades
        return [random.sample(self.cidades, len(self.cidades)) for _ in range(self.tamanho_populacao)]

    def calcular_aptidao(self, individuo):
        # Calcula a aptidão como a distância total percorrida na rota
        distancia_total = sum(individuo[i].distancia(individuo[i + 1]) for i in range(len(individuo) - 1))
        distancia_total += individuo[-1].distancia(individuo[0])  # Retorno à cidade inicial
        return 1 / distancia_total  # Quanto menor a distância, maior a aptidão

    def selecao(self, populacao):
        #Usa torneio para selecionar um pai
        torneio = random.sample(populacao, 3)
        return max(torneio, key=self.calcular_aptidao)

    def crossover(self, pai1, pai2):
        # Realiza o crossover ordenado (OX) para manter a validade da permutação
        if random.random() < self.taxa_crossover:
            ponto1, ponto2 = sorted(random.sample(range(len(pai1)), 2))
            filho1 = pai1[ponto1:ponto2]
            filho2 = pai2[ponto1:ponto2]

            resto1 = [c for c in pai2 if c not in filho1]
            resto2 = [c for c in pai1 if c not in filho2]

            filho1 = resto1[:ponto1] + filho1 + resto1[ponto1:]
            filho2 = resto2[:ponto1] + filho2 + resto2[ponto1:]

            return filho1, filho2
        return pai1, pai2

    def mutacao(self, individuo):
        #Realiza mutação por inversão em uma parte da rota
        if random.random() < self.taxa_mutacao:
            ponto1, ponto2 = sorted(random.sample(range(len(individuo)), 2))
            individuo[ponto1:ponto2] = reversed(individuo[ponto1:ponto2])
        return individuo

    def evoluir(self, populacao):
        # Cria uma nova população aplicando seleção, crossover e mutação
        nova_populacao = []
        while len(nova_populacao) < self.tamanho_populacao:
            pai1 = self.selecao(populacao)
            pai2 = self.selecao(populacao)
            filho1, filho2 = self.crossover(pai1, pai2)
            nova_populacao.append(self.mutacao(filho1))
            if len(nova_populacao) < self.tamanho_populacao:
                nova_populacao.append(self.mutacao(filho2))
        return nova_populacao

    def executar(self):
        # Executa o Algoritmo Genético para otimizar a rota do Caixeiro Viajante
        populacao = self.gerar_populacao()
        melhor_solucao = None
        melhor_aptidao = float('-inf')
        geracoes_sem_melhoria = 0

        for _ in range(self.geracoes):
            populacao = self.evoluir(populacao)
            for individuo in populacao:
                aptidao = self.calcular_aptidao(individuo)
                if aptidao > melhor_aptidao:
                    melhor_aptidao = aptidao
                    melhor_solucao = individuo
                    geracoes_sem_melhoria = 0
                else:
                    geracoes_sem_melhoria += 1

            if geracoes_sem_melhoria >= 20:  # Critério de parada
                break

        return melhor_solucao, 1 / melhor_aptidao  # Retorna a melhor solução e a menor distância

def carregar_instancia_tsp(caminho_arquivo):
    # Carrega os dados das cidades a partir do arquivo de entrada, ignorando informações iniciais.
    with open(caminho_arquivo, 'r') as f:
        cidades = []
        for linha in f:
            partes = linha.strip().split()
            if len(partes) == 3:
                _, x, y = map(float, partes)  # Ignora o primeiro número (índice da cidade)
                cidades.append(Cidade(x, y))
        return cidades

def salvar_resultados(resultados):
    """Salva os resultados em um arquivo JSON."""
    with open(f'{OUTPUT_FILE}/resultados_tsp.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

# Parâmetros do Algoritmo Genético
tamanho_populacao = 300
geracoes = 1000
taxa_crossover = 0.95
taxa_mutacao = 0.1

# Carregar instância do problema
cidades = carregar_instancia_tsp(ARQUIVO_TESTE)
resultados = []

# Executar múltiplas vezes para avaliar consistência
for i in range(10):
    start_time = time.time()
    tsp_ag = CaixeiroViajanteAG(cidades, tamanho_populacao, geracoes, taxa_crossover, taxa_mutacao)
    solucao, menor_distancia = tsp_ag.executar()
    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
        "execucao": i + 1,
        "menor_distancia": menor_distancia,
        "tempo_execucao": tempo_execucao,
    }
    resultados.append(resultado)
    salvar_resultados(resultados)

    # Exibir solução de maneira mais clara:
    print(f"\nExecução {i + 1}:")
    print(f"Menor distância percorrida: {menor_distancia}")
    print(f"Tempo de Execução: {tempo_execucao:.4f} segundos")
    print("Melhor rota encontrada:")
    print(" → ".join(f"({cidade.x:.0f}, {cidade.y:.0f})" for cidade in solucao))
