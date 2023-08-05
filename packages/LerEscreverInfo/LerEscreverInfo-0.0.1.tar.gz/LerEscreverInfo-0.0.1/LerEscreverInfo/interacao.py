import armazenamento


def interacao():
    cpf = input("Por favor, insira o seu cpf: ")
    nome = input("Por favor, insira o seu nome: ")
    endereco = input("Por favor, insira o seu endereço: ")

    armazenamento.armazenar(cpf, nome, endereco)