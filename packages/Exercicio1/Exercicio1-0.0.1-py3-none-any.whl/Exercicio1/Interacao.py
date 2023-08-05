def interacao():
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? ")
    endereco = input("Qual seu endereco? ")
    print(f"Nome: {nome}, CPF: {cpf}, Endereco: {endereco}")
    return nome, cpf, endereco

interacao()