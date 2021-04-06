from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from src.api.model import Usuario

app = FastAPI()


@app.get("/usuario")
def get_usuario():
    return Usuario('teste', datetime.now())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
