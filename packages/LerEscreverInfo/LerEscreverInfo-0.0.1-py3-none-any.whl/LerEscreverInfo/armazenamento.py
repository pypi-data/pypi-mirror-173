import os

def armazenar(cpf, nome, endereco):
    texto = []
    arquivo = 'dados_usuario.txt'

    if os.path.exists(arquivo):
        arq = open("dados_usuario.txt", 'r')
        texto.append(arq.read())
        arq.close()

    arq = open("dados_usuario.txt", 'w')
    texto.append(f'{cpf}: "{nome}", "{endereco}"' + "\n")
    arq.writelines(texto)
    arq.close()