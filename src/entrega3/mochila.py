class Mochila:
    def __init__(self, capacidade, itens):
        self.capacidade = capacidade
        self.itens = itens
        self.solucao_atual = [0] * len(itens)
        self.peso_atual = 0
        self.valor_atual = 0

    def gerar_solucao_gulosa_custo_beneficio(self):
        itens_ordenados = sorted(self.itens, key=lambda x: x['valor'] / x['peso'], reverse=True)
        solucao = [0] * len(self.itens)
        capacidade_restante = self.capacidade

        for item in itens_ordenados:
            indice = self.itens.index(item) 
            if item['peso'] <= capacidade_restante:
                solucao[indice] = 1
                capacidade_restante -= item['peso']

        self.solucao_atual = solucao
        self.peso_atual = sum(item['peso'] for i, item in enumerate(self.itens) if solucao[i] == 1)
        self.valor_atual = sum(item['valor'] for i, item in enumerate(self.itens) if solucao[i] == 1)

        return self.solucao_atual, self.valor_atual, self.peso_atual

def ler_arquivo_mochila(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        primeira_linha = arquivo.readline().strip().split()
        capacidade = int(primeira_linha[1])

        itens = []
        for linha in arquivo:
            valor, peso = map(int, linha.strip().split())
            itens.append({'valor': valor, 'peso': peso})

    return Mochila(capacidade, itens)

mochila = ler_arquivo_mochila("mochila_4_20")

solucao, valor, peso = mochila.gerar_solucao_gulosa_custo_beneficio()

print("Solução Gulosa (Custo-Benefício):", solucao)
print("Valor Total:", valor)
print("Peso Total:", peso)
