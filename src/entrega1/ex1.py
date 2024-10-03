class Grafo:

    def __init__(self, vertices):
        self.vertices = int(vertices)
        # Matriz de adjacência
        # Inicialização da matriz com 0 em todos os elementos
        self.grafo = [[0]*self.vertices for i in range(self.vertices)]

    def add_aresta(self, u, v, peso):
        self.grafo[int(u)-1][int(v)-1] = int(peso)

    def visualizar_matriz(self):
        for i in range(self.vertices):
            print(self.grafo[i])

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