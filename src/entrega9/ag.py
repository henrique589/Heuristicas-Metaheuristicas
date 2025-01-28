import random
from pathlib import Path

ARQUIVO_TESTE = Path(__file__).parent / 'mochila_4_20'

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
        return [[random.randint(0, 1) for _ in range(len(self.itens))] for _ in range(self.tamanho_populacao)]

    def calcular_aptidao(self, individuo):
        lucro_total = 0
        peso_total = 0
        for i in range(len(individuo)):
            if individuo[i] == 1:
                lucro_total += self.itens[i].lucro
                peso_total += self.itens[i].peso
                if peso_total > self.capacidade:
                    return 0 
        return lucro_total

    def selecao(self, populacao):
        valores_aptidao = [self.calcular_aptidao(ind) for ind in populacao]
        soma_aptidao = sum(valores_aptidao)
        if soma_aptidao == 0:
            return random.choice(populacao) 
        probabilidades = [f / soma_aptidao for f in valores_aptidao]
        indice_selecionado = random.choices(range(len(populacao)), weights=probabilidades, k=1)[0]
        return populacao[indice_selecionado]

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

        for geracao in range(self.geracoes):
            populacao = self.evoluir(populacao)
            for individuo in populacao:
                aptidao = self.calcular_aptidao(individuo)
                if aptidao > melhor_aptidao:
                    melhor_aptidao = aptidao
                    melhor_solucao = individuo

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
itens, capacidade = carregar_instancia_mochila(ARQUIVO_TESTE)

tamanho_populacao = 50
geracoes = 100
taxa_crossover = 0.8
taxa_mutacao = 0.05

mochila_ag = MochilaAG(itens, capacidade, tamanho_populacao, geracoes, taxa_crossover, taxa_mutacao)
solucao, lucro_maximo = mochila_ag.executar()

print("Melhor solução:", solucao)
print("Lucro máximo:", lucro_maximo)
