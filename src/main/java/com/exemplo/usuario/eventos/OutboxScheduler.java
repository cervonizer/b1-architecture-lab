package com.exemplo.usuario.eventos;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
@Component
public class OutboxScheduler {
    private final OutboxDispatcher dispatcher;
    @Value("${b1.eventos.agendador:true}") private boolean ativo;
    public OutboxScheduler(OutboxDispatcher dispatcher){this.dispatcher=dispatcher;}
    @Scheduled(fixedDelayString="${b1.eventos.intervalo-ms:2000}")
    public void executar(){if(ativo)dispatcher.despachar();}
}
