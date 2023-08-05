def armazenamento(nome, cpf, cep):
    f = open("dados_usuario.txt", "a")
    f.write(f"Nome: {nome}\nCPF: {cpf}\nCEP: {cep}\n\n")
    f.close()

armazenamento()