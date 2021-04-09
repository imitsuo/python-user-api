import datetime
import re

from marshmallow import ValidationError, fields, Schema, validate, validates, post_load
from model import UsuarioModel, EnderecoModel


def _validate_cpf(value):
    if not str.isdigit(value):
        raise ValidationError("Cpf inválido.")

    cpf = [int(char) for char in value if char.isdigit()]

    if len(cpf) != 11:
        raise ValidationError("Cpf inválido.")

    if cpf == cpf[::-1]:
        raise ValidationError("Cpf inválido.")

    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            raise ValidationError("Cpf inválido.")


def _validate_cep(value):
    if re.match('\d{5}-\d{3}', value) is None:
        raise ValidationError("Cep inválido.")


class MyDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.datetime):
            return value
        return super()._deserialize(value, attr, data)


class EnderecoValidator(Schema):
    cep = fields.Str(required=True)
    rua = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error='Rua deve ter no mínimo {min} e no máximo {max} caracteres.'
        )
    )
    bairro = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error='bairro deve ter no mínimo {min} e no máximo {max} caracteres.'
        )
    )
    cidade = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error='Cidade deve ter no mínimo {min} e no máximo {max} caracteres.'
        )
    )
    estado = fields.Str(required=True)

    @validates("cep")
    def validate_cep(self, value):
        _validate_cep(value)

    @post_load
    def make_endereco(self, data: dict, **kwargs):
        return EnderecoModel(**data)


class UsuarioValidator(Schema):
    nome = fields.Str(
        required=True,
        validate=validate.Length(
            min=2,
            max=100,
            error='Nome deve ter no mínimo {min} e no máximo {max} caracteres.'
        )
    )
    cpf = fields.Str(required=True)
    data_nascimento = fields.DateTime(required=True)
    endereco = fields.Nested(EnderecoValidator(), required=True)

    @validates("cpf")
    def validate_cpf(self, value):
        _validate_cpf(value)

    @post_load
    def make_usuario(self, data: dict, **kwargs):
        return UsuarioModel(**data)
