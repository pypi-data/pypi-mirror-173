def store(name, cpf, address, path):
    with open(path, "a+") as arq:
        arq.write(f"CPF: {cpf}\n Name: {name}\n Address: {address}\n")
    print("Armazenamento feito com sucesso")
