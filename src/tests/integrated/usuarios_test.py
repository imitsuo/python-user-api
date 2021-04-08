from datetime import datetime

from fastapi.testclient import TestClient
import unittest

from src.api.database import Base
from src.api.main import app


from sqlalchemy import create_engine, MetaData, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.api.model import UsuarioModel, EnderecoModel

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"


class UsuariosTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        cls.sessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=cls.engine)

    def setUp(self):
        self.db = self.sessionLocal()
        self.client = TestClient(app)
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def tearDown(self):
        pass
        # Base.metadata.drop_all(bind=self.engine)
        # Base.metadata.drop_all(bind=self.engine)

    def criar_usuario_para_testes(self):
        _cpf = '87535514600'
        _usuario = self.db.query(UsuarioModel).filter(UsuarioModel.cpf == _cpf).first()
        if _usuario is not None:
            q = delete(EnderecoModel).where(EnderecoModel.usuario_id == _usuario.id)
            self.db.execute(q)

            q = delete(UsuarioModel).where(UsuarioModel.id == _usuario.id)
            self.db.execute(q)

        _usuario = UsuarioModel()
        _usuario.cpf = _cpf
        _usuario.data_nascimento = datetime(2021, 1, 13)
        _usuario.nome = 'teste'
        self.db.add(_usuario)
        self.db.flush()

        _endereco = EnderecoModel()
        _endereco.cep = '01111-333'
        _endereco.rua = 'aaa'
        _endereco.bairro = '5555'
        _endereco.cidade = 'dsadas'
        _endereco.estado = 'SP'
        _endereco.usuario_id = _usuario.id
        self.db.add(_endereco)
        self.db.flush()
        # self.db.commit()

        return _usuario, _endereco

    def test_obter_Usuario_por_id__usuario_cadastrado__expected_usuario(self):
        # FIXTURES
        _usuario, _endereco = self.criar_usuario_para_testes()

        # EXERCISE
        response = self.client.get(f'/usuarios/{_usuario.id}')

        # ASSERTS
        assert response.status_code == 200
        assert response.json() == {
                                    'id': _usuario.id,
                                    'cpf': _usuario.cpf,
                                    'data_nascimento': _usuario.data_nascimento.isoformat(),
                                    'nome': _usuario.nome,
                                    'endereco': {
                                                  'bairro': _endereco.bairro,
                                                  'cep': _endereco.cep,
                                                  'estado': _endereco.estado,
                                                  'cidade': _endereco.cidade,
                                                  'id': _endereco.id,
                                                  'rua': _endereco.rua,
                                                  'usuario_id': _endereco.usuario_id
                                                }
                                              }

    def test_listar_usuarios__usuario_cadastrado__expected_usuario_paginado(self):
        # FIXTURES
        _usuario, _endereco = self.criar_usuario_para_testes()

        # EXERCISE
        response = self.client.get(f'/usuarios/?offset=0')

        # ASSERTS
        assert response.status_code == 200
        assert response.json() == {
                                    'limit': 10,
                                    'offset': 0,
                                    'total': 1,
                                    'usuarios': [
                                                  {
                                                    'id': _usuario.id,
                                                    'cpf': _usuario.cpf,
                                                    'data_nascimento': _usuario.data_nascimento.isoformat(),
                                                    'nome': _usuario.nome,
                                                    'endereco': {
                                                                  'bairro': _endereco.bairro,
                                                                  'cep': _endereco.cep,
                                                                  'estado': _endereco.estado,
                                                                  'cidade': _endereco.cidade,
                                                                  'id': _endereco.id,
                                                                  'rua': _endereco.rua,
                                                                  'usuario_id': _endereco.usuario_id
                                                    }
                                                  }
                                         ]
                                    }

    def test_criar_usuario__novo_usuario__expected_criar_usuario(self):
        # FIXTURES
        _cpf = '55827901016'
        _usuario = self.db.query(UsuarioModel).filter(UsuarioModel.cpf == _cpf).first()
        if _usuario is not None:
            q = delete(EnderecoModel).where(EnderecoModel.usuario_id == _usuario.id)
            self.db.execute(q)

            q = delete(UsuarioModel).where(UsuarioModel.id == _usuario.id)
            self.db.execute(q)

        _payload = {
            'nome': 'teste 2',
            'cpf': _cpf,
            'data_nascimento': '2021-04-08T00:00:00.000000',
            'endereco': {
                         'cep': '08121-040',
                         'rua': 'bb',
                         'bairro': 'aa',
                         'cidade': 'ss',
                         'estado': 'SP'
                       }
            }

        # EXERCISE
        response = self.client.post('/usuarios/', json=_payload)

        # ASSERTS
        _usuario = self.db.query(UsuarioModel).filter(UsuarioModel.cpf == _cpf).first()

        assert response.status_code == 201
        assert response.json() == {
            'id': _usuario.id,
            'nome': 'teste 2',
            'cpf': _cpf,
            'data_nascimento': '2021-04-08T00:00:00',
            'endereco': {
                         'cep': '08121-040',
                         'rua': 'bb',
                         'bairro': 'aa',
                         'cidade': 'ss',
                         'estado': 'SP',
                         'id': _usuario.endereco.id,
                         'usuario_id': _usuario.id
                       }
            }

    def test_atualizar_usuario__usuario_cadastrado__expected_atualizar_usuario(self):
        # FIXTURES
        _usuario, _endereco = self.criar_usuario_para_testes()

        _payload = {
            'nome': 'teste aaaa',
            'cpf': _usuario.cpf,
            'data_nascimento': '2021-04-01T00:00:00',
            'endereco': {
                'cep': '08122-040',
                'rua': 'bb c',
                'bairro': 'aab',
                'cidade': 'ssa',
                'estado': 'SC'
            }
        }

        # EXERCISE
        response = self.client.put(f'/usuarios/{_usuario.id}', json=_payload)

        # ASSERTS
        assert response.status_code == 200
        self.db.refresh(_usuario)

        self.assertEqual('teste aaaa', _usuario.nome)
        self.assertEqual(datetime(2021, 4, 1), _usuario.data_nascimento)
        self.assertEqual('08122-040', _usuario.endereco.cep)
        self.assertEqual('bb c', _usuario.endereco.rua)
        self.assertEqual('aab', _usuario.endereco.bairro)
        self.assertEqual('ssa', _usuario.endereco.cidade)
        self.assertEqual('SC', _usuario.endereco.estado)

        assert response.json() == {
            'id': _usuario.id,
            'nome': 'teste aaaa',
            'cpf': _usuario.cpf,
            'data_nascimento': '2021-04-01T00:00:00',
            'endereco': {
                'id': _usuario.endereco.id,
                'cep': '08122-040',
                'rua': 'bb c',
                'bairro': 'aab',
                'cidade': 'ssa',
                'estado': 'SC',
                'usuario_id': _usuario.id
            }
        }

