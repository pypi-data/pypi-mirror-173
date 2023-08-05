def armazenamento(nome, cpf, endereço):
    f = open("dados_usuario.txt", "a")
    f.write(f"{nome}\n{cpf}\n{endereço}\n\n")
    f.close()

armazenamento()