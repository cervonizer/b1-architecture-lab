"""Classificador supervisionado de relevancia. Nao devolve uma lista fixa."""
from pathlib import Path
from functools import lru_cache
import hashlib,json,os,re,unicodedata
import numpy as np
import joblib

ROOT=Path(__file__).resolve().parent
STOP={'a','o','as','os','de','da','do','das','dos','em','e','com','para','por','um','uma','ao','na','no','como','qual','que'}

def normalizar(texto):
    texto=''.join(c for c in unicodedata.normalize('NFKD',texto.lower()) if not unicodedata.combining(c))
    return ' '.join(w for w in re.findall(r'[a-z0-9]+',texto) if w not in STOP)

def texto_curso(curso):return normalizar(curso['titulo']+' '+curso.get('descricao','')+' '+' '.join(curso.get('tags',[])))

def features(vectorizer,interesses,nivel,curso):
    perfil=normalizar(' '.join(interesses) if isinstance(interesses,list) else interesses)
    texto=texto_curso(curso);v=vectorizer.transform([perfil,texto])
    similaridade=float((v[0]@v[1].T).toarray()[0,0])
    termos=set(perfil.split());overlap=len(termos & set(texto.split()))/max(1,len(termos))
    delta=int(curso.get('nivel',1))-int(nivel)
    return [similaridade,overlap,float(max(0,delta)),float(abs(delta))]

@lru_cache(maxsize=1)
def carregar_modelo():
    path=Path(os.getenv('B1_ML_MODEL',str(ROOT/'modelos/recomendador.joblib')))
    metadata=json.loads(path.with_suffix('.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=metadata['sha256_modelo']:
        raise RuntimeError('Artefato do recomendador nao corresponde ao hash versionado')
    return joblib.load(path),metadata

def recomendar(interesses,nivel,cursos,limite=5):
    bundle,meta=carregar_modelo()
    if not cursos:return {'fonte':'modelo-supervisionado','degradado':False,'cursos':[],'modelo':meta['versao'],'modelo_sha256':meta['sha256_modelo']}
    X=np.array([features(bundle['vectorizer'],interesses,nivel,c) for c in cursos])
    probabilidades=bundle['classificador'].predict_proba(X)[:,1]
    ordem=sorted(range(len(cursos)),key=lambda i:(-float(probabilidades[i]),str(cursos[i]['id'])))[:limite]
    resultado=[{'id':cursos[i]['id'],'titulo':cursos[i]['titulo'],'relevancia_estimada':round(float(probabilidades[i]),6)} for i in ordem]
    return {'fonte':'modelo-supervisionado','degradado':False,'cursos':resultado,'perfil':{'interesses':interesses,'nivel':nivel},
            'modelo':meta['versao'],'modelo_sha256':meta['sha256_modelo'],'treinamento':'dados-sinteticos-de-laboratorio'}
