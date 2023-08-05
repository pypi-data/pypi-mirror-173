import consulta
import interacao

if __name__ == "__main__":
    resp = ''
    print("--------------------------------------")
    print("Escolha a operação que deseja fazer:")
    print("(1) Inserir dados")
    print("(2) Buscar dados")
    print("(3) Sair")
    print("--------------------------------------")
    while resp != '3':
        resp = input("Escolha: ")
        if resp == '1':
            interacao.interacao()
        elif resp == '2':
            consulta.pesquisa()

