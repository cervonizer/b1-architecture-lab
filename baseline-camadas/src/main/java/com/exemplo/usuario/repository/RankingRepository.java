package com.exemplo.usuario.repository;

import com.exemplo.usuario.domain.Assinatura;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface RankingRepository extends JpaRepository<Assinatura, Long> {
    @Query("select a from Assinatura a join fetch a.usuario order by (a.cursosConcluidosComSucesso * 100 + a.moedas) desc")
    List<Assinatura> buscarRanking();
}
