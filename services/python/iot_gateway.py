"""MQTT -> spool duravel SQLite -> Core HTTP. Confirma MQTT apos commit local."""
import json
import os
import sqlite3
import time
import threading
import urllib.request
import base64
from pathlib import Path
import paho.mqtt.client as mqtt

TIPOS = {"presenca": "PRESENCA", "inicio": "INICIO", "conclusao": "CONCLUSAO"}

def transformar(topic, payload):
    dado = json.loads(payload)
    instituicao = dado["institution"]
    dispositivo = dado["device"]
    if topic != f"lab/{instituicao}/{dispositivo}/eventos": raise ValueError("Topico nao corresponde ao dispositivo")
    if dado["event"] not in TIPOS: raise ValueError("Evento desconhecido")
    if not isinstance(dado["user_id"], int) or dado["user_id"] <= 0: raise ValueError("Usuario invalido")
    for campo in ["id", "institution", "device"]:
        if not isinstance(dado[campo], str) or not 1 <= len(dado[campo]) <= 100: raise ValueError("Identificador invalido")
    return {"eventId": dado["id"], "deviceId": dispositivo, "institutionId": instituicao,
            "usuarioId": dado["user_id"], "tipo": TIPOS[dado["event"]]}

class Spool:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.db() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("CREATE TABLE IF NOT EXISTS eventos(id TEXT PRIMARY KEY,payload TEXT NOT NULL,entregue INT DEFAULT 0,tentativas INT DEFAULT 0)")
            db.execute("CREATE TABLE IF NOT EXISTS rejeitados(id INTEGER PRIMARY KEY,topico TEXT,payload TEXT,motivo TEXT)")
    def db(self): return sqlite3.connect(self.path, timeout=10)
    def salvar(self, evento):
        payload = json.dumps(evento, sort_keys=True)
        with self.db() as db:
            anterior = db.execute("SELECT payload FROM eventos WHERE id=?", (evento["eventId"],)).fetchone()
            if anterior and anterior[0] != payload: raise ValueError("eventId reutilizado com conteudo diferente")
            db.execute("INSERT OR IGNORE INTO eventos(id,payload) VALUES (?,?)", (evento["eventId"], payload))
    def rejeitar(self, topic, payload, erro):
        with self.db() as db: db.execute("INSERT INTO rejeitados(topico,payload,motivo) VALUES (?,?,?)", (topic,payload,erro))
    def pendentes(self):
        with self.db() as db: return db.execute("SELECT id,payload FROM eventos WHERE entregue=0 LIMIT 20").fetchall()
    def resultado(self, event_id, sucesso):
        with self.db() as db: db.execute("UPDATE eventos SET tentativas=tentativas+1,entregue=? WHERE id=?", (int(sucesso),event_id))

def despachar(spool, core_url, credencial):
    for event_id, payload in spool.pendentes():
        ok = False
        try:
            request = urllib.request.Request(core_url + "/api/iot/eventos", data=payload.encode(),
                headers={"Content-Type":"application/json","Authorization":"Basic " + credencial})
            with urllib.request.urlopen(request, timeout=2) as resposta: ok = resposta.status == 200
        except Exception as erro: print(json.dumps({"eventId":event_id,"entregue":False,"erro":str(erro)}), flush=True)
        spool.resultado(event_id, ok)
        if ok: print(json.dumps({"eventId":event_id,"entregue":True}), flush=True)

def main():
    spool = Spool(os.getenv("B1_SPOOL", "state/iot.db"))
    core = os.getenv("B1_CORE_URL", "http://localhost:18080")
    credencial = base64.b64encode((os.getenv("B1_CORE_USER","admin") + ":" + os.getenv("B1_CORE_PASSWORD","123456")).encode()).decode()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="b1-gateway", clean_session=False, manual_ack=True)
    client.username_pw_set(os.getenv("B1_MQTT_USER","gateway"),os.getenv("B1_MQTT_PASSWORD","b1-gateway-lab"))
    def conectado(client, userdata, flags, reason, properties):
        if reason == 0:
            client.subscribe("lab/+/+/eventos", qos=1)
            print("MQTT_CONNECTED", flush=True)
    def mensagem(client, userdata, msg):
        payload = msg.payload.decode(errors="replace")
        try:
            evento = transformar(msg.topic, payload)
            spool.salvar(evento)
            print(json.dumps({"eventId":evento["eventId"],"spool":True}), flush=True)
        except (ValueError, KeyError, TypeError) as erro:
            spool.rejeitar(msg.topic, payload, str(erro))
            print(json.dumps({"rejeitado":True,"erro":str(erro)}), flush=True)
        # Persistencia bem sucedida (evento ou quarentena) antes do PUBACK.
        client.ack(msg.mid,msg.qos)
    client.on_connect=conectado;client.on_message=mensagem
    client.connect(os.getenv("B1_MQTT_HOST","localhost"),int(os.getenv("B1_MQTT_PORT","18883")),60)
    client.loop_start()
    try:
        while True: despachar(spool,core,credencial);time.sleep(1)
    finally: client.disconnect();client.loop_stop()

if __name__ == "__main__": main()
