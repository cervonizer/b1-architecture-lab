# Evidências do Desafio 6

O [ADR 006](../../adr/ADR-006.md) justifica pipeline coordenado, métricas e bloqueadores. O Jenkinsfile foi executado de verdade no job local `B1_Architecture_Lab`, build 1, em 27 de outubro de 2026.

## Resultado

- Resultado final SUCCESS, duração de 45,86 segundos.
- 22 testes Java e 6 testes Python publicados pelo Jenkins, todos aprovados, sem ignorados.
- Estágio de fronteiras aprovado.
- Estágio de implantação e experimentos aprovado, incluindo FastAPI interrompido, consumidor indisponível, replay de gateway e dispositivo MQTT e coleta Prometheus.

`jenkins-build.json` contém metadados e lista de artefatos arquivados; `jenkins-console.log` contém o console integral; `jenkins-tests.json` contém o relatório publicado. As capturas `jenkins-success.png` e `jenkins-28-testes.png` permitem conferir visualmente o resultado.

## Observabilidade

`experimento.json` registra as consultas Prometheus: fallback real de IA, alvo b1-core UP e fila pendente depois de falhar o consumidor. `metricas.prom` preserva a exposição do Core. `grafana-falhas.png` mostra o dashboard com os contadores e a pendência, em uma execução manual anterior do mesmo laboratório; a captura não é apresentada como print do build Jenkins.

Os JSONs D3 a D6 foram atualizados com a execução Jenkins de run_id 7f4ec76c-8303-46f9-8469-92d71e9b152b. Os logs dos processos e os XMLs de testes publicados foram copiados do workspace dessa execução. Os logs maven-verify.log e pytest.log preservam também a validação local anterior, identificada pelos próprios timestamps.

## Fonte e ambiente

O build usou SOURCE_DIR local porque o repositório privado foi criado depois da validação. Não houve checkout remoto ou webhook GitHub demonstrado. O mesmo Jenkinsfile pode usar checkout scm quando o job for configurado para o repositório.

Core, IA e gateway foram processos locais em portas próprias; Mosquitto, Prometheus e Grafana foram containers. O laboratório Jenkins é uma instância separada no loopback 19090, sem copiar usuários/segredos do Jenkins anterior. Ele não representa uma configuração de segurança de produção.

## Limites

Amostra curta não é SLA nem teste de 100 mil usuários. Recomendação é simulação e assistente não usa LLM. H2 é o banco do experimento; a base mantém perfil PostgreSQL. O envio no Canvas e o acesso da professora ao repositório privado não foram executados.
