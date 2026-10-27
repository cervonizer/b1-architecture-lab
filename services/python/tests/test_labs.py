from fastapi.testclient import TestClient
from ia_service import app
from iot_gateway import Spool, transformar
import pytest

@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setenv("B1_PYTHON_DB",str(tmp_path/"python.db"))
    monkeypatch.setenv("B1_FAILURE_FILE",str(tmp_path/"failure"))
    return TestClient(app)

def test_recomendacao_identifica_simulacao(client):
    r=client.get("/recomendacoes");assert r.status_code==200;assert r.json()["fonte"]=="python-simulacao"

def test_assistente_recupera_fonte_sem_fingir_llm(client):
    r=client.post("/assistente",json={"pergunta":"Como funciona ranking?"})
    assert r.json()["fontes"]==["ranking"];assert r.json()["modo"]=="sem-LLM"

def test_notificacao_idempotente_e_recuperacao(client):
    evento={"event_id":"curso-1","tipo":"CURSO_CONCLUIDO","matricula_id":1,"usuario_id":1}
    client.post("/lab/notificacoes/falha",json={"ativo":True})
    assert client.post("/notificacoes",json=evento).status_code==503
    client.post("/lab/notificacoes/falha",json={"ativo":False})
    assert client.post("/notificacoes",json=evento).json()["duplicado"] is False
    assert client.post("/notificacoes",json=evento).json()["duplicado"] is True
    assert client.get("/lab/notificacoes").json()["recebidas"]==1

def test_gateway_transforma_e_deduplica_duravelmente(tmp_path):
    topic="lab/instituicao-1/dispositivo-1/eventos"
    payload='{"id":"evt1","device":"dispositivo-1","institution":"instituicao-1","user_id":1,"event":"conclusao"}'
    evento=transformar(topic,payload);assert evento["tipo"]=="CONCLUSAO"
    spool=Spool(tmp_path/"iot.db");spool.salvar(evento);spool.salvar(evento)
    reiniciado=Spool(tmp_path/"iot.db");assert len(reiniciado.pendentes())==1
    reiniciado.resultado("evt1",True);assert reiniciado.pendentes()==[]

def test_gateway_rejeita_topico_incompativel():
    with pytest.raises(ValueError): transformar("lab/outra/dispositivo-1/eventos",'{"id":"evt1","device":"dispositivo-1","institution":"instituicao-1","user_id":1,"event":"conclusao"}')

def test_dispositivo_preserva_saida_ate_confirmacao(tmp_path):
    from simulador import enfileirar,replay
    path=tmp_path/'saida.db';evento={'id':'offline','event':'presenca'}
    enfileirar(path,evento)
    def indisponivel(payload):raise ConnectionError('sem rede')
    with pytest.raises(ConnectionError):replay(path,indisponivel)
    recebidos=[];assert replay(path,recebidos.append)==1
    assert len(recebidos)==1;assert replay(path,recebidos.append)==0
