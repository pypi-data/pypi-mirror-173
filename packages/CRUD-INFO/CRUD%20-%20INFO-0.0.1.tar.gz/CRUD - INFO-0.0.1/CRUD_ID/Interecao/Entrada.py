import CRUD_ID.Armazenamento.Armazenar


def insert(path):
    name = input("Insert your name")
    cpf = input("Insert your cpf")
    address = input("Insert your address")
    return CRUD_ID.Armazenamento.Armazenar.store(name, cpf, address, path)
