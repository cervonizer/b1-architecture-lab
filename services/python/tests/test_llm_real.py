"""Estes testes fazem inferencia real, sem mock do modelo."""
import os,re
import pytest
from rag_engine import get_engine
from recomendador import normalizar

pytestmark=pytest.mark.skipif(os.getenv('B1_TESTAR_LLM')!='1',reason='Ative B1_TESTAR_LLM=1 depois de preparar os pesos locais')

def test_llm_real_gera_resposta_com_creditos_e_fonte():
    r=get_engine().responder('Quantos creditos recebo ao concluir um curso com aproveitamento?')
    resposta=normalizar(r['resposta'])
    assert r['geracao']['executada'] is True
    assert r['geracao']['classe']=='Qwen2ForCausalLM'
    assert r['geracao']['parametros']>100_000_000
    assert r['geracao']['tokens_gerados']>0
    assert 'creditos' in [f['id'] for f in r['fontes']]
    assert re.search(r'\b3\b|\btres\b',resposta) and 'credit' in resposta

def test_llm_real_responde_exemplo_de_pontuacao():
    r=get_engine().responder('Com dois cursos concluidos e sete moedas, quantos pontos tenho no ranking?')
    assert r['geracao']['executada'] is True
    assert '207' in r['resposta']
    assert 'ranking' in [f['id'] for f in r['fontes']]
