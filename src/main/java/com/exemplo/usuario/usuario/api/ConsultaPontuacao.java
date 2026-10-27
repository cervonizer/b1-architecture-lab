package com.exemplo.usuario.usuario.api;

import java.util.List;

/** Contrato de leitura entre modulos; nao expoe entidades JPA. */
public interface ConsultaPontuacao {
    List<PontuacaoUsuario> listar();

    record PontuacaoUsuario(Long usuarioId, String nome, Integer cursosConcluidos, Integer moedas) {}
}
