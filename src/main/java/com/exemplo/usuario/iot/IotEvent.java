package com.exemplo.usuario.iot;
import jakarta.persistence.*;
@Entity
@Table(name="iot_inbox")
public class IotEvent {
    @Id private String id;
    @Column(nullable=false,length=4000)private String payload;
    protected IotEvent(){}
    public IotEvent(String id,String payload){this.id=id;this.payload=payload;}
    public String getId(){return id;}
    public String getPayload(){return payload;}
}
