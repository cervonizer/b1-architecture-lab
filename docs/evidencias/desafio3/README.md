# Evidencias do Desafio 3 com IA real

A versao atual substitui a simulacao anterior. O [ADR 003](../../adr/ADR-003.md) registra a decisao e os limites.

## O que foi executado

- Treino real de LogisticRegression: 195 pares de treino e 75 de teste, sem compartilhar perfis entre os grupos.
- Avaliacao do classificador em dados sinteticos; F1 de 0,7692 e accuracy de 0,92, com baseline de accuracy 0,84.
- Inferencia do artefato treinado para perfis distintos; o Core envia seu catalogo realmente cadastrado.
- Recuperacao TF-IDF de documentos do projeto seguida de geracao pelo Qwen2.5 0.5B Instruct local.
- Respostas geradas e verificadas sobre creditos, pontuacao, notificacao e indisponibilidade de IA, alem de abstencao fora do corpus.
- Interrupcao do processo Python, fallback do Core e continuidade da consulta de cursos.

## Arquivos

`treinamento.json` descreve dataset, grupos, metricas e hashes. O CSV e o artefato ficam em `services/python/dados/` e `services/python/modelos/`, na raiz do projeto.

`avaliacao-rag.json` guarda perguntas, respostas completas e fontes. `inferencia-real.log` registra execucao real. `llm-pesos-manifest.json` identifica revisao, tamanho e SHA256 dos pesos, que nao sao publicados no Git.

`experimento.json` registra a integracao Java/Python e as falhas com timestamp. Os relatorios finais da esteira estao na pasta D6. `historico-simulacao/` preserva a versao anterior somente como historico da correcao.

## Reproduzir

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r services/python/requirements.lock.txt
.venv/bin/python services/python/treinar_modelo.py
.venv/bin/python scripts/preparar_llm.py
B1_TESTAR_LLM=1 PYTHONPATH=services/python .venv/bin/python -m pytest services/python/tests -q
```

Use B1_LLM_DIR para escolher outro cache dos pesos. Sem B1_TESTAR_LLM=1, os dois testes de geracao ficam explicitamente ignorados; a execucao final Jenkins habilita ambos. Os testes unitarios de contrato HTTP podem usar stubs, enquanto a avaliacao e os testes de LLM registrados aqui fazem inferencia real.

## Limites

O dataset e sintetico e pequeno; nao se promete acuracia para alunos reais. O LLM e pre-treinado, sem fine tuning pela equipe. A avaliacao factual e limitada. O primeiro carregamento requer download publico de aproximadamente 1 GB, mas nenhuma pergunta ou dado de aluno e enviado para uma API externa. A imagem Docker Python foi adaptada para montar os pesos, mas a validacao de inferencia foi feita em processos nativos no Mac.
