package com.exemplo.usuario.eventos;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface OutboxRepository extends JpaRepository<EventoPendente,String> {
    List<EventoPendente> findTop20ByEntregueFalseOrderByCriadoEmAsc();
    long countByEntregueFalse();
}
