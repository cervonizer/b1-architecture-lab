# Evidências do Desafio 2

## Hipótese e alteração

A regra do Ranking deve ser aplicada a qualquer fonte de dados sem depender de Spring/JPA ou da API de Usuário no domínio. A troca da fonte deve manter cálculo, ordenação, campos e endpoint. O ADR 002 e o C4 Component explicitam as responsabilidades.

Antes: aplicação conhece a API de Usuário, calcula pontos e delega ordenação a SQL com a mesma fórmula.

Depois: `RankingService → CarregarParticipantes`; `JpaParticipantesAdapter` e `ParticipantesEmMemoria` implementam a porta. O domínio calcula e ordena. O adapter JPA usa a API pública de Usuário, preservando o encapsulamento das entidades.

## Execuções de 26 de outubro de 2026

Ambiente: Temurin JDK 17.0.20.1, Maven 3.9.16, Spring Boot 3.5.5 e H2 no perfil de integração. Não houve mudança de dependências no pom.xml.

| Teste | Casos | Evidência |
| --- | ---: | --- |
| RankingDomainTest | 6 | Fórmula em quatro combinações, ordenação sem alterar entrada e lista vazia |
| RankingArchitectureTest | 1 | Imports do domínio limitados a Java e ao próprio domínio; sem anotações de framework |
| RankingAdaptersTest | 4 | Mesmo contrato para MEMORIA e JPA com lista preenchida e vazia |
| RankingIntegrationTest | 3 | Preserva fórmula/ordem/dados, lista vazia e GET autenticado |
| Total | 14 | Zero falhas, zero erros e zero ignorados |

`dominio-isolado.log` registra execução somente dos sete testes de domínio/arquitetura, sem subir contexto Spring nem banco. `suite-completa.log` registra os 14 testes. Os XMLs Surefire contêm resultados por classe. `fronteira.log` registra a verificação textual de acesso a outros módulos.

## Troca efetiva de adapter

`RankingAdaptersTest` instancia o mesmo `RankingService` passando alternativamente uma instância `ParticipantesEmMemoria` e o bean real `JpaParticipantesAdapter`. O serviço e o domínio não mudam entre execuções. O adapter JPA percorre a API de Usuário, serviço transacional e repositório Spring Data contra H2; não é um mock de repositório.

Para entradas Ana com 2 cursos e 7 moedas e Bia com 1 curso e 150 moedas, ambos os adapters devem retornar Bia com 250 pontos e Ana com 207, preservando também IDs, nome, cursos e moedas. O fake recebe a lista fora da ordem de pontuação para demonstrar que a ordenação é regra comum do domínio. Ambos devem retornar lista vazia sem participantes.

## Reproduzir

Na raiz do projeto, com Java 17:

```sh
mvn -Dtest=RankingDomainTest,RankingArchitectureTest test
mvn -Dtest=RankingAdaptersTest test
mvn test
python3 scripts/verificar_fronteira.py
```

Não exige MySQL, Docker ou alteração do projeto `mock_spring`. A aplicação usa JPA por padrão; o fake só existe nos testes e não cria perfil de produção alternativo.

## Limites e trade offs

A guarda de arquitetura examina imports/anotações, não bytecode/reflexão. O domínio é isolado nessa fatia; outros módulos continuam com JPA e dependências cruzadas. A ordenação mudou do banco para memória e não foi testada sob carga. H2 não substitui validação específica do PostgreSQL. A troca não comprova independência de implantação nem implementação completa de DDD/Clean/Onion.

O exemplo `mock_spring.zip` mostra testes Mockito e um DAO falso em outro domínio; ele foi inspecionado como referência. Não foi adotado como base do Core nem apresentado como evidência de execução deste laboratório.
