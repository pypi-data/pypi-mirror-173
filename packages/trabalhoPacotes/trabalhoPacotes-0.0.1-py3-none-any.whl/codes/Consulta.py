def consulta(cpf: str) -> str:
    with open('dados_usuario.txt', 'r') as arq:
        for users in arq.readlines():
            if cpf in users:
                _, nome, endereco = users.split()
                return f'NOME: {nome} ENDEREÇO: {endereco}'
        
        return 'Não existe cadastro com este CPF'
