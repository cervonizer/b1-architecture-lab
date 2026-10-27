package com.exemplo.usuario.ia;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
import java.util.*;

@Service
public class AiGateway {
    private final String baseUrl;
    private final ObjectMapper json;
    private final MeterRegistry metrics;
    private final HttpClient http = HttpClient.newBuilder().connectTimeout(Duration.ofMillis(300)).build();
    private final long timeoutMs;

    public AiGateway(@Value("${b1.ia.url:http://localhost:18081}") String baseUrl,
                     ObjectMapper json, MeterRegistry metrics,
                     @Value("${b1.ia.timeout-ms:600}") long timeoutMs) {
        this.baseUrl = baseUrl; this.json = json; this.metrics = metrics; this.timeoutMs = timeoutMs;
    }

    public Map<String, Object> consultar(String path, Map<String, Object> payload) {
        try {
            var builder = HttpRequest.newBuilder(URI.create(baseUrl + path)).timeout(Duration.ofMillis(timeoutMs));
            if (payload == null) builder.GET();
            else builder.header("Content-Type", "application/json").POST(HttpRequest.BodyPublishers.ofString(json.writeValueAsString(payload)));
            var resposta = http.send(builder.build(), HttpResponse.BodyHandlers.ofString());
            if (resposta.statusCode() != 200) throw new IllegalStateException("HTTP da IA: " + resposta.statusCode());
            @SuppressWarnings("unchecked") Map<String, Object> dados = json.readValue(resposta.body(), Map.class);
            metrics.counter("b1.ia.calls", "outcome", "success").increment();
            return dados;
        } catch (Exception ex) {
            if (ex instanceof InterruptedException) Thread.currentThread().interrupt();
            metrics.counter("b1.ia.calls", "outcome", "fallback").increment();
            return Map.of("fonte", "fallback-estatico", "degradado", true,
                    "cursos", List.of("Catálogo geral disponível no Core"),
                    "resposta", "Assistente temporariamente indisponível. Consulte os cursos e materiais cadastrados.");
        }
    }
}
