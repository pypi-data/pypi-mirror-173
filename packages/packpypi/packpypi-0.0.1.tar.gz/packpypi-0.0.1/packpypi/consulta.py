def consulta():
    cpf = input("Digite o cpf que quer vizualizar: ")
    f = open("dados_usuario.txt", "r")
    txt = f.read().splitlines()
    f.close()
    for i in range(len(txt)):
        if cpf in txt[i]:
            print(txt[i-1] + ", " + txt[i+1])
            return txt[i-1], txt[i+1]

consulta()