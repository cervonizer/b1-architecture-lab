"""Compara imports do Ranking usando os ZIPs originais e o projeto evoluído.
Uso: python3 scripts/comparar_dependencias.py > docs/evidencias/desafio1/dependencias.json
"""
from pathlib import Path
from zipfile import ZipFile
import re
import json

projeto = Path(__file__).resolve().parents[1]
pacote = projeto

def medir(arquivos, modular):
    imports = []
    for nome, texto in sorted(arquivos.items()):
        if '/ranking/' in nome or Path(nome).name.startswith('Ranking'):
            for alvo in re.findall(r'^import (com\.exemplo\.usuario\.[\w.*]+);', texto, re.M):
                imports.append({'arquivo': nome, 'import': alvo})
    externos = [x for x in imports if x['import'].split('.')[3] != 'ranking'] if modular else []
    return {
        'arquivos_java_producao': len(arquivos),
        'imports_ranking': imports,
        'imports_intermodulares_ranking': externos,
        'imports_intermodulares_nao_api_ranking': [x for x in externos if x['import'].split('.')[4] != 'api'],
    }

resultado = {}
for tipo in ['Camadas', 'Modular']:
    with ZipFile(pacote / 'fontes' / f'B1_Desafio1_Monolito_{tipo}.zip') as arquivo:
        textos = {n.split('/src/main/java/', 1)[1]: arquivo.read(n).decode()
                  for n in arquivo.namelist()
                  if '/src/main/java/' in n and n.endswith('.java') and not n.startswith('__MACOSX/')}
    resultado[tipo.lower() + '_original'] = medir(textos, tipo == 'Modular')
base = projeto / 'src/main/java'
textos = {f.relative_to(base).as_posix(): f.read_text() for f in base.rglob('*.java')}
resultado['modular_evoluido'] = medir(textos, True)
print(json.dumps(resultado, ensure_ascii=False, indent=2))
