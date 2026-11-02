# Estrutura do produto

O Core e um monolito modular Java 17 com Spring Boot. Usuario, Curso, Matricula e Ranking sao capacidades internas. O Ranking tem dominio Java puro e uma porta para obter dados. A recomendacao e o assistente sao atendidos por um servico Python separado. Prometheus coleta metricas e Grafana exibe o dashboard. Jenkins executa testes e os experimentos de falha.
