# Evidências do Desafio 5

O [ADR 005](../../adr/ADR-005.md) define hipótese, alternativas, decisão e limites. `experimento.json` registra as etapas com timestamp UTC e identificador da execução real.

A execução é reproduzida por `scripts/rodar_microlabs.py`, com serviços reais iniciados em portas de laboratório. Os testes de regressão Java e Python e seus logs estão em `../desafio6/`.

Mosquitto é um broker MQTT real. Há replay do spool depois de reiniciar o gateway, fila de sessão MQTT com gateway offline e fila local do simulador quando não consegue publicar. O Core deduplica eventId. Não se usou HTTP direto como substituto de MQTT no experimento.
