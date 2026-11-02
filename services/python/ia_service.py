"""IA real: recomendador supervisionado e RAG com LLM local; consumidor do laboratorio."""
from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,Field
from pathlib import Path
from contextlib import asynccontextmanager
import sqlite3,os,json
from recomendador import recomendar,carregar_modelo
from rag_engine import get_engine

@asynccontextmanager
async def lifespan(app):
    carregar_modelo()
    get_engine().carregar_llm()
    yield

app=FastAPI(title="B1 IA real e consumidor do laboratorio",lifespan=lifespan)

@app.get('/health')
def health():
    _,meta=carregar_modelo();engine=get_engine()
    return {'status':'UP','modo':'ml-treinado-e-rag-llm','recomendador':meta['versao'],
            'llm_carregado':engine.model is not None,'llm_modelo':engine.manifest['model_id'] if engine.manifest else None}

class CursoEntrada(BaseModel):
    id:int
    titulo:str=Field(min_length=1,max_length=300)
    descricao:str=Field(default='',max_length=4000)
    nivel:int=Field(default=1,ge=1,le=3)
    tags:list[str]=Field(default_factory=list,max_length=30)

class PerfilRecomendacao(BaseModel):
    interesses:list[str]=Field(default_factory=lambda:['java','arquitetura'],min_length=1,max_length=20)
    nivel:int=Field(default=1,ge=1,le=3)
    cursos:list[CursoEntrada]=Field(max_length=1000)

@app.post('/recomendacoes')
def recomendar_catalogo(perfil:PerfilRecomendacao):
    return recomendar(perfil.interesses,perfil.nivel,[c.model_dump() for c in perfil.cursos])

@app.get('/recomendacoes')
def recomendar_demo(interesses:str=Query(default='java,arquitetura',max_length=500),nivel:int=Query(default=1,ge=1,le=3)):
    catalogo=json.loads((Path(__file__).parent/'dados/catalogo_laboratorio.json').read_text())
    dados=recomendar(interesses.split(','),nivel,catalogo);dados['catalogo']='ficticio-de-laboratorio'
    return dados

class Pergunta(BaseModel):
    pergunta:str=Field(min_length=1,max_length=2000)

@app.post('/assistente')
def assistente(pergunta:Pergunta):
    try:return get_engine().responder(pergunta.pergunta)
    except Exception as erro:
        # Falha real e propagada ao gateway, que aplica fallback; nao se apresenta texto fixo como LLM.
        raise HTTPException(503,'Geracao local indisponivel') from erro

def connect():
    path=Path(os.getenv('B1_PYTHON_DB','state/python.db'));path.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS notificacoes (event_id TEXT PRIMARY KEY,payload TEXT NOT NULL)')
    return db

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
