# Indisponibilidade da IA

Se o servico Python de inteligencia artificial ficar indisponivel, o Core usa fallback: devolve catalogo geral e informa que o assistente esta temporariamente indisponivel. Cursos, matriculas e Ranking continuam funcionando. A chamada externa tem timeout. O assistente com LLM possui um prazo maior que a recomendacao porque gerar texto leva mais tempo. As operacoes essenciais nao dependem da IA.
