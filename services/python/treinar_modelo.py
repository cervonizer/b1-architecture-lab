"""Treina e avalia sem misturar perfis entre treino e teste."""
from pathlib import Path
import json,csv,hashlib,datetime
import numpy as np
import sklearn,joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GroupShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
from recomendador import normalizar,texto_curso,features

ROOT=Path(__file__).resolve().parent

def treinar(saida=None):
    csv_path=ROOT/'dados/relevancia_sintetica.csv'
    dados=list(csv.DictReader(csv_path.open()))
    catalogo=json.loads((ROOT/'dados/catalogo_laboratorio.json').read_text());por_id={c['id']:c for c in catalogo}
    groups=np.array([r['perfil_id'] for r in dados]);y=np.array([int(r['relevante']) for r in dados])
    train,test=next(GroupShuffleSplit(n_splits=1,test_size=.25,random_state=42).split(dados,y,groups))
    assert set(groups[train]).isdisjoint(set(groups[test]))
    # Metadados do catalogo sao conhecidos; perfis de teste nao entram no fit do vocabulário.
    corpus=[texto_curso(c) for c in catalogo]+[normalizar(dados[i]['interesses']) for i in train]
    vectorizer=TfidfVectorizer(ngram_range=(1,2)).fit(corpus)
    X=np.array([features(vectorizer,r['interesses'],int(r['nivel']),por_id[int(r['curso_id'])]) for r in dados])
    modelo=make_pipeline(StandardScaler(),LogisticRegression(class_weight='balanced',random_state=42,max_iter=1000))
    modelo.fit(X[train],y[train]);pred=modelo.predict(X[test]);prob=modelo.predict_proba(X[test])[:,1]
    metricas={'accuracy':float(accuracy_score(y[test],pred)),'precision':float(precision_score(y[test],pred,zero_division=0)),
              'recall':float(recall_score(y[test],pred,zero_division=0)),'f1':float(f1_score(y[test],pred,zero_division=0)),
              'roc_auc':float(roc_auc_score(y[test],prob)),
              'baseline_accuracy_sempre_negativo':float(accuracy_score(y[test],np.zeros_like(y[test])))}
    path=Path(saida or ROOT/'modelos/recomendador.joblib');path.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump({'vectorizer':vectorizer,'classificador':modelo},path,compress=3)
    meta={'versao':'logistic-relevance-v1','tipo':'LogisticRegression supervisionada com TFIDF e atributos de perfil',
          'dados':'270 pares sinteticos, 18 perfis e 15 cursos; sem dados de alunos reais',
          'treino':len(train),'teste':len(test),'perfis_treino':sorted(set(groups[train])),'perfis_teste':sorted(set(groups[test])),
          'seed':42,'metricas_teste':metricas,'sklearn':sklearn.__version__,
          'sha256_dataset':hashlib.sha256(csv_path.read_bytes()).hexdigest(),
          'sha256_modelo':hashlib.sha256(path.read_bytes()).hexdigest(),
          'instante_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'limite':'Avaliacao pequena e sintetica; nao comprova qualidade em producao.'}
    path.with_suffix('.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
    return meta

if __name__=='__main__':print(json.dumps(treinar(),ensure_ascii=False,indent=2))
