def string_binaria(n, string=""):
    if(len(string) == n):
        print(string)
        return
    
    string_binaria(n, string + "0")
    string_binaria(n, string + "1")

n = input('Digite um valor para n: ')
string_binaria(int(n))