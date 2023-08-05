def consulta():
    cpf = input("Insira o CPF que deseja consultar: ")
    f = open("dados_usuario.txt", "r")
    txt = f.read().splitlines()
    f.close()
    for i in range(len(txt)):
        if cpf in txt[i]:
            print(txt[i-1] + ", " + txt[i+1])
            return txt[i-1], txt[i+1]
    print("Nenhum usuario encontrado")
    return
consulta()
