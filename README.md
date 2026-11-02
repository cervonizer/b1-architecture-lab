# B1 Architecture Lab completo

Seis desafios de decisão arquitetural, com Core Java/Spring Boot, laboratório Python/FastAPI, eventos com outbox, MQTT e Jenkins/Prometheus/Grafana. A suíte passou com 24 testes Java e 12 testes Python. Os experimentos executam falhas e recuperação de processos reais.

## Leitura principal

- [Registro arquitetural e matriz de ASRs](docs/arquitetura/README.md).
- [Seis ADRs](docs/adr/ADR-001.md), a partir do ADR 001.
- [Guia para executar e entregar](GUIA_ENTREGA.md).
- [Evidência da esteira e observabilidade](docs/evidencias/desafio6/README.md).
- [Prazo e fontes oficiais no Canvas](docs/fontes-canvas/README.md).

A equipe, requisitos, alternativas, trade offs e síntese para a AF estão no registro cumulativo. A consulta ao Canvas confirmou os quatro anexos usados como base e a entrega B1 em 4 de novembro de 2026 às 23h59. Nenhuma tarefa foi enviada automaticamente.

## Testes

Com JDK 17 e Maven:

```sh
mvn verify
python3 -m venv .venv
.venv/bin/python -m pip install -r services/python/requirements.lock.txt
.venv/bin/python scripts/preparar_llm.py
B1_TESTAR_LLM=1 PYTHONPATH=services/python .venv/bin/python -m pytest services/python/tests -q
python3 scripts/verificar_fronteira.py
```

A versão Python testada é 3.12. O lock registra as versões efetivamente resolvidas. Os testes de domínio do Ranking continuam podendo rodar isoladamente sem banco/Spring.

## Laboratório integrado

Requer Docker Desktop e portas 18080, 18081, 18883, 19091 e 13001 disponíveis. As configurações MQTT fornecidas usam credenciais didáticas e ACL, vinculadas ao loopback.

```sh
docker compose -f compose.lab.yml up -d
B1_JAVA="$JAVA_HOME/bin/java" .venv/bin/python scripts/rodar_microlabs.py --keep-running
```

Use JAVA_HOME apontando para JDK 17. Sem `--keep-running`, o experimento encerra os processos de Core, IA e gateway que ele mesmo criou depois de salvar as evidências. Ele não interrompe a aplicação da porta 8080. O perfil H2 usa dados de laboratório, descartados ao reiniciar o Core.

Painéis locais: Grafana http://localhost:13001 e Prometheus http://localhost:19091. Grafana do laboratório usa admin / b1-grafana-lab. Core de laboratório: http://localhost:18080/index.html, HTTP Basic admin / 123456.

## Esteira

`Jenkinsfile` usa ferramentas nomeadas JDK17 e Maven. Sem repositório remoto configurado, SOURCE_DIR permite uma cópia local da fonte para o laboratório. Com SCM configurado, deixe SOURCE_DIR vazio. O job publica JUnit e arquiva artefatos e evidências; a execução real está registrada nos arquivos D6.

## Escopo e limites

É uma entrega de arquitetura com microsoluções. A recomendação usa modelo supervisionado treinado em dados sintéticos; o assistente usa recuperação de documentos e um LLM local real. O Core mantém entidades JPA existentes e a conversão completa de todos os módulos para Hexagonal não foi realizada. Ordenação do Ranking em memória, filas e banco precisam de validação de capacidade antes de produção. Credenciais didáticas não são destinadas a ambientes remotos.

A pasta `fontes/` preserva materiais originais, e `baseline-camadas/` é somente comparação. O mock_spring foi identificado como apoio do A3. Repositório público de entrega: https://github.com/cervonizer/b1-architecture-lab. O envio no Canvas ainda precisa ser concluído.

## IA real

Abra http://localhost:18080/ia.html durante o laboratório para usar o recomendador e o assistente. O modelo de recomendação e seus metadados são versionados. O LLM Qwen2.5 0.5B roda localmente; os pesos de aproximadamente 1 GB são baixados com revisão fixa e ficam fora do Git. O corpus possui fontes do próprio projeto. Ver o ADR 003 para métricas e limites.
