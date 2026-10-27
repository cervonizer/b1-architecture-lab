package com.exemplo.usuario.eventos;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;
@RestController
@RequestMapping("/api/lab/eventos")
public class EventosController {
    private final OutboxRepository repo;private final OutboxDispatcher dispatcher;private final NotificationClient client;private final ObjectMapper json;
    public EventosController(OutboxRepository repo,OutboxDispatcher dispatcher,NotificationClient client,ObjectMapper json){
        this.repo=repo;this.dispatcher=dispatcher;this.client=client;this.json=json;
    }
    @GetMapping("/pendentes") public Map<String,Object> pendentes(){return Map.of("pendentes",repo.countByEntregueFalse());}
    @PostMapping("/despachar") public Map<String,Object> despachar(){return Map.of("entregues",dispatcher.despachar());}
    @PostMapping("/sincrono") public Map<String,Object> sincrono(@RequestBody Map<String,Object> payload)throws Exception{
        if(!client.enviar(json.writeValueAsString(payload)))throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Consumidor indisponivel");
        return Map.of("entregue",true);
    }
}
