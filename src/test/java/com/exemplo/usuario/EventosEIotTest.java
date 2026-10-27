package com.exemplo.usuario;
import com.exemplo.usuario.eventos.*;
import com.exemplo.usuario.matricula.application.MatriculaService;
import com.exemplo.usuario.usuario.domain.*;
import com.exemplo.usuario.usuario.internal.persistence.UsuarioRepository;
import com.exemplo.usuario.curso.domain.Curso;
import com.exemplo.usuario.curso.internal.persistence.CursoRepository;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.test.web.servlet.MockMvc;
import java.net.InetSocketAddress;
import java.util.concurrent.atomic.AtomicInteger;
import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties="b1.eventos.agendador=false")
@AutoConfigureMockMvc
@org.springframework.boot.test.autoconfigure.actuate.observability.AutoConfigureObservability
@ActiveProfiles("h2")
@Transactional
class EventosEIotTest {
    static final AtomicInteger status=new AtomicInteger(503);
    static final HttpServer consumidor;
    static {try {
        consumidor=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
        consumidor.createContext("/notificacoes",e->{e.getRequestBody().readAllBytes();e.sendResponseHeaders(status.get(),-1);e.close();});consumidor.start();
    }catch(Exception e){throw new ExceptionInInitializerError(e);}}
    @DynamicPropertySource static void configurar(DynamicPropertyRegistry r){
        r.add("b1.notificacao.url",()->"http://127.0.0.1:"+consumidor.getAddress().getPort()+"/notificacoes");
    }
    @AfterAll static void fechar(){consumidor.stop(0);}
    @Autowired MatriculaService matriculas;
    @Autowired UsuarioRepository usuarios;
    @Autowired CursoRepository cursos;
    @Autowired OutboxRepository outbox;
    @Autowired OutboxDispatcher dispatcher;
    @Autowired MockMvc http;
    static final String AUTH="Basic YWRtaW46MTIzNDU2";
    @BeforeEach void falhar(){status.set(503);}
    @Test void conclusaoNaoDependeDoConsumidorERepeticaoNaoDuplicaCredito(){
        var usuario=new Usuario("Aluno","eventos@example.com","senha-cifrada");usuario.vincularAssinatura(new Assinatura(usuario));usuarios.saveAndFlush(usuario);
        var curso=cursos.saveAndFlush(new Curso("Curso","Descricao"));
        var matricula=matriculas.matricular(usuario.getId(),curso.getId(),false);
        matriculas.concluir(matricula.getId(),8.0);matriculas.concluir(matricula.getId(),8.0);
        assertThat(usuario.getAssinatura().getCreditosCursos()).isEqualTo(3);
        assertThat(usuario.getAssinatura().getCursosConcluidosComSucesso()).isEqualTo(1);
        assertThat(outbox.countByEntregueFalse()).isEqualTo(1);
    }
    @Test void eventoPendenteSobreviveAFalhaERecuperaDepois(){
        outbox.saveAndFlush(new EventoPendente("teste-retry","{\"event_id\":\"teste-retry\",\"tipo\":\"CURSO_CONCLUIDO\"}"));
        assertThat(dispatcher.despachar()).isZero();
        assertThat(outbox.findById("teste-retry").orElseThrow().getTentativas()).isEqualTo(1);
        assertThat(outbox.countByEntregueFalse()).isEqualTo(1);
        status.set(200);
        assertThat(dispatcher.despachar()).isEqualTo(1);
        assertThat(outbox.countByEntregueFalse()).isZero();
    }
    @Test void interacaoSincronaPropagaIndisponibilidade()throws Exception{
        http.perform(post("/api/lab/eventos/sincrono").header("Authorization",AUTH).contentType("application/json").content("{\"event_id\":\"sincrono\",\"tipo\":\"TESTE\"}"))
            .andExpect(status().isServiceUnavailable());
    }
    @Test void iotDeduplicaERejeitaConflito()throws Exception{
        String body="{\"eventId\":\"iot-1\",\"deviceId\":\"device-1\",\"institutionId\":\"inst-1\",\"usuarioId\":1,\"tipo\":\"CONCLUSAO\"}";
        http.perform(post("/api/iot/eventos").header("Authorization",AUTH).contentType("application/json").content(body)).andExpect(status().isOk()).andExpect(jsonPath("$.duplicado").value(false));
        http.perform(post("/api/iot/eventos").header("Authorization",AUTH).contentType("application/json").content(body)).andExpect(status().isOk()).andExpect(jsonPath("$.duplicado").value(true));
        http.perform(post("/api/iot/eventos").header("Authorization",AUTH).contentType("application/json").content(body.replace("CONCLUSAO","PRESENCA"))).andExpect(status().isConflict());
    }
    @Test void metricasProtegidasDisponiveisParaColetor()throws Exception{
        http.perform(get("/actuator/prometheus")).andExpect(status().isUnauthorized());
        http.perform(get("/actuator/prometheus").header("Authorization",AUTH)).andExpect(status().isOk());
    }
}
