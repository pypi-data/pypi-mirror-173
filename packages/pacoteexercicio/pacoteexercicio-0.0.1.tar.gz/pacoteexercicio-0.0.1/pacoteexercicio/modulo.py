def registrar_dados():
    cpf = input('digite seu cpf: ')
    nome = input('digite seu nome: ')
    endereco = input('digite seu endereço: ')

    with open('bancoDeDados.txt', 'w') as arquivo:
        arquivo.write(f'cpf: {cpf}, nome: {nome}, endereço: {endereco}') 
        arquivo.close()


def ler_dados():
    with open('bancoDeDados.txt', 'r') as arquivo:
        dados = arquivo.read()
        print(dados)
        arquivo.close()
        
