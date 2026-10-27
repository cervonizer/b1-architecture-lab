package com.exemplo.usuario.iot;
import org.springframework.data.jpa.repository.JpaRepository;
public interface IotRepository extends JpaRepository<IotEvent,String>{}
