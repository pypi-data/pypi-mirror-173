
def interacao():
    nome = input("Qual seu nome? ")
    cpf = input("Qual seu CPF? ")
    end = input("Qual seu endereco? ")
    print(f"Nome: {nome}, CPF: {cpf}, Endereco: {end}")
    return nome, cpf, end

interacao()
