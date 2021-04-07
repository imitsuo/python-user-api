from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from src.api.model import Usuario

app = FastAPI()


@app.get("/usuarios")
def get_usuario():
    return Usuario('teste', datetime(2020, 1, 12))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
