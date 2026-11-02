from pathlib import Path
import json
from recomendador import recomendar,carregar_modelo
from rag_engine import RagEngine

ROOT=Path(__file__).resolve().parents[1]

def test_treino_e_teste_nao_compartilham_perfis():
    _,meta=carregar_modelo()
    assert set(meta['perfis_treino']).isdisjoint(meta['perfis_teste'])
    assert meta['treino']==195 and meta['teste']==75
    assert meta['metricas_teste']['f1']>0

def test_modelo_muda_ranking_conforme_interesse():
    cursos=json.loads((ROOT/'dados/catalogo_laboratorio.json').read_text())
    java=recomendar(['java','arquitetura'],2,cursos)['cursos']
    iot=recomendar(['iot','mqtt'],2,cursos)['cursos']
    assert java[0]['id']!=iot[0]['id']
    assert iot[0]['id'] in [9,10,14]

def test_modelo_usa_catalogo_recebido_e_nao_lista_fixa():
    cursos=[{'id':901,'titulo':'Java e arquitetura','descricao':'spring java arquitetura modular'},
            {'id':902,'titulo':'Sensores MQTT','descricao':'iot mqtt sensores dispositivos'}]
    r=recomendar(['iot','mqtt'],2,cursos)
    assert {c['id'] for c in r['cursos']}=={901,902}
    assert r['cursos'][0]['id']==902

def test_recuperacao_aponta_para_regra_versionada():
    fontes=RagEngine().recuperar('Quantos creditos recebo ao concluir um curso com aproveitamento?')
    assert 'creditos' in [x['id'] for x in fontes]
    assert all(x['arquivo'] and x['trecho'] for x in fontes)
