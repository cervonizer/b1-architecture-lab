"""Contrato de IA e consumidor de notificacoes para os mini labs. Sem LLM externo."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import sqlite3
import os

app = FastAPI(title="B1 IA e consumidor do laboratorio")
MATERIAIS = {
    "ranking": "O Ranking soma 100 pontos por curso concluido e as moedas da assinatura.",
    "creditos": "Uma conclusao com aproveitamento concede tres creditos de cursos.",
    "arquitetura": "O Core e um monolito modular Java; IA possui uma fronteira HTTP em Python.",
}

def connect():
    path = Path(os.getenv("B1_PYTHON_DB", "state/python.db"))
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS notificacoes (event_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
    return db

@app.get("/health")
def health(): return {"status": "UP", "modo": "simulacao-do-contrato"}

@app.get("/recomendacoes")
def recomendar():
    return {"fonte": "python-simulacao", "degradado": False,
            "cursos": ["Arquitetura de Software B1", "Testes e qualidade"],
            "nota": "Catalogo fixo para testar fronteira e falha; nao e modelo ML treinado."}

class Pergunta(BaseModel):
    pergunta: str = Field(min_length=1, max_length=2000)

@app.post("/assistente")
def assistente(pergunta: Pergunta):
    encontrados = [(chave, texto) for chave, texto in MATERIAIS.items() if chave in pergunta.pergunta.lower()]
    return {"fonte": "recuperacao-lexical-local", "degradado": False, "modo": "sem-LLM",
            "resposta": " ".join(texto for _, texto in encontrados) or "Consulte os materiais cadastrados no Core.",
            "fontes": [chave for chave, _ in encontrados]}

class Notificacao(BaseModel):
    event_id: str = Field(min_length=1, max_length=100)
    tipo: str
    matricula_id: int | None = None
    usuario_id: int | None = None

@app.post("/notificacoes")
def notificar(evento: Notificacao):
    falha = Path(os.getenv("B1_FAILURE_FILE", "state/notificacoes.off"))
    if falha.exists(): raise HTTPException(503, "Falha controlada do consumidor")
    payload = evento.model_dump_json()
    with connect() as db:
        anterior = db.execute("SELECT payload FROM notificacoes WHERE event_id=?", (evento.event_id,)).fetchone()
        if anterior and anterior[0] != payload: raise HTTPException(409, "event_id com conteudo diferente")
        db.execute("INSERT OR IGNORE INTO notificacoes VALUES (?,?)", (evento.event_id, payload))
    return {"aceito": True, "duplicado": anterior is not None}

@app.get("/lab/notificacoes")
def notificacoes():
    with connect() as db: return {"recebidas": db.execute("SELECT COUNT(*) FROM notificacoes").fetchone()[0]}

class Falha(BaseModel): ativo: bool

@app.post("/lab/notificacoes/falha")
def simular_falha(falha: Falha):
    path = Path(os.getenv("B1_FAILURE_FILE", "state/notificacoes.off"))
    path.parent.mkdir(parents=True, exist_ok=True)
    if falha.ativo: path.touch()
    else: path.unlink(missing_ok=True)
    return {"falha": falha.ativo}
