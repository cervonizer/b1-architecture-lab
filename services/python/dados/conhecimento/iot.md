# Eventos de dispositivos

Dispositivos simulados publicam eventos de presenca, inicio e conclusao em MQTT com QoS 1. O broker e Mosquitto. O gateway valida e transforma o evento, grava em spool SQLite e envia ao Core. O eventId permite detectar duplicidade. Filas locais e sessao persistente permitem reenvio apos desconexao. QoS 1 permite redelivery e nao significa processamento exatamente uma vez.
