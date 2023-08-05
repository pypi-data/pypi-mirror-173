import Interacao


def armazenar():
    arq = open("../dados_usuario.txt", 'w')
    dados = Interacao.interagir()
    arq.write(dados)
    arq.close()


armazenar()