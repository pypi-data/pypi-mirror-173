def pesquisa():

    cpf = input("Insira o CPF que deseja buscar: ")

    arq = open('dados_usuario.txt', 'r')
    for line in arq:
        if cpf in line:
            print(line)
