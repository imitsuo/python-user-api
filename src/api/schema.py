import datetime

from marshmallow import ValidationError, fields, Schema, validate, validates, post_load

from src.api.model import Usuario, Endereco


def _validate_cpf(value):
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


class MyDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.datetime):
            return value
        return super()._deserialize(value, attr, data)




class EnderecoSchema(Schema):
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

    @post_load
    def make_endereco(self, data: dict, **kwargs):
        return Endereco(**data)


class UsuarioSchema(Schema):
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
    endereco = fields.Nested(EnderecoSchema(), required=True)

    @validates("cpf")
    def validate_cpf(self, value):
        _validate_cpf(value)

    @post_load
    def make_usuario(self, data: dict, **kwargs):
        return Usuario(**data)
