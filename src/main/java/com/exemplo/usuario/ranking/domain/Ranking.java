package com.exemplo.usuario.ranking.domain;

import java.util.Comparator;
import java.util.List;

public final class Ranking {
    private Ranking() {}

    /** Preserva a ordem de entrada nos empates; nao cria um desempate de negocio. */
    public static List<ParticipanteRanking> ordenar(List<ParticipanteRanking> participantes) {
        return participantes.stream()
                .sorted(Comparator.comparingInt(ParticipanteRanking::pontos).reversed())
                .toList();
    }
}
