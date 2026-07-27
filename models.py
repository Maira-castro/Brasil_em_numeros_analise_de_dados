from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///banco.db", connect_args={"check_same_thread": False})

Base = declarative_base()

class Brasil(Base):
    __tablename__ = "brasil_db"

    id = Column(Integer, primary_key=True, index=True)
    uf_id = Column(Integer)
    estado = Column(String)
    ano = Column(Integer)
    populacao = Column(Integer)
    sigla = Column(String)
    regiao = Column(String) 

    def __init__(self, uf_id, estado, ano, populacao, sigla, regiao):
        self.uf_id = uf_id
        self.estado = estado
        self.ano = ano
        self.populacao = populacao
        self.sigla = sigla
        self.regiao = regiao