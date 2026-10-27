package com.exemplo.usuario.usuario.application;

import com.exemplo.usuario.usuario.api.ConsultaPontuacao;
import com.exemplo.usuario.usuario.internal.persistence.PontuacaoRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class ConsultaPontuacaoService implements ConsultaPontuacao {
    private final PontuacaoRepository repository;

    public ConsultaPontuacaoService(PontuacaoRepository repository) {
        this.repository = repository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<PontuacaoUsuario> listar() {
        return repository.buscarParticipantes().stream().map(a -> new PontuacaoUsuario(
                a.getUsuario().getId(), a.getUsuario().getNome(),
                a.getCursosConcluidosComSucesso(), a.getMoedas())).toList();
    }
}
