# Requisitos e comparação do B1

## Conclusão

O B1 vale 6,0 pontos e exige seis decisões arquiteturais evolutivas sobre o mesmo produto da AC1, com 1,0 ponto por desafio. A entrega é um registro vivo no Git, não seis aplicações independentes. A opção inicial proposta é um monólito modular, mas os ZIPs não comprovam redução de acoplamento apenas pela mudança de pastas. Foi iniciada uma melhoria concreta da fronteira de leitura do Ranking.

Fontes primárias: `fontes/Exercicio_B1_Architecture_Lab_6_Desafios_Reavaliado.docx` (requisitos e critérios), `fontes/Exemplo_Solucao_Desafio_1_Architecture_Lab_B1.docx` (exemplo orientativo) e os dois ZIPs preservados em `fontes/`. O exemplo não adiciona obrigação de escolher monólito modular. As descrições nos READMEs dos ZIPs são hipóteses didáticas que precisam ser confrontadas com o código.

## Exigências comuns aos seis desafios

1. Identificar RFs e RNFs afetados; classificar RNFs por FURPS+ quando pertinente.
2. Selecionar no máximo três RNFs como ASRs por desafio. Para cada ASR, escrever uma frase explicando como altera estrutura, comunicação, dados, implantação ou operação.
3. Registrar RPCs como requisitos, restrições ou premissas; não confundir decisões propostas com restrições impostas.
4. Comparar pelo menos duas alternativas com trade-offs; cumprir as comparações específicas de cada cenário.
5. Registrar ADR com contexto, ASRs/RPCs, alternativas, decisão e consequências.
6. Atualizar C4 no nível afetado. Container é a visão mínima; Component quando envolver organização interna do Core.
7. Implementar uma microsolução que teste uma hipótese arquitetural e versionar evidência real.
8. Manter `/docs/arquitetura/README.md` cumulativo. ADRs podem ficar nesse README ou em `/docs/adr/`. A matriz de ASRs evolui ao longo do B1.

A cadeia obrigatória é RF → RNF → ASR + RPC → alternativas e trade-offs → ADR → C4 → evidência. Uma tecnologia precisa resolver um problema do case; popularidade e modernidade não bastam.

| Critério por desafio | Pontos |
| --- | ---: |
| RF/RNF e seleção dos ASRs | 0,25 |
| RPC e alternativas/trade-offs | 0,20 |
| ADR e justificativa | 0,20 |
| C4 coerente | 0,15 |
| Microsolução/evidência e Git | 0,20 |

Entrega final: link do repositório e identificação da equipe; README com seis decisões e matriz cumulativa de ASRs; ADRs essenciais e C4 final coerente; links/pastas das microsoluções e evidências; síntese das decisões levadas à PoC da Avaliação Final. O enunciado não fixa SLA, concorrência, prazo de entrega, quantidade de páginas ou necessidade de implementar seis arquiteturas completas.

## Requisitos por desafio

### Desafio 1 Drivers e evolução do Core

Cenário: crescimento de 1.000 para até 100.000 usuários, com Ranking crescendo mais que outras funções. Isso não informa usuários simultâneos nem prova um gargalo.

- RF01 Ranking e RF02 Conquistas; evolução das funções existentes.
- RNFs a analisar: manutenibilidade, desempenho, escalabilidade, testabilidade e complexidade operacional.
- RPCs: Java/Spring Boot no Core, seis desenvolvedores, banco relacional e legado da AC1.
- Comparações obrigatórias: monólito em camadas, monólito modular e decomposição seletiva em serviços.
- Questão: há evidência de escala/deploy independente que justifique distribuição?
- Mini-lab: reorganizar uma funcionalidade da AC1 em uma estrutura modular pequena e comparar dependências antes/depois.
- ADR e C4 Container; explicitar impacto interno e preparar Component para o Desafio 2.

### Desafio 2 Organização interna do Core

- RF01 Ranking e RF02 Conquistas/regras de gamificação.
- RNFs: manutenibilidade, testabilidade, modificabilidade e facilidade de evolução.
- RPCs: Core continua Spring Boot; reaproveitar regras existentes; não reescrever o produto inteiro para aplicar um padrão.
- Comparar arquitetura atual com Ports & Adapters/Hexagonal ou equivalente; justificar eventual combinação com DDD/Clean/Onion.
- Identificar a dependência que precisa ser invertida e avaliar o custo da estrutura.
- Mini-lab: isolar uma regra de domínio e trocar pelo menos um adapter, por exemplo fake/mock versus JPA, mantendo testes do domínio.
- ADR e C4 Component do Core.

### Desafio 3 Serviço Python e IA

