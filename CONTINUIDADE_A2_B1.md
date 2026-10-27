# Relação entre o A2 e o B1

O usuário esclareceu que o trabalho anterior realizado em conjunto foi o A2, não a AC1. A conversa recuperada foi “Inspecionar projetos do Exercício A2”, com os projetos `cervonizer/a2-pratica1-integracao` e `cervonizer/a2-jogo-enigma`.

## O que já existe do A2

Foram localizados o Jenkinsfile do Jogo Enigma, os arquivos Compose de desenvolvimento e homologação, a configuração Prometheus, o datasource Grafana e o dashboard exportado. O relatório do A2 registra testes JUnit, cobertura JaCoCo, análise PMD, build Docker, homologação com PostgreSQL e BFF, health check, Cypress e observabilidade via Actuator/Prometheus/Grafana. Isso é evidência histórica; a disponibilidade atual dos serviços precisa ser verificada antes da reutilização.

Repositórios:
- https://github.com/cervonizer/a2-pratica1-integracao
- https://github.com/cervonizer/a2-jogo-enigma

## Como aproveitar no B1

Os projetos de monólito anexados ao B1 seguem como base imediata do exercício. O A2 fornece referências de esteira, implantação e observabilidade para o Desafio 6. Será necessário adaptar nomes de artefatos, serviços, portas, testes e métricas ao Core do B1 e aos componentes que forem efetivamente escolhidos nos desafios anteriores. Os prints e builds do A2 não comprovam os ASRs nem a execução do B1.

O A2 não deve ser identificado como a AC1 de gamificação mencionada no enunciado. A relação com uma eventual implementação própria da AC1 só precisará de esclarecimento se a professora exigir sua utilização em lugar das bases que forneceu para o B1. Isso não bloqueia o início pelos anexos atuais.

## Fontes consultadas

Conversa anterior recuperada pelo aplicativo e arquivos locais do A2, incluindo o Jenkinsfile em `work/a2_projects/jogo_enigma/jogo-enigma-api-v1-A2-corrigido/jogo-enigma-api-v1-A2-corrigido/` e os fontes do relatório em `tmp/pdfs/build_report.py`, no espaço de trabalho de 5 de outubro de 2026. O link compartilhado informado pelo usuário não carregou no leitor web; ele não foi usado como fonte para afirmações novas.
