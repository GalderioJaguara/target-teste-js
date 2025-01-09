from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime

class UsuarioBase(SQLModel):
    id: int = Field(default=None, index=True, primary_key=True)
    usuario: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(unique=True, nullable=False)

class Usuario (UsuarioBase ,table=True):

    hash: str = Field(nullable=False)

class CreateUser(UsuarioBase):
    senha: str


class ClienteBase(SQLModel):
    nome: str = Field(index=True,nullable=False)
    telefone: str 


class Cliente(ClienteBase, table=True):
    id: int = Field(default=None, index=True, primary_key=True)

class EncomendaBase(SQLModel):
    id_cliente: int = Field(default=None, foreign_key="cliente.id")
    produto: str
    preco: float
    data_encomenda: datetime
    data_entrega: datetime
    status: str

class Encomenda(EncomendaBase, table=True):
    id: int = Field(default=None, index=True, primary_key=True)

