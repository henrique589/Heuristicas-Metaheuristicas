class Grafo:

    def __init__(self, vertices):
        self.vertices = int(vertices)
        # Matriz de adjacência
        self.matriz_adjacencia = [[0]*self.vertices for i in range(self.vertices)]
        # Lista de adjacência
        self.lista_adjacencia = [[] for i in range(self.vertices)]

    def add_aresta(self, u, v, peso):
        # Add arestas para matriz de ajacência
        self.matriz_adjacencia[int(u)-1][int(v)-1] = int(peso)
        self.matriz_adjacencia[int(v)-1][int(u)-1] = int(peso)

        # Add arestas para lista de adjacência
        self.lista_adjacencia[int(u)-1].append([int(v), int(peso)])
        self.lista_adjacencia[int(v)-1].append([int(u), int(peso)])

    def visualizar_matriz(self):
        # Exibir matriz de adjacência
        for i in range(self.vertices):
            print(self.matriz_adjacencia[i])

    def visualizar_lista(self):
        #Exibir lista de adjacência
        for i in range(self.vertices):
            print(f'{i+1}: ', end='  ')
            for j in self.lista_adjacencia[i]:
                print(f'{j} ->', end='  ')
            print()

#Open the file for reading
with open('in.txt', 'r') as f:
    for idx, line in enumerate(f):
        # The strip method removes spaces from a string
        # The split method divides a string into parts
        nodes = line.strip().split()
        if idx == 0: 
            g = Grafo(nodes[0])
        else:
            g.add_aresta(nodes[0], nodes[1], nodes[2])

g.visualizar_matriz()
g.visualizar_lista()