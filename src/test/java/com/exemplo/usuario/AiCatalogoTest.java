package com.exemplo.usuario;

import com.exemplo.usuario.curso.domain.Curso;
import com.exemplo.usuario.curso.internal.persistence.CursoRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
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
import java.util.concurrent.atomic.AtomicReference;
import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest(properties="b1.eventos.agendador=false")
@AutoConfigureMockMvc
@ActiveProfiles("h2")
@Transactional
class AiCatalogoTest {
    static final AtomicInteger chamadas=new AtomicInteger();
    static final AtomicReference<String> corpo=new AtomicReference<>();
    static final AtomicReference<String> metodo=new AtomicReference<>();
    static final HttpServer python;
    static {try{
        python=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
        python.createContext("/recomendacoes",e->{
            chamadas.incrementAndGet();metodo.set(e.getRequestMethod());corpo.set(new String(e.getRequestBody().readAllBytes(),java.nio.charset.StandardCharsets.UTF_8));
            byte[] resposta="{\"fonte\":\"modelo-supervisionado\",\"degradado\":false,\"cursos\":[]}".getBytes();
            e.sendResponseHeaders(200,resposta.length);e.getResponseBody().write(resposta);e.close();
        });python.start();
    }catch(Exception e){throw new ExceptionInInitializerError(e);}}
    @DynamicPropertySource static void configurar(DynamicPropertyRegistry r){r.add("b1.ia.url",()->"http://127.0.0.1:"+python.getAddress().getPort());}
    @AfterAll static void fechar(){python.stop(0);}
    @BeforeEach void limpar(){chamadas.set(0);}
    @Autowired MockMvc http;
    @Autowired CursoRepository cursos;
    @Autowired ObjectMapper json;
    @Test void enviaPerfilECatalogoCadastradoAoPython()throws Exception{
        var curso=cursos.saveAndFlush(new Curso("Arquitetura Java","Java e modularidade"));
        http.perform(get("/api/ia/recomendacoes").param("interesses","java,arquitetura").param("nivel","2")
            .header("Authorization","Basic YWRtaW46MTIzNDU2")).andExpect(status().isOk()).andExpect(jsonPath("$.degradado").value(false));
        var payload=json.readTree(corpo.get());
        assertThat(metodo.get()).isEqualTo("POST");
        assertThat(payload.get("nivel").asInt()).isEqualTo(2);
        assertThat(payload.get("interesses").get(0).asText()).isEqualTo("java");
        assertThat(payload.get("cursos").get(0).get("id").asLong()).isEqualTo(curso.getId());
        assertThat(payload.get("cursos").get(0).get("titulo").asText()).isEqualTo("Arquitetura Java");
    }
    @Test void rejeitaNivelInvalidoAntesDeChamarIA()throws Exception{
        http.perform(get("/api/ia/recomendacoes").param("nivel","0").header("Authorization","Basic YWRtaW46MTIzNDU2"))
            .andExpect(status().isBadRequest());
        assertThat(chamadas.get()).isZero();
    }
}
