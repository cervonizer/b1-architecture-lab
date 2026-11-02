"""Baixa apenas pesos e configuracoes oficiais; nao envia perguntas a servicos externos."""
from pathlib import Path
import os,json,hashlib
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY','1')
os.environ.setdefault('HF_HUB_DISABLE_XET','1')
from huggingface_hub import snapshot_download

ROOT=Path(__file__).resolve().parents[1]
MODEL_ID='Qwen/Qwen2.5-0.5B-Instruct'
REVISION='7ae557604adf67be50417f59c2c2f167def9a775'
path=Path(os.getenv('B1_LLM_DIR',str(ROOT/'.cache/modelos/qwen2.5-0.5b'))).resolve()
path.mkdir(parents=True,exist_ok=True)
snapshot_download(MODEL_ID,revision=REVISION,local_dir=path,token=False,
    allow_patterns=['*.json','*.safetensors','merges.txt','vocab.json','LICENSE','README.md'],max_workers=3)
weights=path/'model.safetensors'
meta={'model_id':MODEL_ID,'revision':REVISION,'license':'Apache-2.0','arquivo':'model.safetensors',
      'bytes':weights.stat().st_size,'sha256':hashlib.sha256(weights.read_bytes()).hexdigest()}
(path/'B1_MODEL_MANIFEST.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta,indent=2))
print('LLM disponivel em',path)
