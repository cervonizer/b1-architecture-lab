package com.exemplo.usuario;

import com.exemplo.usuario.fake.ParticipantesEmMemoria;
import com.exemplo.usuario.ranking.application.RankingService;
import com.exemplo.usuario.ranking.application.port.CarregarParticipantes;
import com.exemplo.usuario.ranking.domain.ParticipanteRanking;
import com.exemplo.usuario.ranking.internal.persistence.JpaParticipantesAdapter;
import com.exemplo.usuario.usuario.domain.Assinatura;
import com.exemplo.usuario.usuario.domain.Usuario;
import com.exemplo.usuario.usuario.internal.persistence.UsuarioRepository;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(properties="b1.eventos.agendador=false")
@AutoConfigureMockMvc
@ActiveProfiles("h2")
@Transactional
class RankingAdaptersTest {
    enum Adapter { MEMORIA, JPA }
    @Autowired JpaParticipantesAdapter jpa;
    @Autowired UsuarioRepository usuarios;

    private Long criar(String nome, int cursos, int moedas) {
        var usuario = new Usuario(nome, nome.toLowerCase() + "@example.com", "senha-cifrada");
        var assinatura = new Assinatura(usuario);
        assinatura.setCursosConcluidosComSucesso(cursos);
        assinatura.setMoedas(moedas);
        usuario.vincularAssinatura(assinatura);
        return usuarios.saveAndFlush(usuario).getId();
    }

    @ParameterizedTest(name = "Mesma regra com adapter {0}")
    @EnumSource(Adapter.class)
    void trocaAdapterMantendoCasoDeUsoEResultados(Adapter tipo) {
        Long anaId = criar("Ana", 2, 7);
        Long biaId = criar("Bia", 1, 150);
        // Mesmos dados, entrada fora da ordem de pontuacao no fake.
        CarregarParticipantes fonte = tipo == Adapter.JPA ? jpa : new ParticipantesEmMemoria(List.of(
                new ParticipanteRanking(anaId, "Ana", 2, 7),
                new ParticipanteRanking(biaId, "Bia", 1, 150)));
        var resultado = new RankingService(fonte).listar();
        assertThat(resultado).extracting(r -> r.getUsuarioId()).containsExactly(biaId, anaId);
        assertThat(resultado).extracting(r -> r.getNome()).containsExactly("Bia", "Ana");
        assertThat(resultado).extracting(r -> r.getPontos()).containsExactly(250, 207);
        assertThat(resultado).extracting(r -> r.getCursosConcluidos()).containsExactly(1, 2);
        assertThat(resultado).extracting(r -> r.getMoedas()).containsExactly(150, 7);
    }

    @ParameterizedTest(name = "Ranking vazio com adapter {0}")
    @EnumSource(Adapter.class)
    void trocaAdapterMantendoResultadoVazio(Adapter tipo) {
        CarregarParticipantes fonte = tipo == Adapter.JPA ? jpa : new ParticipantesEmMemoria(List.of());
        assertThat(new RankingService(fonte).listar()).isEmpty();
    }
}
