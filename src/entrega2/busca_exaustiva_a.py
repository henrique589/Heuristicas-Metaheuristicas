import time

def permutacao(nums: list[int]):
    n = len(nums)
    solucao = []

    def backtrack():
        if len(solucao) == n:
            print(solucao)
            return
        
        for x in nums:
            if x not in solucao:
                solucao.append(x)
                backtrack()
                solucao.pop()

    start_time = time.time()
    backtrack()
    end_time = time.time()
    print(f'Tempo de processamento = {end_time - start_time:.4f} segundos')

n = int(input('Digite um número n: '))
nums = list(range(1, n + 1))
permutacao(nums)