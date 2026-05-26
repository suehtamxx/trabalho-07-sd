from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, joinedload
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./teste_carga.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos do banco de dados
class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    pedidos = relationship("Pedido", back_populates="cliente")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente", back_populates="pedidos")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    Base.metadata.create_all(bind=engine)
    try:
        if db.query(Cliente).count() == 0:
            print("Populando o banco de dados com dados de teste...")
            for i in range(1, 51):
                cliente = Cliente(nome=f"Cliente {i}")
                db.add(cliente)
                db.commit()
                db.refresh(cliente)

                for j in range(1, 6):
                    pedido = Pedido(descricao=f"Pedido {j} do Cliente {i}", cliente_id=cliente.id)
                    db.add(pedido)
            db.commit()
        yield
    finally:
        db.close()

app = FastAPI(title="API Monolítica - Otimizada (Rápida)", lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ClienteCreate(BaseModel):
    nome: str

@app.get("/api/recurso-lento")
def recurso_lento(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).options(joinedload(Cliente.pedidos)).all()
    resultado = []

    for cliente in clientes:
        resultado.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "total_pedidos": len(cliente.pedidos) 
        })
    return resultado

@app.get("/api/recurso-detalhe/{id}")
def recurso_detalhe(id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"id": cliente.id, "nome": cliente.nome}

@app.get("/api/status")
def status():
    return {"status": "ok", "message": "API está rodando"}

@app.post("/api/recurso")
def criar_recurso(cliente: ClienteCreate, db: Session = Depends(get_db)):
    novo_cliente = Cliente(nome=cliente.nome)
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return {"id": novo_cliente.id, "nome": novo_cliente.nome}