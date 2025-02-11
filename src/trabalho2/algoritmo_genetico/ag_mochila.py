import random
import time
from pathlib import Path
import json

ARQUIVO_TESTE = Path(__file__).parent / 'mochila_100_1000_1'
OUTPUT_FILE = Path(__file__).parent

class Item:
    def __init__(self, lucro, peso):
        self.lucro = lucro
        self.peso = peso

class MochilaAG:
    def __init__(self, itens, capacidade, tamanho_populacao, geracoes, taxa_crossover, taxa_mutacao):
        self.itens = itens
        self.capacidade = capacidade
        self.tamanho_populacao = tamanho_populacao
        self.geracoes = geracoes
        self.taxa_crossover = taxa_crossover
        self.taxa_mutacao = taxa_mutacao

    def gerar_populacao(self):
        populacao = []
        while len(populacao) < self.tamanho_populacao:
            individuo = [random.randint(0, 1) for _ in range(len(self.itens))]
            if self.calcular_aptidao(individuo) > 0:  
                populacao.append(individuo)
        return populacao

    def calcular_aptidao(self, individuo):
        lucro_total = 0
        peso_total = 0
        for i in range(len(individuo)):
            if individuo[i] == 1:
                lucro_total += self.itens[i].lucro
                peso_total += self.itens[i].peso
        
        if peso_total > self.capacidade:
            return lucro_total * (self.capacidade / peso_total)  
        return lucro_total

    def selecao(self, populacao):
        valores_aptidao = [self.calcular_aptidao(ind) for ind in populacao]
        if sum(valores_aptidao) == 0:  
            return random.choice(populacao)  

        return random.choices(populacao, weights=valores_aptidao, k=1)[0] 

    def crossover(self, pai1, pai2):
        if random.random() < self.taxa_crossover:
            ponto = random.randint(1, len(pai1) - 1)
            return pai1[:ponto] + pai2[ponto:], pai2[:ponto] + pai1[ponto:]
        return pai1, pai2

    def mutacao(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                individuo[i] = 1 - individuo[i]
        return individuo

    def evoluir(self, populacao):
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
        populacao = self.gerar_populacao()
        melhor_solucao = None
        melhor_aptidao = 0
        geracoes_sem_melhoria = 0

        for geracao in range(self.geracoes):
            populacao = self.evoluir(populacao)
            for individuo in populacao:
                aptidao = self.calcular_aptidao(individuo)
                if aptidao > melhor_aptidao:
                    melhor_aptidao = aptidao
                    melhor_solucao = individuo
                    geracoes_sem_melhoria = 0  
                else:
                    geracoes_sem_melhoria += 1

            if geracoes_sem_melhoria >= 20: 
                break

        return melhor_solucao, melhor_aptidao

def carregar_instancia_mochila(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
        n, capacidade = map(int, linhas[0].split())
        itens = []
        for linha in linhas[1:]:
            lucro, peso = map(int, linha.split())
            itens.append(Item(lucro, peso))
        return itens, capacidade
    
def salvar_resultados(resultados):
    with open(f'{OUTPUT_FILE}/resultados_mochila.json', "w") as jsonfile:
        json.dump(resultados, jsonfile, indent=4)

itens, capacidade = carregar_instancia_mochila(ARQUIVO_TESTE)
resultados = []

tamanho_populacao = 300
geracoes = 1000
taxa_crossover = 0.95
taxa_mutacao = 0.1

for i in range(10):
    start_time = time.time()
    mochila_ag = MochilaAG(itens, capacidade, tamanho_populacao, geracoes, taxa_crossover, taxa_mutacao)
    solucao, lucro_maximo = mochila_ag.executar()
    end_time = time.time()
    tempo_execucao = end_time - start_time

    resultado = {
            "execucao": i + 1,
            "lucro_maximo": lucro_maximo,
            "tempo_execucao": tempo_execucao,
        }
    resultados.append(resultado)
    salvar_resultados(resultados)

    print()
    print("Melhor solução:", solucao)
    print("Lucro máximo:", lucro_maximo)
    print("Tempo de Execução:", tempo_execucao)
