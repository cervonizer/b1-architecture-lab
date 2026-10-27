package com.exemplo.usuario;

import com.exemplo.usuario.ranking.domain.ParticipanteRanking;
import com.exemplo.usuario.ranking.domain.Ranking;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import java.util.ArrayList;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

class RankingDomainTest {
    @ParameterizedTest
    @CsvSource({"0,0,0", "1,0,100", "2,7,207", "1,150,250"})
    void aplicaRegraExistenteDeCursosEMoedas(int cursos, int moedas, int esperado) {
        assertThat(new ParticipanteRanking(1L, "Aluno", cursos, moedas).pontos()).isEqualTo(esperado);
    }

    @Test void ordenaPorPontosSemAlterarListaDeEntrada() {
        var ana = new ParticipanteRanking(1L, "Ana", 2, 7);
        var bia = new ParticipanteRanking(2L, "Bia", 1, 150);
        var entrada = new ArrayList<>(List.of(ana, bia));
        assertThat(Ranking.ordenar(entrada)).containsExactly(bia, ana);
        assertThat(entrada).containsExactly(ana, bia);
    }

    @Test void aceitaRankingVazio() {
        assertThat(Ranking.ordenar(List.of())).isEmpty();
    }
}
