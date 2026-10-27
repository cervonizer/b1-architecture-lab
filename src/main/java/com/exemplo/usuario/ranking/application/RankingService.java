package com.exemplo.usuario.ranking.application;

import com.exemplo.usuario.ranking.api.RankingResponseDTO;
import com.exemplo.usuario.ranking.application.port.CarregarParticipantes;
import com.exemplo.usuario.ranking.domain.Ranking;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class RankingService {
    private final CarregarParticipantes participantes;

    public RankingService(CarregarParticipantes participantes) {
        this.participantes = participantes;
    }

    public List<RankingResponseDTO> listar() {
        return Ranking.ordenar(participantes.carregar()).stream().map(a -> new RankingResponseDTO(
                a.usuarioId(), a.nome(), a.cursosConcluidos(), a.moedas(), a.pontos())).toList();
    }
}
