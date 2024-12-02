def gerar_solucao_gulosa(itens, capacidade):
    solucao = [0] * len(itens)
    temp = []
    peso_atual = 0

    for index, item in enumerate(itens):
        valor, peso = item
        valor_relativo = valor / peso
        tupla = (index, valor, peso, valor_relativo)
        temp.append(tupla)
    temp.sort(key=lambda x: x[3], reverse=True)
    
    for item in temp:
        index, valor, peso, valor_relativo = item
        if peso_atual + peso <= capacidade:
            solucao[index] = 1
            peso_atual += peso
    
    return solucao

def avalia_solucao(solucao, itens):
    valor_total = 0
    peso_total = 0

    for index, item in enumerate(itens):
        valor, peso = item
        if solucao[index]:
            valor_total += valor
            peso_total += peso
    
    return peso_total, valor_total

def gerar_vizinhos(solucao, itens, capacidade):
    vizinhos = []

    for index in range(len(solucao)):
        nova_solucao = solucao[:]
        
        nova_solucao[index] = 1 - solucao[index]

        peso_total = sum(itens[i][1] for i in range(len(itens)) if nova_solucao[i] == 1)

        if peso_total <= capacidade:
            vizinhos.append(nova_solucao)
    
    return vizinhos

def selecionar_melhor_vizinho(vizinhos, itens, lista_tabu, s_best, valor_s_best):
    """
    Seleciona o melhor vizinho, considerando a lista tabu e os critérios de aspiração.

    Parâmetros:
    - vizinhos: Lista de soluções vizinhas (vetores binários).
    - itens: Lista de tuplas (valor, peso), representando os itens disponíveis.
    - lista_tabu: Lista tabu atual, contendo os movimentos proibidos.
    - s_best: Melhor solução global encontrada até agora.
    - valor_s_best: Valor da melhor solução global.
    
    Retorno:
    - melhor_vizinho: O melhor vizinho selecionado.
    - valor_melhor_vizinho: O valor total do melhor vizinho selecionado.
    """
    melhor_vizinho = None
    valor_melhor_vizinho = 0
    movimento_escolhido = None

    for vizinho in vizinhos:
        peso_vizinho, valor_vizinho = avalia_solucao(vizinho, itens)

        movimento = [i for i in range(len(vizinho)) if vizinho[i] != s_best[i]]

        if movimento in lista_tabu:
            if valor_vizinho > valor_s_best:
                if valor_vizinho > valor_melhor_vizinho:
                    melhor_vizinho = vizinho
                    valor_melhor_vizinho = valor_vizinho
                    movimento_escolhido = movimento
        else:
            if valor_vizinho > valor_melhor_vizinho:
                melhor_vizinho = vizinho
                valor_melhor_vizinho = valor_vizinho
                movimento_escolhido = movimento

    if melhor_vizinho is None and lista_tabu:
        movimento_escolhido = lista_tabu[0]
        for vizinho in vizinhos:
            movimento = [i for i in range(len(vizinho)) if vizinho[i] != s_best[i]]
            if movimento == movimento_escolhido:
                melhor_vizinho = vizinho
                peso_vizinho, valor_melhor_vizinho = avalia_solucao(vizinho, itens)
                break

    return melhor_vizinho, valor_melhor_vizinho

def atualizar_lista_tabu(lista_tabu, movimento, tamanho_maximo):
    lista_tabu.append(movimento)

    if len(lista_tabu) > tamanho_maximo:
        lista_tabu.pop(0)  

    return lista_tabu

def busca_tabu(itens, capacidade, max_iter, max_sem_melhora, tamanho_tabu):
    solucao_atual = gerar_solucao_gulosa(itens, capacidade)
    peso_atual, valor_atual = avalia_solucao(solucao_atual, itens)
    melhor_solucao = solucao_atual[:]
    melhor_valor = valor_atual

    lista_tabu = []
    iteracoes = 0
    iteracoes_sem_melhora = 0

    while iteracoes < max_iter and iteracoes_sem_melhora < max_sem_melhora:
        iteracoes += 1

        vizinhos = gerar_vizinhos(solucao_atual, itens, capacidade)

        melhor_vizinho, valor_vizinho = selecionar_melhor_vizinho(vizinhos, itens, lista_tabu, melhor_solucao, melhor_valor)

        movimento_realizado = [i for i in range(len(solucao_atual)) if solucao_atual[i] != melhor_vizinho[i]]

        lista_tabu = atualizar_lista_tabu(lista_tabu, movimento_realizado, tamanho_tabu)

        solucao_atual = melhor_vizinho[:]
        peso_atual, valor_atual = avalia_solucao(solucao_atual, itens)

        if valor_atual > melhor_valor:
            melhor_solucao = solucao_atual[:]
            melhor_valor = valor_atual
            iteracoes_sem_melhora = 0  
        else:
            iteracoes_sem_melhora += 1

    return melhor_solucao, melhor_valor

def main():
    nome_arquivo = "mochila_4_20"

    capacidade, itens = ler_arquivo_mochila(nome_arquivo)

    itens_convertidos = [(item['valor'], item['peso']) for item in itens]

    max_iter = 100  
    max_sem_melhora = 20  
    tamanho_tabu = 5  

    melhor_solucao, melhor_valor = busca_tabu(itens_convertidos, capacidade, max_iter, max_sem_melhora, tamanho_tabu)

    print("Resultado da Busca Tabu:")
    print(f"Melhor solução: {melhor_solucao}")
    print(f"Valor total da melhor solução: {melhor_valor}")
    print(f"Peso total da melhor solução: {sum(itens_convertidos[i][1] for i in range(len(itens_convertidos)) if melhor_solucao[i] == 1)}")

def ler_arquivo_mochila(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        primeira_linha = arquivo.readline().strip().split()
        capacidade = int(primeira_linha[1])

        itens = []
        for linha in arquivo:
            valor, peso = map(int, linha.strip().split())
            itens.append({'valor': valor, 'peso': peso})

    return capacidade, itens

main()