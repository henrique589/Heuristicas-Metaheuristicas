MAX_ITERACOES = 100

class Mochila:
    def __init__(self, capacidade, itens, num_itens):
        self.capacidade = capacidade
        self.itens = itens
        self.solucao_atual = [0] * len(itens)
        self.peso_atual = 0
        self.valor_atual = 0
        self.iteracao_atual = 0  
        self.num_itens = num_itens

    def avaliar_solucao(self, solucao):
        peso_final = 0
        valor_final = 0

        for i, item in enumerate(self.itens):
            if solucao[i] == 1:
                peso_final += item['peso']
                valor_final += item['valor']

        if peso_final > self.capacidade:
            return 0  
        else:
            return valor_final

    def gerar_solucao_inicial(self):
        self.solucao_atual = [0] * len(self.itens)
        self.peso_atual = 0
        self.valor_atual = 0

    def flip(self, solucao, indice):
        nova_solucao = solucao[:]
        nova_solucao[indice] = 1 - nova_solucao[indice]
        return nova_solucao

    def criterio_parada(self):
        return self.iteracao_atual >= MAX_ITERACOES

    def busca_local(self):
        self.gerar_solucao_inicial()  
        melhorou = True

        while not self.criterio_parada() and melhorou:
            melhorou = False
            melhor_valor_vizinho = self.valor_atual
            melhor_vizinho = self.solucao_atual

            for i in range(len(self.itens)):
                # Gera uma nova solução vizinha aplicando o flip
                solucao_vizinha = self.flip(self.solucao_atual, i)
                valor_vizinho = self.avaliar_solucao(solucao_vizinha)

                # Verifica se o vizinho é uma solução melhor
                if valor_vizinho > melhor_valor_vizinho and sum(solucao_vizinha) <= self.num_itens:
                    peso_vizinho = sum(item['peso'] for j, item in enumerate(self.itens) if solucao_vizinha[j] == 1)
                    if peso_vizinho <= self.capacidade:
                        melhor_vizinho = solucao_vizinha
                        melhor_valor_vizinho = valor_vizinho
                        melhorou = True

            # Atualiza para o melhor vizinho encontrado
            self.solucao_atual = melhor_vizinho
            self.valor_atual = melhor_valor_vizinho
            self.peso_atual = sum(item['peso'] for j, item in enumerate(self.itens) if self.solucao_atual[j] == 1)

            self.iteracao_atual += 1 

        return self.solucao_atual, self.valor_atual


def ler_arquivo_mochila(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        primeira_linha = arquivo.readline().strip().split()
        num_itens = int(primeira_linha[0])
        capacidade = int(primeira_linha[1])

        itens = []
        for linha in arquivo:
            valor, peso = map(int, linha.strip().split())
            itens.append({'valor': valor, 'peso': peso})

    return Mochila(capacidade, itens, num_itens)

    
mochila = ler_arquivo_mochila("mochila_4_20")

melhor_solucao, valor_melhor_solucao = mochila.busca_local()

print("Melhor Solução:", melhor_solucao)
print("Valor da Melhor Solução:", valor_melhor_solucao)
print("Peso Total:", mochila.peso_atual)
print("Número de Itens Selecionados:", sum(melhor_solucao))
