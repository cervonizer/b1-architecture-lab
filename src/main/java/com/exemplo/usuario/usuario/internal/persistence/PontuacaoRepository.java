package com.exemplo.usuario.usuario.internal.persistence;

import com.exemplo.usuario.usuario.domain.Assinatura;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface PontuacaoRepository extends JpaRepository<Assinatura, Long> {
    @Query("select a from Assinatura a join fetch a.usuario")
    List<Assinatura> buscarParticipantes();
}
