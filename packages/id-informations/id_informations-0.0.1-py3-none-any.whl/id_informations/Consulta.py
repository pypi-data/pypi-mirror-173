def consultar():
    arq = open("../dados_usuario.txt", 'r')
    dados = arq.readline()
    print(dados)

consultar()
