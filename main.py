from typing import Union
from typing import Annotated

from fastapi import FastAPI, Request, HTTPException,Depends
from fastapi.templating import Jinja2Templates
from models import *
from argon2 import PasswordHasher 
from argon2.exceptions import VerifyMismatchError

templates = Jinja2Templates("templates")

app = FastAPI()
sqlite_nome_arquivo = "confeitaria.db"
sqlite_url = f"sqlite:///{sqlite_nome_arquivo}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

ph = PasswordHasher()

@app.post("/register")
def register(usuario: str, email: str, senha: str, senha_confirmar: str):
    if not usuario.strip() or not email.strip() or not senha.strip() or not senha_confirmar.strip():
        raise HTTPException(status_code= 400, detail= "Bad request: Missing fields")
    if senha != senha_confirmar:
        raise HTTPException(status_code=400, detail="Bad request: passwords not match")
    
    with Session(engine) as session:

        senha_encriptada = ph.hash(senha)

        usr = Usuario(usuario=usuario, email=email, hash=senha_encriptada)

        session.add(usr)
        session.commit()
        session.refresh(usr)
        return usr

@app.post("/login")
def login(usuario:str, senha:str ):
    
    with Session(engine) as session:
        st = select(Usuario).where(Usuario.usuario == usuario)
        lista_bd = session.exec(st)
        for i in lista_bd:
            if not i.usuario:
                raise HTTPException (status_code=404, detail="Not found")
            try:
                ph.verify(i.hash, senha)
            except VerifyMismatchError:
                raise HTTPException(status_code=400, detail="Bad request, password not match")
            return "sucesso"
        

@app.get("/clientes")
def obter_clientes():
    with Session(engine) as session:
        lista = session.exec(select(Cliente)).all()
        return lista
    

@app.post("/clientes/criar")
def criar_clientes(cliente: ClienteBase):
    if not cliente.nome.strip() or not cliente.telefone.strip():
        raise HTTPException(status_code=400, detail="Bad request: 'nome' and 'telefone' fields cannot be empty")
    with Session(engine) as session:    
        db_cliente = Cliente.model_validate(cliente)
        session.add(db_cliente)
        session.commit()
        session.refresh(db_cliente)
        return db_cliente

@app.get("/clientes/{cliente_id}")
def obter_cliente(cliente_id: int):
    with Session(engine) as session:
        pessoa = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
        return pessoa

@app.put("/clientes/{cliente_id}")
def atualizar_dados_do_cliente(cliente_id: int ,cliente: ClienteBase):
    with Session(engine) as session:
        pessoa = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
        if not pessoa:
            raise HTTPException (status_code=404, detail="Not found")
        pessoa.nome = cliente.nome
        pessoa.telefone = cliente.telefone

        session.add(pessoa)
        session.commit()
        session.refresh(pessoa)
        return pessoa
@app.post("/encomendas")
def criar_encomenda(encomenda: EncomendaBase, cliente: ClienteBase):
    with Session(engine) as session:
        id_cliente = session.exec(select(Cliente.id).where(Cliente.nome == cliente.nome, Cliente.telefone == cliente.telefone)).first()
        if not id_cliente:
            novo_cliente = criar_clientes(cliente)
            encomenda.id_cliente = novo_cliente.id
        else:
            encomenda.id_cliente = id_cliente

        db_encomenda = Encomenda.model_validate(encomenda)
        session.add(db_encomenda)
        session.commit()
        session.refresh(db_encomenda)
        return db_encomenda

        
@app.get("/encomendas")
def obter_encomendas():
    with Session(engine) as session:
        encomendas = session.exec(select(Encomenda)).all()
        return encomendas
    
@app.get("/encomendas/{encomenda_id}")
def obter_encomenda(encomenda_id: int):
    with Session(engine) as session:
        encomenda = session.exec(select(Encomenda).where(Encomenda.id == encomenda_id)).first()
        if not encomenda:
            raise HTTPException(status_code=404, detail= "Not found")
        return encomenda
@app.delete("/encomendas/delete/{encomenda_id}")
def excluir_encomenda(encomenda_id: int):
    with Session(engine) as session:
        encomenda = session.exec(select(Encomenda).where(Encomenda.id == encomenda_id)).first()
        encomenda_copia = encomenda
        if not encomenda:
            raise HTTPException(status_code=404, detail= "Not found")
        session.delete(encomenda)
        session.commit()
        return {"dado excluido com sucesso": encomenda}
    
@app.put("/encomendas/{encomenda_id}")
def atualizar_encomenda(encomenda: EncomendaBase, encomenda_id:int):
    with Session(engine) as session:
        encomenda_existente = session.exec(select(Encomenda).where(Encomenda.id == encomenda_id)).first()
        if not encomenda_existente:
            raise HTTPException(status_code=404, detail="Not found")
        
        encomenda_existente.id_cliente = encomenda.id_cliente
        encomenda_existente.produto = encomenda.produto
        encomenda_existente.data_entrega = encomenda.data_entrega
        encomenda_existente.data_encomenda = encomenda.data_encomenda
        encomenda_existente.status = encomenda.status
        encomenda_existente.preco = encomenda.preco

        session.add(encomenda_existente)
        session.commit()
        session.refresh(encomenda_existente)
        
        return encomenda_existente