# Notificacoes e eventos

Uma falha ou indisponibilidade de notificacao nao impede a conclusao do curso. A conclusao grava o evento na outbox, na mesma transacao do estado e dos creditos, e retorna sucesso. Um dispatcher tenta entregar a notificacao posteriormente. Se o consumidor estiver fora, o evento permanece pendente para nova tentativa. O consumidor deduplica pelo event_id para nao repetir a notificacao.
