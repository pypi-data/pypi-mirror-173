def consulta():
    busca = str(input('Qual o cpf para busca? \n'))

    f = open(r'/atividade/dados_usuario.txt', 'r')
    dados = f.readlines()
    substr = ""
    count = 0
    for i in dados:
        if busca in i:
            for j in i:
                if j == ",":
                    count += 1

                if count != 1:
                    substr += j

            break

    print(substr)


consulta()
