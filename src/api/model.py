from datetime import datetime


class Usuario:
    def __init__(self, nome: str, data_nascimento: datetime):
        self.nome = nome
        self.data_nascimento = data_nascimento
