from datetime import datetime


class Endereco:
    def __init__(self, cep: str, rua: str, bairro: str, cidade: str, estado: str):
        self.cep = cep
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado


class Usuario:
    def __init__(self, nome: str, cpf: str, data_nascimento: datetime, endereco: Endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco