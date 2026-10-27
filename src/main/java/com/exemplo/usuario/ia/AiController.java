package com.exemplo.usuario.ia;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
@RestController
@RequestMapping("/api/ia")
public class AiController {
    private final AiGateway gateway;
    public AiController(AiGateway gateway) { this.gateway = gateway; }
    @GetMapping("/recomendacoes") public Map<String,Object> recomendar() { return gateway.consultar("/recomendacoes", null); }
    @PostMapping("/assistente") public Map<String,Object> perguntar(@RequestBody Map<String,Object> pergunta) {
        return gateway.consultar("/assistente", pergunta);
    }
}
