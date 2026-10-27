package com.exemplo.usuario.ranking.application.port;

import com.exemplo.usuario.ranking.domain.ParticipanteRanking;
import java.util.List;

/** Porta de saida definida pelo caso de uso de Ranking. Nao exige ordem de entrada. */
public interface CarregarParticipantes {
    List<ParticipanteRanking> carregar();
}
