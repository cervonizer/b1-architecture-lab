# Evidências do Desafio 4

O [ADR 004](../../adr/ADR-004.md) define hipótese, alternativas, decisão e limites. `experimento.json` registra as etapas com timestamp UTC e identificador da execução real.

A execução é reproduzida por `scripts/rodar_microlabs.py`, com serviços reais iniciados em portas de laboratório. Os testes de regressão Java e Python e seus logs estão em `../desafio6/`.

O consumidor retorna 503, a conclusão transacional continua, a pendência permanece e é entregue após recuperação. O comando de conclusão repetido não duplica créditos. A outbox usa o banco relacional; com H2 em memória a persistência é limitada à sessão.
