package com.exemplo.usuario;

import org.junit.jupiter.api.Test;
import java.nio.file.Files;
import java.nio.file.Path;
import static org.assertj.core.api.Assertions.assertThat;

class RankingArchitectureTest {
    @Test void dominioSoDependeDeJavaEDoProprioDominio() throws Exception {
        Path pasta = Path.of("src/main/java/com/exemplo/usuario/ranking/domain");
        try (var arquivos = Files.walk(pasta)) {
            for (var arquivo : arquivos.filter(p -> p.toString().endsWith(".java")).toList()) {
                var texto = Files.readString(arquivo);
                assertThat(texto).doesNotContain("@Entity", "@Service", "@Component", "@Autowired");
                for (var linha : texto.lines().filter(l -> l.startsWith("import ")).toList()) {
                    assertThat(linha.startsWith("import java.") ||
                            linha.startsWith("import com.exemplo.usuario.ranking.domain."))
                        .as("Dependencia indevida em %s: %s", arquivo, linha).isTrue();
                }
            }
        }
    }
}
