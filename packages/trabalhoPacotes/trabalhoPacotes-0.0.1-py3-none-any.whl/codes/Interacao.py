def interacao() -> tuple:
    cpf, nome, endereco = input('Digite seu cpf, nome de usuário e endereço: ').split()
    
    return f'{cpf} {nome} {endereco}\n'
