# Guia de demonstração e entrega do B1 completo

## O que entregar

Link de repositório acessível à professora, equipe identificada, registro cumulativo com seis decisões e matriz de ASRs, seis ADRs, C4 final, microsoluções/evidências e síntese das escolhas levadas à PoC da AF. O prazo exibido no Canvas é 4 de novembro de 2026 às 23h59. Não foi realizado envio da tarefa.

## Roteiro de demonstração

1. Mostrar o registro em docs/arquitetura/README.md, com três ASRs por desafio e as RPCs.
2. D1: comparar pacotes em camadas com módulos e APIs públicas; mostrar dependências antes/depois.
3. D2: executar testes de domínio e contrato MEMORIA/JPA. Explicar a porta e a ordenação em memória.
4. D3: mostrar JSON com Python disponível, interrompido e consulta essencial funcionando. Explicar que a IA é simulação do contrato, sem LLM real.
5. D4: comparar HTTP 503 síncrono com conclusão 200 assíncrona; mostrar pendência e recuperação, sem duplicar créditos.
6. D5: mostrar MQTT real, spool, sessão offline e replay do dispositivo; diferenciar QoS 1 de deduplicação de negócio.
7. D6: mostrar Jenkins, 22 testes Java, 6 Python e dashboard de fallback/fila/ingestão. Explicar o que cada métrica comprova e seus limites.
8. Encerrar com a síntese para a AF e os limites de produção.

## Ambiente

O README da raiz contém os comandos completos. A aplicação de laboratório usa porta 18080; o serviço Python 18081; Mosquitto 18883; Prometheus 19091; Grafana 13001. Uma instância Jenkins isolada foi usada na porta 19090, com JDK 17 para o build. O uso de fonte local no Jenkins não equivale a webhook GitHub.

No IntelliJ, abra esta raiz, que contém pom.xml, e use SDK 17. A aplicação antiga da porta 8080 pode continuar aberta, mas pertence à etapa anterior; suas capturas são preservadas como evidência histórica D1.

## Publicação

Repositório privado criado para esta entrega: https://github.com/cervonizer/b1-architecture-lab. Antes de enviar o link no Canvas, conceder acesso à professora. O ZIP é uma cópia editável adicional. Nenhuma submissão foi feita no Canvas.

O histórico Git local permite rastrear os desafios iniciais e as evoluções finais. Os logs mostram resultados reais e não devem ser substituídos por alegações de capacidades não testadas.
