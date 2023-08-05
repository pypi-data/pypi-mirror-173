def interacao():
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? ")
    cep = input("Qual seu CEP? ")
    print(f"Nome: {nome}, CPF: {cpf}, CEP: {cep}")
    return nome, cpf, cep

interacao()