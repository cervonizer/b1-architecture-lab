package com.exemplo.usuario.iot;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.MeterRegistry;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import java.util.Map;
@RestController
@RequestMapping("/api/iot/eventos")
public class IotController {
    public record Evento(@NotBlank @Size(max=100) String eventId,
                         @NotBlank @Size(max=100) String deviceId,
                         @NotBlank @Size(max=100) String institutionId,
                         @NotNull @Positive Long usuarioId,
                         @NotBlank @Pattern(regexp="PRESENCA|INICIO|CONCLUSAO") String tipo){}
    private final IotRepository repo;private final ObjectMapper json;private final MeterRegistry metrics;
    public IotController(IotRepository repo,ObjectMapper json,MeterRegistry metrics){this.repo=repo;this.json=json;this.metrics=metrics;}
    @PostMapping
    public synchronized Map<String,Object> receber(@Valid @RequestBody Evento evento)throws Exception{
        String payload=json.writeValueAsString(evento);
        var existente=repo.findById(evento.eventId());
        boolean duplicate=existente.isPresent();
        if(!duplicate){
            try{repo.saveAndFlush(new IotEvent(evento.eventId(),payload));}
            catch(DataIntegrityViolationException e){existente=repo.findById(evento.eventId());if(existente.isEmpty())throw e;duplicate=true;}
        }
        if(duplicate && !existente.orElseThrow().getPayload().equals(payload))
            throw new ResponseStatusException(HttpStatus.CONFLICT,"eventId reutilizado com conteudo diferente");
        metrics.counter("b1.iot.received","outcome",duplicate?"duplicate":"accepted").increment();
        return Map.of("eventId",evento.eventId(),"duplicado",duplicate,"aceito",true);
    }
    @GetMapping public Map<String,Object> contar(){return Map.of("eventos",repo.count());}
}
