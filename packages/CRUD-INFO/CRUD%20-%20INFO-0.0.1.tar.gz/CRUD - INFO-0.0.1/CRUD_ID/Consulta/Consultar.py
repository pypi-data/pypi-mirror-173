def consultar(path):
    cpf = input("Insert cpf to search")
    i = 0
    with open(path, "r") as arq:
        lines = arq.readlines()
        for line in lines:
            i += 1
            if cpf in line:
                for j in range(i, i + 2):
                    print(lines[j])
