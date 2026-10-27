package com.exemplo.usuario.ranking.internal.persistence;

import com.exemplo.usuario.ranking.application.port.CarregarParticipantes;
import com.exemplo.usuario.ranking.domain.ParticipanteRanking;
import com.exemplo.usuario.usuario.api.ConsultaPontuacao;
import org.springframework.stereotype.Component;
import java.util.List;

/** Adapter para os dados relacionais, respeitando a API publica do modulo Usuario. */
@Component
public class JpaParticipantesAdapter implements CarregarParticipantes {
    private final ConsultaPontuacao consulta;

    public JpaParticipantesAdapter(ConsultaPontuacao consulta) {
        this.consulta = consulta;
    }

    @Override
    public List<ParticipanteRanking> carregar() {
        return consulta.listar().stream().map(a -> new ParticipanteRanking(
                a.usuarioId(), a.nome(), a.cursosConcluidos(), a.moedas())).toList();
    }
}
