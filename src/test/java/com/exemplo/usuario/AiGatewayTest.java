package com.exemplo.usuario;
import com.exemplo.usuario.ia.AiGateway;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.Test;
import java.net.InetSocketAddress;
import static org.assertj.core.api.Assertions.assertThat;

class AiGatewayTest {
    @Test void usaRespostaPythonQuandoDisponivel() throws Exception {
        var servidor=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
        servidor.createContext("/recomendacoes",e->{byte[] body="{\"degradado\":false,\"fonte\":\"python-simulacao\"}".getBytes();e.sendResponseHeaders(200,body.length);e.getResponseBody().write(body);e.close();});
        servidor.start();
        try {
            var gateway=new AiGateway("http://127.0.0.1:"+servidor.getAddress().getPort(),new ObjectMapper(),new SimpleMeterRegistry(),600);
            assertThat(gateway.consultar("/recomendacoes",null)).containsEntry("degradado",false);
        }finally{servidor.stop(0);}
    }
    @Test void falhaDeConexaoAtivaFallbackEMetrica() throws Exception {
        var socket=new java.net.ServerSocket(0);int porta=socket.getLocalPort();socket.close();
        var metrics=new SimpleMeterRegistry();
        var gateway=new AiGateway("http://127.0.0.1:"+porta,new ObjectMapper(),metrics,200);
        assertThat(gateway.consultar("/recomendacoes",null)).containsEntry("degradado",true);
        assertThat(metrics.counter("b1.ia.calls","outcome","fallback").count()).isEqualTo(1);
    }
    @Test void erroHttpTambemAtivaFallback() throws Exception {
        var servidor=HttpServer.create(new InetSocketAddress("127.0.0.1",0),0);
        servidor.createContext("/recomendacoes",e->{e.sendResponseHeaders(503,-1);e.close();});servidor.start();
        try {
            var gateway=new AiGateway("http://127.0.0.1:"+servidor.getAddress().getPort(),new ObjectMapper(),new SimpleMeterRegistry(),600);
            assertThat(gateway.consultar("/recomendacoes",null)).containsEntry("degradado",true);
        }finally{servidor.stop(0);}
    }
}
