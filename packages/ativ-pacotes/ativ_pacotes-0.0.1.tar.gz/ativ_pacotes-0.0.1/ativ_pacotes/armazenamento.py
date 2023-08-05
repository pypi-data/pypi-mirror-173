def armazenamento(nome, cpf, endereco):
    arq = open('../../cesupa/ativ_pacotes/dados_usuario.txt', 'a')
    arq.write(f'Nome : {nome}, CPF: {cpf}, endereco: {endereco}.\n')
    arq.close()

