package com.exemplo.usuario.matricula.internal.persistence;

import com.exemplo.usuario.matricula.domain.Matricula;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

// Repository de Matricula.
public interface MatriculaRepository extends JpaRepository<Matricula, Long> {

    // O Spring Data entende "findByUsuarioId" e monta a consulta.
    List<Matricula> findByUsuarioId(Long usuarioId);
    @org.springframework.data.jpa.repository.Lock(jakarta.persistence.LockModeType.PESSIMISTIC_WRITE)
    @org.springframework.data.jpa.repository.Query("select m from Matricula m where m.id = :id")
    java.util.Optional<Matricula> buscarParaConclusao(@org.springframework.data.repository.query.Param("id") Long id);
}
