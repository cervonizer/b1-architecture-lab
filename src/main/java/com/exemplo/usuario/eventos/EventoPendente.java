package com.exemplo.usuario.eventos;
import jakarta.persistence.*;
import java.time.Instant;
@Entity
@Table(name="outbox_eventos")
public class EventoPendente {
    @Id private String id;
    @Column(nullable=false, length=4000) private String payload;
    private boolean entregue;
    private int tentativas;
    private Instant criadoEm;
    protected EventoPendente() {}
    public EventoPendente(String id, String payload) { this.id=id; this.payload=payload; this.criadoEm=Instant.now(); }
    public String getId(){return id;}
    public String getPayload(){return payload;}
    public boolean isEntregue(){return entregue;}
    public int getTentativas(){return tentativas;}
    public void registrarTentativa(boolean sucesso){tentativas++; if(sucesso) entregue=true;}
}
