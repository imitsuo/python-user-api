from datetime import datetime

from fastapi.testclient import TestClient
import unittest
from src.api.main import app


class UsuariosTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def tearDown(self):
        pass

    def test_get__obter_Usuario_por_id__expected_usuario(self):
        response = self.client.get("/usuarios")
        assert response.status_code == 200
        assert response.json() == {
            "nome": "teste",
            "data_nascimento": datetime(2020, 1, 12).isoformat()
        }
