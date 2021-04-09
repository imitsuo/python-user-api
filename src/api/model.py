from datetime import datetime

from pydantic.main import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


class EnderecoSchema(BaseModel):
    cep: str
    rua: str
    bairro: str
    cidade: str
    estado: str


class UsuarioSchema(BaseModel):
    nome: str
    cpf: str
    data_nascimento: datetime
    endereco: EnderecoSchema


class UsuarioModel(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), unique=True, index=True)
    nome = Column(String(100), nullable=True)
    data_nascimento = Column(DateTime, nullable=True)
    endereco = relationship("EnderecoModel", uselist=False)


class EnderecoModel(Base):
    __tablename__ = "endereco"
    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(9), nullable=True)
    rua = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    estado = Column(String(2), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

