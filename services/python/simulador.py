"""Simulador com fila local: mantem eventos nao confirmados para replay."""
import json,os,uuid,argparse,sqlite3
from pathlib import Path
import paho.mqtt.publish as publish

def enfileirar(path, evento):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS saida(id TEXT PRIMARY KEY,payload TEXT,confirmado INT DEFAULT 0)')
        db.execute('INSERT OR IGNORE INTO saida(id,payload) VALUES (?,?)',(evento['id'],json.dumps(evento)))

def replay(path, publisher):
    with sqlite3.connect(path) as db:
        eventos=db.execute('SELECT id,payload FROM saida WHERE confirmado=0').fetchall()
    for event_id,payload in eventos:
        publisher(payload)  # QoS 1: so retorna apos o PUBACK do broker.
        with sqlite3.connect(path) as db:db.execute('UPDATE saida SET confirmado=1 WHERE id=?',(event_id,))
    return len(eventos)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--id',default=str(uuid.uuid4()))
    parser.add_argument('--evento',default='conclusao',choices=['presenca','inicio','conclusao'])
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args();path=os.getenv('B1_DEVICE_DB','state/device.db')
    evento={'id':args.id,'device':'dispositivo-1','institution':'instituicao-1','user_id':1,'event':args.evento}
    if not args.replay:enfileirar(path,evento)
    def enviar(payload):
        publish.single('lab/instituicao-1/dispositivo-1/eventos',payload,qos=1,
            hostname=os.getenv('B1_MQTT_HOST','localhost'),port=int(os.getenv('B1_MQTT_PORT','18883')),
            auth={'username':'device01','password':'b1-device-lab'})
    try:print(json.dumps({'confirmados':replay(path,enviar)}))
    except Exception as e:
        print(json.dumps({'fila_preservada':True,'erro':str(e)}));raise SystemExit(2)

if __name__=='__main__':main()
