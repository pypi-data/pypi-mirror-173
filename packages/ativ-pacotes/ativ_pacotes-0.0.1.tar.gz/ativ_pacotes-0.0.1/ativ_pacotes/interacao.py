from ativ_pacotes import armazenamento as ar


def interacao():
    nome = str(input('Digite o nome: \n'))
    cpf = str(input('Digite o CPF: \n'))
    endereco = str(input('Digite o endereco: \n'))

    ar.armazenamento(nome, cpf, endereco)


interacao()
