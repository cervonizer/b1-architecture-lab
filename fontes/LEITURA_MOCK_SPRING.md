# Inspeção do mock spring

O ZIP contém um projeto Spring Boot 3.3.3 com Java 17, JaCoCo 0.8.12, Jogo, Juiz, Participante, FinalizaJogo, JogoDao e JogoDaoFalso. Os testes usam Mockito para substituir a classe concreta JogoDao. O DAO real usa JDBC/MySQL, não JPA. FinalizaJogo depende da classe concreta, e o DAO falso não implementa uma interface comum com ela.

Não foram encontrados diretório Git, URL SCM preenchida ou endereço de GitHub. O artefato Maven é `br.com.valueprojects:teste-na-pratica_spring`. Não há cursos, matrículas nem a regra de 100 pontos por curso do B1. Trata-se de material de apoio para estudar testes e persistência, sem evidência suficiente para identificá-lo como o repositório de entrega do B1. Não foi executada sua suíte nem alterado seu código.

O laboratório D2 implementa a inversão por uma interface explícita e a troca entre fonte em memória e JPA na base do B1, reaproveitando a ideia de substituir infraestrutura por um test double.

O ZIP original foi preservado no material recebido e na entrega parcial anterior. Seu SHA256 e 9a5a10519b805a01ee86c4336919b271f38ff9eae636abfd651016158830c127. Ele nao e necessario para executar o B1 e nao integra o pacote final.