- RF03 Recomendação inteligente e RF04 Assistente educacional.
- RNFs: deploy independente, escalabilidade, tolerância a falhas, interoperabilidade, desempenho e manutenibilidade.
- RPCs: Core em Java/Spring Boot; ML/RAG em Python; indisponibilidade da IA não pode bloquear o fluxo essencial.
- Comparar IA embutida, módulo acoplado e serviço Python independente; discutir ML/RAG juntos ou separados. Python isoladamente não basta como justificativa arquitetural.
- Definir fronteira, comportamento degradado e ASRs que justificam autonomia/escala.
- Mini-lab: Spring Boot consome FastAPI; parar Python e observar/tratar a falha.
- ADR e C4 Container com protocolos e fronteira de IA.

### Desafio 4 Comunicação e eventos

- RF02 Conquistas e RF05 Notificações; eventos de conclusão de atividades.
- RNFs: tolerância a falhas, disponibilidade, latência, consistência, desacoplamento e recuperabilidade.
- RPCs: operações essenciais concluem com consumidor externo indisponível; broker tem custo operacional.
- Comparar REST síncrono e comunicação assíncrona; se houver broker, comparar RabbitMQ e Kafka pelo problema concreto.
- Definir resposta imediata, consistência eventual e ASR que justifica mensageria.
- Mini-lab: implementar uma interação síncrona e uma assíncrona; simular consumidor indisponível e registrar o efeito.
- ADR e C4 Container; sequência simplificada quando necessária para demonstrar o fluxo crítico.

### Desafio 5 IoT e MQTT

- RF06 Receber eventos IoT e encaminhá-los à plataforma; presença, início e conclusão em laboratórios.
- RNFs: interoperabilidade, eficiência de comunicação, disponibilidade, tolerância à conectividade intermitente, escalabilidade e segurança de integração.
- RPCs: dispositivos de baixo poder computacional, conexão intermitente, custo operacional de protocolo/broker.
- Comparar REST direto, MQTT com consumidor e MQTT com integração posterior à mensageria interna; essa última depende de ASR que a justifique.
- Discutir duplicidade, perda relevante e necessidade de segundo broker.
- Mini-lab: simulador publica em broker MQTT; consumidor recebe e transforma para uso da aplicação.
- ADR e C4 Container com dispositivos, broker, consumidor/gateway e Core; fluxo quando útil.

### Desafio 6 CI CD e observabilidade

- RFs de todos os componentes construídos e operação/evolução.
- RNFs: observabilidade, deploy independente, confiabilidade, testabilidade, recuperabilidade e desempenho.
- RPCs: Jenkins como base da esteira; Prometheus/Grafana como ferramentas do laboratório; artefatos/configurações versionados.
- Comparar pipeline único e pipelines por componente; definir bloqueadores de deploy e métricas que comprovam ASRs anteriores.
- Mini-lab: evoluir Jenkinsfile, instrumentar ao menos uma métrica, provocar uma condição observável e registrar evidência em Grafana/Prometheus.
- ADR, C4 Deployment ou Container com elementos de operação, e atualização final do C4 arquitetural.

## Comparação dos projetos fornecidos

| Aspecto | Camadas | Modular fornecido |
| --- | --- | --- |
| Java de produção | 37 arquivos | 41 arquivos, incluindo quatro package-info |
| Organização | controller, service, repository, domain, dto, config | usuario, curso, matricula, ranking e shared; subcamadas internas |
| Comportamento Java | Mesmo conteúdo após normalizar pacotes/imports | Mesmas 37 classes funcionais; quatro descritores adicionais |
| Runtime | Um processo Spring Boot e banco relacional | Mesmo runtime, sem escala/deploy por módulo |
| Build | Java 17, Spring Boot 3.5.5, Springdoc 2.8.11 | Dependências iguais; nome/artefato Maven distintos |
| Implantação | Dockerfile e Compose | Arquivos idênticos aos da versão em camadas |
| Persistência | JPA, PostgreSQL; perfil H2 | Mesmas configurações e entidades |
| Ranking | Quatro classes espalhadas nas camadas | Quatro classes agrupadas em ranking |
| Fronteiras | Dependências horizontais | Ranking consulta entidade Assinatura de usuario; MatriculaService acessa repositórios internos de usuario e curso |
| Proteção automática de módulos | Ausente | Ausente; package-info só documenta |
| Testes nos ZIPs | Ausentes | Ausentes |
| Compilação da base recebida | Compila; suíte acrescentada passou com 3 testes | Falha: Matricula não importa Usuario e Curso após mudança de pacote |

O Ranking calcula `100 * cursosConcluidosComSucesso + moedas`, com ordenação descendente na consulta JPA, `join fetch` de usuário e retorno de todos os resultados. Não há paginação, cache ou medição de carga fornecida. Empates não têm ordem secundária definida. O endpoint é `GET /api/ranking` em ambas as versões.

Não foram encontrados módulos próprios de badges/recompensas, IA, MQTT, Jenkinsfile ou configuração Prometheus/Grafana. Há regras de assinatura, créditos, moedas, promoção de plano e matrícula, mas isso não equivale a comprovar todo o RF02 do enunciado. A ausência de identificação da AC1 impede afirmar que o material reproduz integralmente o produto da equipe.

