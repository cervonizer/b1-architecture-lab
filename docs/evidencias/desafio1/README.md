# Evidências do Desafio 1

Este registro preserva o mini lab inicial do Desafio 1. O código atual acrescenta a evolução do Desafio 2, descrita em `../desafio2/README.md`. O C4 e a matriz atuais estão no registro arquitetural cumulativo. As fontes e o baseline ficam na raiz do projeto.

## Hipótese

Agrupar classes por capacidade e substituir o acesso do Ranking a uma entidade de outro módulo por um contrato público torna a fronteira explícita, preservando comportamento. Só mover pastas não prova que as dependências foram protegidas.

## Resultados observados em 26 de outubro de 2026

| Verificação | Resultado | Arquivo |
| --- | --- | --- |
| Modular fornecido, código de produção intacto | Falha de compilação por ausência de imports de Usuario e Curso em Matricula; testes não iniciados | compilacao-modular-original.log |
| Camadas, com suíte de caracterização acrescentada | 3 testes, 0 falhas, 0 erros | test-camadas.log |
| Modular evoluído, imports corrigidos e fronteira alterada | 3 testes, 0 falhas, 0 erros | test-projeto.log e XML Surefire |
| Ranking só usa api pública de outros módulos | Verificação passou | fronteira.log |
| Imports de Ranking para domínio/persistência de outro módulo | 1 no modular recebido, 0 no evoluído | dependencias.json e dependencias.md |

Os testes foram executados com Temurin JDK 17.0.20.1, Maven 3.9.16 e perfil H2. A primeira tentativa de execução restrita falhou por limitações do ambiente de testes; o resultado acima corresponde às execuções finais concluídas. As dependências foram baixadas para a pasta de trabalho, sem alterar versões do pom.xml.

Os três testes verificam: fórmula e ordenação com dois usuários (250 e 207 pontos); lista vazia; `GET /api/ranking` autenticado retornando os campos esperados. A suíte usa Spring, JPA/H2 e MockMvc. No projeto em camadas, apenas os imports da suíte foram adaptados aos pacotes originais; seu código de produção não foi alterado.

Não se afirma que o ZIP modular original passou em testes: ele não compilava. A evidência de comportamento compara a base em camadas com a versão modular corrigida e evoluída.

## Reproduzir

Dentro de `projeto/`, com JDK 17 e Maven:

```sh
mvn test
python3 scripts/verificar_fronteira.py
python3 scripts/comparar_dependencias.py
```

O último comando usa os ZIPs preservados em `fontes/` e imprime o inventário JSON. Execute o script de fronteira contra a versão evoluída; ele retorna erro se uma referência do Ranking acessar outro módulo fora de `api`. É uma análise textual, sem proteção geral por bytecode.

Para reproduzir o teste de comparação no baseline, copie `RankingIntegrationTest-camadas.java.txt` como `baseline-camadas/src/test/java/com/exemplo/usuario/RankingIntegrationTest.java` e execute `mvn test` naquela pasta. Os ZIPs originais continuam sem testes; a suíte é uma adição deste trabalho.

`alteracoes.patch` registra as mudanças no Java de produção relativamente ao modular original, incluindo a correção dos imports de Matrícula. Os testes e documentos novos estão diretamente no projeto editável.

## O que a evidência sustenta

A fatia Ranking deixa de conhecer entidades e repositórios de Usuário diretamente. Endpoint, cálculo, campos e ordem descendente são preservados nos casos testados. A quantidade de dependências intermodulares continua uma; houve substituição da dependência, não eliminação do vínculo entre capacidades.

## Limites

Não houve execução de Docker/PostgreSQL, ensaio de 100 mil usuários, benchmark de latência ou teste de concorrência. H2 não valida todas as particularidades do PostgreSQL. Empates e paginação seguem sem política adicional. As dependências cruzadas de Matrícula continuam. A troca de adapter do Desafio 2 foi realizada depois deste registro; consulte as evidências próprias desse desafio. A equipe confirmou que usará as bases anexadas para avançar. A publicação remota depende de definir o repositório B1; os resultados deste mini lab não comprovam desempenho sob carga.
