def armazenamento(nome, cpf, endereco):
    f = open("dados_usuario.txt", "a")
    f.write(f"{nome}\n{cpf}\n{endereco}\n\n")
    f.close()

armazenamento()