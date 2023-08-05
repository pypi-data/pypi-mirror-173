from Interacao import interacao
from Armazenamento import armazenar
from Consulta import consulta

while True:
    choice = input('Digite 1 para armazenar dados e 2 para consultar: ')

    if choice == '1':
        armazenar(interacao())
    elif choice == '2':
        cpf = input('Digite o cpf a ser consultado: ')
        print(consulta(cpf))
