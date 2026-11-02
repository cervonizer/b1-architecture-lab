# Dados do laboratorio de recomendacao

Os 18 perfis e os 15 cursos sao ficticios, criados para demonstracao academica. O CSV contem 270 pares perfil curso com rotulos binarios de relevancia escolhidos para cada perfil. Nao sao historicos de alunos reais nem dados de producao.

Os rotulos positivos foram definidos na preparacao do conjunto, e nao pelo classificador. O treinamento separa perfis inteiros entre treino e teste para evitar que linhas do mesmo perfil aparecam nos dois grupos. As metricas descrevem apenas este conjunto sintetico pequeno.

Em execucao via Core, o modelo pontua o catalogo realmente cadastrado em Java, recebido no corpo HTTP. O catalogo ficticio e usado somente no treinamento, na avaliacao e na chamada direta de demonstracao ao servico Python.
