package com.exemplo.usuario.ranking.domain;

/** Dados de negocio imutaveis, sem dependencias de persistencia ou framework. */
public record ParticipanteRanking(Long usuarioId, String nome, int cursosConcluidos, int moedas) {
    public int pontos() {
        return cursosConcluidos * 100 + moedas;
    }
}