O domínio usa anotações JPA. O agrupamento modular ainda não prova independência de framework ou conclusão do Desafio 2. Também há risco de contabilização repetida: `MatriculaService.concluir` não verifica conclusão anterior antes de incrementar a assinatura. Esse ponto deve ser tratado ao desenhar idempotência no fluxo de conclusão/eventos, sem alterar silenciosamente o comportamento neste primeiro lab.

## Trabalho iniciado

Foi identificado um defeito no ZIP modular: `matricula/domain/Matricula.java` usa `Usuario` e `Curso` sem importar os novos pacotes. A comparação normalizada não captura essa falha, pois as classes conviviam no mesmo pacote na versão em camadas. Os dois imports foram acrescentados somente à cópia evoluída; o original foi preservado.

Foi copiado o projeto modular para `projeto/`, preservando os originais. O Ranking passou a depender exclusivamente do contrato público `usuario.api.ConsultaPontuacao`, que retorna registros imutáveis com dados de leitura, sem expor entidades JPA. A consulta e a ordenação existentes foram movidas para a persistência de Usuário; sua implementação mapeia os dados dentro da transação. Endpoint, DTO, fórmula e ordenação foram preservados.

Isso reduz o conhecimento direto do Ranking sobre persistência e domínio de outro módulo. Não elimina acoplamento lógico aos dados de Usuário, não cria escala independente e não resolve as dependências de Matrícula. A suíte com três testes passou tanto no baseline em camadas quanto na versão evoluída, com JPA/H2 e consulta HTTP via MockMvc. O modular original falhou antes dos testes, por falta de imports. Docker/PostgreSQL e carga de 100 mil usuários não foram validados. A medição estática e o teste de fronteira estão em `projeto/docs/evidencias/desafio1/` e `projeto/scripts/`.

O ADR-001 e a matriz de ASRs foram reescritos para distinguir restrições do enunciado, escolhas da base e decisões propostas. O C4 Container representa o Core como um único container; o C4 Component atual mostra domínio, porta e adapter do Desafio 2. O Desafio 2 foi implementado posteriormente, com ADR 002, domínio Java puro e contrato executado com adapters em memória e JPA. Os desafios 3 a 6 permanecem pendentes.

## Decisões que dependem do usuário

- A equipe foi confirmada como a mesma do A2 e está identificada no README. Falta definir o repositório remoto B1; turma/disciplina podem ser acrescentadas se exigidas.
- Usar os ZIPs do B1 como base imediata. O usuário esclareceu que fizemos o A2 juntos, não a AC1; só esclarecer a relação com a AC1 caso a professora exija outro repositório de origem.
- Revisar a proposta de monólito modular como direção inicial; a escolha foi usada para avançar localmente, sem publicação remota.
- Verificar a disponibilidade atual do ambiente já utilizado no A2: Docker, Jenkins e Prometheus/Grafana. As configurações e evidências anteriores foram localizadas; ver `CONTINUIDADE_A2_B1.md`. Não é necessário solicitar novamente a instalação dessas ferramentas como ponto de partida.
- Definir com a equipe metas de carga/latência, disponibilidade e critérios de revisão da extração de serviços. O enunciado não fornece esses números.
- Para IA, definir fonte de conhecimento, dados disponíveis, uso permitido de LLM e fallback aceitável. Para eventos/IoT, definir perda tolerada, janela de recuperação e identidade dos eventos.

Essas decisões não impedem a inspeção e o primeiro lab, mas afetam a integração com a AC1 e os laboratórios seguintes.

## Correção de contexto do trabalho anterior

O trabalho realizado anteriormente em conjunto foi o A2. Sua esteira e observabilidade servirão de referência para o Desafio 6, mediante adaptação e novas evidências do B1. Ver [continuidade A2 B1](CONTINUIDADE_A2_B1.md).

## Atualização da entrega parcial

A entrega atual inclui D1 e D2, com 14 testes aprovados. A fórmula de Ranking foi centralizada no domínio e a ordenação passou a ocorrer em memória; o adapter JPA preserva as fronteiras públicas de Usuário. Ver ADR 002 e evidências D2. O mock_spring recebido depois é material de apoio sem URL Git encontrada, conforme `fontes/LEITURA_MOCK_SPRING.md`.

## Atualização em 27 de outubro de 2026

A versão atual cobre seis mini labs. Os ADRs 003 a 006, evidências reais, C4 final e matriz cumulativa estão em docs/arquitetura/README.md. Os trechos anteriores deste arquivo preservam a inspeção inicial e não substituem esse registro atual. O Canvas confirmou que mock_spring é material de mocks/A3 e que o B1 usa os quatro anexos originais.

## Publicação final

Repositório privado criado com autorização do usuário: https://github.com/cervonizer/b1-architecture-lab. A entrega atual é o registro arquitetural cumulativo com os seis desafios. Solicitações antigas de definição de repositório neste arquivo são históricas.
