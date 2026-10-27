# B1 – Desafio 1 – Versão A: Monólito em Camadas

## Objetivo
Evoluir a aplicação-base sem trocar a arquitetura macro. O novo RF de **Ranking** foi acrescentado mantendo a separação horizontal `controller -> service -> repository -> domain`.

## Decisão do Tech Lead
**RF:** consultar ranking de usuários.  
**RNFs:** desempenho sob crescimento de carga; manutenibilidade; simplicidade operacional.  
**ASRs:** ranking pode crescer mais que os demais casos de uso; equipe ainda pequena; banco e deploy únicos reduzem custo operacional.  
**RPCs:** Java 17, Spring Boot, PostgreSQL, Docker; manter compatibilidade dos endpoints existentes.  
**Alternativas:** monólito em camadas, monólito modular, serviço independente.  
**Decisão/ADR:** nesta versão, manter o monólito em camadas como baseline de comparação.  
**Trade-off:** menor custo operacional e maior simplicidade, porém acoplamento estrutural e escala do processo inteiro.

## C4 – Container (texto)
Usuário -> API Spring Boot (Controllers/Services/Repositories/Domain + Ranking) -> PostgreSQL. O pgAdmin é apenas ferramenta de administração.

## Evidência prática
Novo endpoint `GET /api/ranking` (HTTP Basic admin/123456). Pontuação didática = `100 * cursos concluídos + moedas`.

## Como executar
`docker compose up --build`

Acesse Swagger em `http://localhost:8080/swagger-ui/index.html`.

## O que observar
O Ranking ganhou Controller, Service, Repository e DTO em pastas horizontais. Para localizar tudo que pertence ao Ranking, é necessário navegar por várias camadas. Essa característica será comparada com a versão modular.
