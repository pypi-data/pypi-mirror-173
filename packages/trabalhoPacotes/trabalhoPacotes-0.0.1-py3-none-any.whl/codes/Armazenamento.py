def armazenar(user: str) -> None:
    with open('dados_usuario.txt', 'a') as arq:
        arq.write(user)
