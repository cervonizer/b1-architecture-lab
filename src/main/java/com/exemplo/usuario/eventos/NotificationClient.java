package com.exemplo.usuario.eventos;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
@Component
public class NotificationClient {
    private final String url;
    private final HttpClient http=HttpClient.newBuilder().connectTimeout(Duration.ofMillis(300)).build();
    public NotificationClient(@Value("${b1.notificacao.url:http://localhost:18081/notificacoes}") String url){this.url=url;}
    public boolean enviar(String payload){
        try {
            var request=HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofMillis(600))
                .header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(payload)).build();
            return http.send(request,HttpResponse.BodyHandlers.discarding()).statusCode()/100==2;
        } catch(Exception e){if(e instanceof InterruptedException)Thread.currentThread().interrupt();return false;}
    }
}
