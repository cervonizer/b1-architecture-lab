# Evidências do Desafio 6

O [ADR 006](../../adr/ADR-006.md) justifica a esteira coordenada, as métricas e os bloqueadores. A validação final foi executada no job local `B1_Architecture_Lab`, build **2**, em **27 de outubro de 2026**. Estes resultados são daquela execução; a preparação da entrega em 2 de novembro não representa uma nova execução dos experimentos.

## Resultado final

- Jenkins **SUCCESS**, duração de **101,32 segundos**.
- **24 testes Java + 12 testes Python = 36 aprovados**, sem falhas ou ignorados.
- Os dois testes de geração usam o Qwen local de verdade, habilitados por `B1_TESTAR_LLM=1`.
- Verificação de fronteiras arquiteturais aprovada.
- Experimentos integrados aprovados: recomendador treinado, LLM com fontes, interrupção do Python e continuidade do Core, consumidor indisponível e recuperação, replay MQTT e consultas Prometheus.
- Identificador da execução integrada: `c8f6e821-12cf-4d9e-a2dc-1a9ab9f21ba2`.

## Como conferir

`jenkins-build.json` contém o resultado, o instante e a duração extraídos de `build.xml`. `jenkins-console.log` contém o console do build 2, removidas somente as anotações binárias de apresentação do Jenkins. `jenkins-junit-result.xml` preserva o relatório consolidado; os arquivos `TEST-*.xml` e `python-tests.xml` detalham as suítes. `jenkins-tests.json` resume a contagem.

Os JSONs `experimento.json` dos desafios 3 a 6 foram copiados dos artefatos arquivados pelo build 2. Os arquivos `*-build2.log` são logs dos processos dessa execução. `maven-verify.log` e `pytest.log` preservam a validação local anterior com os mesmos 24 testes Java e 12 Python, identificável pelos próprios caminhos e timestamps.

## Observabilidade

`experimento.json` registra as consultas ao Prometheus no build 2: fallback real de IA, alvo Core UP e fila pendente após falha do consumidor. `metricas.prom` e `grafana-falhas.png` preservam uma execução anterior do laboratório; a imagem comprova a visualização no Grafana e não é apresentada como captura do build 2. Os arquivos sem sufixo `build2` de execução de processos também pertencem à validação anterior.

`historico-build1/` preserva a primeira execução, com 28 testes e IA simulada. Seus resultados e imagens são históricos e não representam a versão final.

## Ambiente e limites

A esteira usou `SOURCE_DIR` local. Não foi demonstrado checkout remoto nem webhook GitHub. O Jenkinsfile permite `checkout scm` quando o job é configurado para o repositório.

Core Java, IA e gateway foram processos nativos; Mosquitto, Prometheus e Grafana foram containers. O Jenkins local isolado usou porta 19090. A inferência do LLM foi validada no Mac; a imagem Docker Python não foi executada nesta validação.

O recomendador foi treinado com dados sintéticos. O Qwen é pré-treinado, sem ajuste pela equipe. A amostra de laboratório não comprova SLA ou capacidade para 100 mil usuários. O experimento usa H2; existe perfil PostgreSQL, mas este conjunto não o valida. A instância local não representa configuração de produção.

O repositório é público. O envio da tarefa no Canvas ainda precisa ser concluído.
