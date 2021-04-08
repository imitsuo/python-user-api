import json
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends, Response
from marshmallow import ValidationError
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from starlette import status

from src.api.database import SessionLocal
from src.api.model import UsuarioSchema, UsuarioModel
from src.api.validator import UsuarioSchema, UsuarioValidator

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/usuarios", status_code=status.HTTP_200_OK)
def listar_usuarios(offset: int = 0, db: Session = Depends(get_db)):
    _limit = 10
    _total = db.query(UsuarioModel).count()
    _query = db.query(UsuarioModel).options(joinedload('endereco')).order_by(UsuarioModel.id)
    _query = _query.limit(_limit).offset(offset)
    _result = _query.all()

    return {'limit': 10, 'offset': offset, 'total': _total, 'usuarios': _result}


@app.get("/usuarios/{usuario_id}", status_code=status.HTTP_200_OK)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    _usuario = db.query(UsuarioModel).options(joinedload('endereco')).filter(UsuarioModel.id == usuario_id).first()
    if _usuario is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return _usuario


@app.post("/usuarios/", status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    try:
        _usuario = UsuarioValidator().loads(usuario.json())
        _endereco = _usuario.endereco
    except ValidationError as err:
        return Response(json.dumps(err.normalized_messages()), status_code=status.HTTP_400_BAD_REQUEST, media_type='application/json')

    _u = db.query(UsuarioModel).filter(UsuarioModel.cpf == usuario.cpf).first()
    if _u is not None:
        return Response(content=json.dumps({'message': 'Usuario já cadastrado'}), status_code=status.HTTP_409_CONFLICT, media_type='application/json')

    db.add(_usuario)
    db.flush()
    _endereco.usuario_id = _usuario.id
    db.add(_endereco)
    db.commit()

    _usuario = db.query(UsuarioModel).options(joinedload('endereco')).filter(UsuarioModel.id == _usuario.id).first()

    return _usuario


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
