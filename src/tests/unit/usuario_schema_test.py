import datetime
import unittest
from src.api.validator import UsuarioValidator


class UsuarioSchemaTest(unittest.TestCase):

    def test_validate__usuario_valido__expected_nenhum_erro(self):
        usuario = UsuarioValidator().load(
            {
                'nome': 'teste',
                'cpf': '87535514600',
                'data_nascimento': datetime.datetime(2020, 1, 1).isoformat(),
                'endereco': {
                    'cep': '00121-010',
                    'rua': 'rua x',
                    'bairro': 'bairro novo',
                    'cidade': 'cidade w',
                    'estado': 'SP'
                }
            }
        )

        self.assertEqual('teste', usuario.nome)
        self.assertEqual('87535514600', usuario.cpf)
        self.assertEqual(datetime.datetime(2020, 1, 1), usuario.data_nascimento)
        self.assertEqual('00121-010', usuario.endereco.cep)
        self.assertEqual('rua x', usuario.endereco.rua)
        self.assertEqual('bairro novo', usuario.endereco.bairro)
        self.assertEqual('cidade w', usuario.endereco.cidade)
        self.assertEqual('SP', usuario.endereco.estado)

    def test_validate__usuario_cpf_invalido__expected_erro(self):
        errors = UsuarioValidator().validate(
            {
                'nome': 'teste',
                'cpf': '8753551460',
                'data_nascimento': datetime.datetime(2020, 1, 1).isoformat(),
                'endereco': {
                    'cep': '00121-010',
                    'rua': 'rua x',
                    'bairro': 'bairro novo',
                    'cidade': 'cidade w',
                    'estado': 'SP'
                }
            }
        )

        self.assertEqual(1, len(errors))
        self.assertEqual(['Cpf inválido.'], errors['cpf'])
