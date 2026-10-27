package com.exemplo.usuario.fake;

import com.exemplo.usuario.ranking.application.port.CarregarParticipantes;
import com.exemplo.usuario.ranking.domain.ParticipanteRanking;
import java.util.List;

/** Fake usado somente no laboratorio e nos testes; nao e bean da aplicacao. */
public final class ParticipantesEmMemoria implements CarregarParticipantes {
    private final List<ParticipanteRanking> participantes;

    public ParticipantesEmMemoria(List<ParticipanteRanking> participantes) {
        this.participantes = List.copyOf(participantes);
    }

    @Override
    public List<ParticipanteRanking> carregar() {
        return participantes;
    }
}
