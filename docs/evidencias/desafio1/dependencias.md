# Dependências observadas no Ranking

A contagem considera imports explícitos de classes do projeto nas classes de produção do Ranking. Não é contagem de chamadas, objetos ou custo de manutenção. Na versão em camadas não há módulos de negócio declarados, por isso a métrica intermodular é aplicada somente às duas variantes modulares.

| Medida | Modular recebido | Modular evoluído |
| --- | ---: | ---: |
| Imports do Ranking para fora de sua capacidade | 1 | 1 |
| Imports externos que expõem domínio/persistência | 1 | 0 |
| Imports externos via contrato público api | 0 | 1 |

O número total de ligações externas não caiu. Mudou o tipo de dependência: `RankingRepository → usuario.domain.Assinatura` foi substituído por `RankingService → usuario.api.ConsultaPontuacao`. `PontuacaoRepository` agora pertence ao módulo Usuário. A dependência dos dados permanece; o contrato deixa de expor entidade JPA.

Antes em camadas: `controller/RankingRestController → service/RankingService → repository/RankingRepository → domain/Assinatura`.

Modular fornecido: `ranking.api → ranking.application → ranking.internal.persistence → usuario.domain.Assinatura`.

Modular evoluído: `ranking.api → ranking.application → usuario.api.ConsultaPontuacao ← usuario.application.ConsultaPontuacaoService → usuario.internal.persistence.PontuacaoRepository → usuario.domain.Assinatura`.

A seta para a interface indica implementação pelo serviço de Usuário. Em execução, a injeção do Spring conecta Ranking à implementação local; não há HTTP entre módulos.

O script `scripts/verificar_fronteira.py` detecta referências de Ranking a pacotes externos que não sejam `api`. É uma verificação textual limitada a essa fatia; reflexão e outros módulos não são cobertos. `dependencias.json` lista todos os imports usados na medição.
