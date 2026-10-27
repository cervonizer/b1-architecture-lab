# Evidências do Desafio 3

O [ADR 003](../../adr/ADR-003.md) define hipótese, alternativas, decisão e limites. `experimento.json` registra as etapas com timestamp UTC e identificador da execução real.

A execução é reproduzida por `scripts/rodar_microlabs.py`, com serviços reais iniciados em portas de laboratório. Os testes de regressão Java e Python e seus logs estão em `../desafio6/`.

O processo FastAPI é encerrado de propósito; o Core usa fallback e mantém consulta de cursos. Recomendação é catálogo fixo e assistente é recuperação lexical sem LLM. Isso testa fronteira e tolerância a falhas, não qualidade de modelos.
