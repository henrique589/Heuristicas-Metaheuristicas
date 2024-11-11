import itertools

def generate_permutations(n):
    # Cria uma lista com os números de 1 a n
    numbers = list(range(1, n + 1))
    # Gera todas as permutações
    perms = itertools.permutations(numbers)
    
    # Itera e imprime cada permutação
    for perm in perms:
        print(perm)

# Exemplo de uso:
n = int(input("Digite o valor de n: "))
generate_permutations(n)
