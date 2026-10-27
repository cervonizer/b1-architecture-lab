package com.exemplo.usuario.eventos;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.Map;
@Service
public class OutboxDispatcher {
    private final OutboxRepository repository;
    private final NotificationClient notificacoes;
    private final ObjectMapper json;
    private final MeterRegistry metrics;

    public OutboxDispatcher(OutboxRepository repository,NotificationClient notificacoes,ObjectMapper json,MeterRegistry metrics){
        this.repository=repository;this.notificacoes=notificacoes;this.json=json;this.metrics=metrics;
        Gauge.builder("b1.outbox.pending",repository,r->r.countByEntregueFalse()).register(metrics);
    }
    // Participa da MESMA transacao da conclusao; nenhum HTTP neste metodo.
    public void registrarConclusao(Long matriculaId,Long usuarioId){
        try {
            String id="conclusao-"+matriculaId;
            repository.save(new EventoPendente(id,json.writeValueAsString(Map.of(
                "event_id",id,"tipo","CURSO_CONCLUIDO","matricula_id",matriculaId,"usuario_id",usuarioId))));
        }catch(com.fasterxml.jackson.core.JsonProcessingException e){throw new IllegalStateException(e);}
    }
    @Transactional
    public synchronized int despachar(){
        int entregues=0;
        for(var evento:repository.findTop20ByEntregueFalseOrderByCriadoEmAsc()){
            boolean ok=notificacoes.enviar(evento.getPayload());
            evento.registrarTentativa(ok);
            repository.save(evento);
            metrics.counter("b1.outbox.attempts","outcome",ok?"delivered":"failed").increment();
            if(ok)entregues++;
        }
        return entregues;
    }
}
