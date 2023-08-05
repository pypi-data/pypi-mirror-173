def interacao():
    nome = input("Informe o seu nome? ")
    cpf = input("Digite o seu CPF? ")
    endereço = input("informe o seu Endereço? ")
    print(f"Nome: {nome}, CPF: {cpf}, Endereco: {endereço}")


    return nome, cpf, endereço

interacao()