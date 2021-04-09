import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_postgres_host = 'localhost'
if os.getenv('POSTGRES_USER_API'):
    _postgres_host = os.getenv('POSTGRES_USER_API')

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:postgres@{_postgres_host}/postgres'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
