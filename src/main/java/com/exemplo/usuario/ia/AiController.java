package com.exemplo.usuario.ia;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;
import com.exemplo.usuario.curso.application.CursoService;
import java.util.*;
@RestController
@RequestMapping("/api/ia")
public class AiController {
    private final AiGateway gateway;
    private final CursoService cursos;
    public AiController(AiGateway gateway,CursoService cursos){this.gateway=gateway;this.cursos=cursos;}
    @GetMapping("/recomendacoes")
    public Map<String,Object> recomendar(@RequestParam(defaultValue="java,arquitetura") String interesses,
                                         @RequestParam(defaultValue="1") int nivel){
        if(nivel<1||nivel>3||interesses.isBlank()||interesses.length()>500)
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Perfil invalido");
        var catalogo=cursos.listarTodos().stream().map(c->Map.<String,Object>of(
            "id",c.getId(),"titulo",c.getTitulo(),"descricao",c.getDescricao()==null?"":c.getDescricao())).toList();
        return gateway.consultar("/recomendacoes",Map.of("interesses",Arrays.asList(interesses.split(",")),"nivel",nivel,"cursos",catalogo));
    }
    @PostMapping("/assistente")
    public Map<String,Object> perguntar(@RequestBody Map<String,Object> pergunta){return gateway.consultar("/assistente",pergunta);}
    @GetMapping("/status")
    public Map<String,Object> status(){return gateway.consultar("/health",null);}
}
