def armazenamento(nome, cpf, end):
    f = open("dados_usuario.txt", "a")
    f.write(f"{nome}\n{cpf}\n{end}\n")
    f.close()

armazenamento()