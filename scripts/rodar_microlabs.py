"""Executa os experimentos D3-D6 com processos reais e MQTT real.
Requer compose.lab.yml ativo, JAR compilado, Java 17 e dependencias Python instaladas.
"""
from pathlib import Path
import os, sys, json, time, base64, subprocess, urllib.request, urllib.error, sqlite3, uuid, argparse

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'state-lab';STATE.mkdir(exist_ok=True)
EVID=ROOT/'docs/evidencias'
AUTH=base64.b64encode(b'admin:123456').decode()
CORE=os.getenv('B1_CORE_URL','http://127.0.0.1:18080')
PYTHON='http://127.0.0.1:18081'
processos={};arquivos=[];resultados={k:[] for k in ['desafio3','desafio4','desafio5','desafio6']}
run_id=str(uuid.uuid4())

def registrar(desafio,etapa,**dados):
    dado={'etapa':etapa,'instante_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'run_id':run_id,**dados}
    resultados[desafio].append(dado);print(json.dumps({'desafio':desafio,**dado},ensure_ascii=False),flush=True)

def request(base,path,method='GET',body=None,auth=True):
    payload=None if body is None else json.dumps(body).encode()
    headers={'Content-Type':'application/json'}
    if auth:headers['Authorization']='Basic '+AUTH
    req=urllib.request.Request(base+path,data=payload,headers=headers,method=method)
    inicio=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=65 if path=="/api/ia/assistente" else 5) as r:code=r.status;raw=r.read().decode()
    except urllib.error.HTTPError as e:code=e.code;raw=e.read().decode()
    try:data=json.loads(raw)
    except ValueError:data=raw
    return code,data,round((time.monotonic()-inicio)*1000,2)

def aguardar(check,timeout=40):
    limite=time.monotonic()+timeout
    while time.monotonic()<limite:
        try:
            valor=check()
            if valor:return valor
        except Exception:pass
        time.sleep(.3)
    raise RuntimeError('Timeout ao aguardar estado do laboratorio')

def iniciar(nome,cmd,env=None):
    arquivo=open(STATE/(nome+'.log'),'a');arquivos.append(arquivo)
    processos[nome]=subprocess.Popen(cmd,cwd=ROOT,env=env or os.environ.copy(),stdout=arquivo,stderr=subprocess.STDOUT)

def parar(nome):
    p=processos.pop(nome,None)
    if p:
        p.terminate()
        try:p.wait(timeout=8)
        except subprocess.TimeoutExpired:p.kill();p.wait()

def iniciar_python():
    env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'services/python')+os.pathsep+env.get('PYTHONPATH','')
    env['B1_PYTHON_DB']=str(STATE/'python.db');env['B1_FAILURE_FILE']=str(STATE/'notificacoes.off')
    iniciar('python',[sys.executable,'-m','uvicorn','ia_service:app','--host','127.0.0.1','--port','18081'],env)
    aguardar(lambda:request(PYTHON,'/health',auth=False)[0]==200,timeout=180)

def iniciar_gateway(core):
    env=os.environ.copy();env['B1_CORE_URL']=core;env['B1_SPOOL']=str(STATE/'iot.db')
    iniciar('gateway',[sys.executable,str(ROOT/'services/python/iot_gateway.py')],env)
    # Aguardar SUBACK/CONNACK antes de publicar ou encerrar para testar sessao persistente.
    aguardar(lambda:'MQTT_CONNECTED' in (STATE/'gateway.log').read_text())
    time.sleep(.5)

def spool_count(entregue):
    with sqlite3.connect(STATE/'iot.db') as db:return db.execute('SELECT count(*) FROM eventos WHERE entregue=?',(entregue,)).fetchone()[0]

def publicar(event_id):
    from paho.mqtt.publish import single
    evento={'id':event_id,'device':'dispositivo-1','institution':'instituicao-1','user_id':1,'event':'conclusao'}
    single('lab/instituicao-1/dispositivo-1/eventos',json.dumps(evento),qos=1,hostname='127.0.0.1',port=18883,
           auth={'username':'device01','password':'b1-device-lab'})
    return evento

def executar():
    # Estado de servicos e dados e exclusivo deste laboratorio; nao altera a app da porta 8080.
    for f in ['python.db','python.db-shm','python.db-wal','iot.db','iot.db-shm','iot.db-wal','notificacoes.off','gateway.log','device.db']:
        (STATE/f).unlink(missing_ok=True)
    jar=next((ROOT/'target').glob('*.jar'))
    java=os.getenv('B1_JAVA','/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home/bin/java')
    iniciar('core',[java,'-jar',str(jar),'--server.port=18080','--spring.profiles.active=h2',
                    '--b1.eventos.agendador=false','--b1.ia.url='+PYTHON,'--b1.notificacao.url='+PYTHON+'/notificacoes'])
    aguardar(lambda:request(CORE,'/actuator/health',auth=False)[0]==200)
    iniciar_python()
    code,aluno,_=request(CORE,'/api/usuarios','POST',{'nome':'Aluno Laboratorio','email':'lab-'+run_id+'@example.com','senha':'Teste123456'})
    assert code==201,(code,aluno)
    code,curso,_=request(CORE,'/api/cursos','POST',{'titulo':'Java e arquitetura modular','descricao':'Java Spring arquitetura monolito modular dominio'})
    assert code==201,(code,curso)
    code,iot_curso,_=request(CORE,'/api/cursos','POST',{'titulo':'IoT e MQTT','descricao':'iot mqtt sensores dispositivos redes eventos'})
    assert code==201
    code,python_curso,_=request(CORE,'/api/cursos','POST',{'titulo':'Python e aprendizado de maquina','descricao':'python dados aprendizado maquina recomendacao'})
    assert code==201
    code,matricula,_=request(CORE,'/api/matriculas','POST',{'usuarioId':aluno['id'],'cursoId':curso['id'],'bonus':False})
    assert code==201,(code,matricula)
    code,dados,ms=request(CORE,'/api/ia/recomendacoes?interesses=java,arquitetura&nivel=2');assert code==200 and dados['degradado'] is False
    assert dados['fonte']=='modelo-supervisionado' and dados['cursos'][0]['id']==curso['id']
    registrar('desafio3','python_disponivel',http=code,resposta=dados,duracao_ms=ms)
    code,iot_recomendado,_=request(CORE,'/api/ia/recomendacoes?interesses=iot,mqtt&nivel=2')
    assert code==200 and iot_recomendado['cursos'][0]['id']==iot_curso['id']
    registrar('desafio3','personalizacao_com_modelo_treinado',resposta=iot_recomendado)
    code,dados,_=request(CORE,'/api/ia/assistente','POST',{'pergunta':'Quantos creditos recebo ao concluir um curso com aproveitamento?'})
    assert code==200 and dados['geracao']['executada'] is True and dados['geracao']['tokens_gerados']>0
    assert any(f['id']=='creditos' for f in dados['fontes'])
    registrar('desafio3','rag_com_llm_real_e_fontes',resposta=dados)
    parar('python')
    code,dados,ms=request(CORE,'/api/ia/recomendacoes');assert code==200 and dados['degradado'] is True
    registrar('desafio3','processo_python_interrompido',http=code,resposta=dados,duracao_ms=ms)
    code,dados,_=request(CORE,'/api/cursos');assert code==200 and len(dados)==3
    registrar('desafio3','core_essencial_continua',http=code,cursos=len(dados))
    iniciar_python()
    request(PYTHON,'/lab/notificacoes/falha','POST',{'ativo':True},auth=False)
    code,dados,ms=request(CORE,'/api/lab/eventos/sincrono','POST',{'event_id':'sync-'+run_id,'tipo':'TESTE'})
    assert code==503,(code,dados);registrar('desafio4','sincrono_consumidor_indisponivel',http=code,duracao_ms=ms)
    path='/api/matriculas/'+str(matricula['id'])+'/concluir'
    code,dados,ms=request(CORE,path,'PUT',{'notaFinal':8});assert code==200 and dados['status']=='CONCLUIDO'
    registrar('desafio4','conclusao_assincrona_com_consumidor_fora',http=code,resposta=dados,duracao_ms=ms)
    request(CORE,path,'PUT',{'notaFinal':8})
    code,aluno,_=request(CORE,'/api/usuarios/'+str(aluno['id']));assert aluno['creditosCursos']==3 and aluno['cursosConcluidosComSucesso']==1
    registrar('desafio4','repeticao_idempotente',usuario=aluno)
    code,dados,_=request(CORE,'/api/lab/eventos/despachar','POST',{});assert dados['entregues']==0
    code,dados,_=request(CORE,'/api/lab/eventos/pendentes');assert dados['pendentes']==1
    registrar('desafio4','evento_retido_apos_falha',resposta=dados)
    request(PYTHON,'/lab/notificacoes/falha','POST',{'ativo':False},auth=False)
    code,dados,_=request(CORE,'/api/lab/eventos/despachar','POST',{});assert dados['entregues']==1
    code,pendentes,_=request(CORE,'/api/lab/eventos/pendentes');assert pendentes['pendentes']==0
    code,notificacoes,_=request(PYTHON,'/lab/notificacoes',auth=False);assert notificacoes['recebidas']==1
    registrar('desafio4','recuperacao_e_entrega',pendentes=pendentes,consumidor=notificacoes)
    # Core temporariamente inacessivel PARA O GATEWAY; core continua rodando para outros fluxos.
    iniciar_gateway('http://127.0.0.1:18089')
    evt1='iot-'+run_id+'-1';publicar(evt1)
    aguardar(lambda:spool_count(0)==1)
    registrar('desafio5','mqtt_recebido_core_inacessivel',pendentes_spool=spool_count(0),eventId=evt1)
    parar('gateway');(STATE/'gateway.log').unlink(missing_ok=True)
    iniciar_gateway(CORE)
    aguardar(lambda:request(CORE,'/api/iot/eventos')[1]['eventos']==1)
    aguardar(lambda:spool_count(1)==1)
    registrar('desafio5','replay_duravel_apos_reinicio',eventos_core=1,entregues_spool=spool_count(1))
    publicar(evt1);time.sleep(.5)
    assert request(CORE,'/api/iot/eventos')[1]['eventos']==1
    code,dados,_=request(CORE,'/api/iot/eventos','POST',{'eventId':evt1,'deviceId':'dispositivo-1','institutionId':'instituicao-1','usuarioId':1,'tipo':'CONCLUSAO'})
    assert dados['duplicado'] is True
    registrar('desafio5','duplicidade_controlada',resposta=dados)
    parar('gateway');(STATE/'gateway.log').unlink(missing_ok=True)
    evt2='iot-'+run_id+'-2';publicar(evt2)
    iniciar_gateway(CORE)
    aguardar(lambda:request(CORE,'/api/iot/eventos')[1]['eventos']==2)
    registrar('desafio5','sessao_mqtt_entrega_evento_publicado_com_gateway_offline',eventos_core=2,eventId=evt2)
    # Dispositivo perde a conexao antes de publicar: fila local preserva o evento.
    env=os.environ.copy();env['B1_DEVICE_DB']=str(STATE/'device.db');env['B1_MQTT_PORT']='18884'
    evt3='iot-'+run_id+'-3'
    offline=subprocess.run([sys.executable,str(ROOT/'services/python/simulador.py'),'--id',evt3],env=env,capture_output=True,text=True)
    assert offline.returncode==2,offline.stdout
    env['B1_MQTT_PORT']='18883'
    online=subprocess.run([sys.executable,str(ROOT/'services/python/simulador.py'),'--replay'],env=env,capture_output=True,text=True)
    assert online.returncode==0,online.stdout
    aguardar(lambda:request(CORE,'/api/iot/eventos')[1]['eventos']==3)
    registrar('desafio5','dispositivo_offline_enfileira_e_reenvia',offline=json.loads(offline.stdout),online=json.loads(online.stdout),eventos_core=3)
    code,metricas,_=request(CORE,'/actuator/prometheus');assert code==200
    for nome in ['b1_ia_calls_total','b1_outbox_pending','b1_outbox_attempts_total','b1_iot_received_total']:assert nome in metricas,nome
    (EVID/'desafio6').mkdir(parents=True,exist_ok=True)
    (EVID/'desafio6/metricas.prom').write_text(metricas)
    prom='http://127.0.0.1:19091'
    aguardar(lambda:request(prom,'/api/v1/query?query=b1_ia_calls_total',auth=False)[1].get('data',{}).get('result'))
    code,consulta,_=request(prom,'/api/v1/query?query=b1_ia_calls_total',auth=False)
    registrar('desafio6','prometheus_observa_fallback_real',http=code,resposta=consulta)
    code,targets,_=request(prom,'/api/v1/targets',auth=False)
    assert any(t['health']=='up' and t['labels'].get('job')=='b1-core' for t in targets['data']['activeTargets'])
    registrar('desafio6','alvo_prometheus_up',http=code,resposta=targets)
    # Falha novamente o consumidor para deixar uma condicao observavel no dashboard.
    request(PYTHON,'/lab/notificacoes/falha','POST',{'ativo':True},auth=False)
    code,mat2,_=request(CORE,'/api/matriculas','POST',{'usuarioId':aluno['id'],'cursoId':curso['id'],'bonus':False});assert code==201
    request(CORE,'/api/matriculas/'+str(mat2['id'])+'/concluir','PUT',{'notaFinal':8})
    request(CORE,'/api/lab/eventos/despachar','POST',{})
    aguardar(lambda:any(float(x['value'][1])>=1 for x in request(prom,'/api/v1/query?query=b1_outbox_pending',auth=False)[1].get('data',{}).get('result',[])))
    registrar('desafio6','fila_pendente_observada',resposta=request(prom,'/api/v1/query?query=b1_outbox_pending',auth=False)[1])
    for desafio,dados in resultados.items():
        destino=EVID/desafio;destino.mkdir(parents=True,exist_ok=True)
        (destino/'experimento.json').write_text(json.dumps(dados,ensure_ascii=False,indent=2)+'\n')
    print('LAB_SUCCESS',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--keep-running',action='store_true');args=parser.parse_args()
    try:
        executar()
        if args.keep_running:
            print('SERVICOS_ATIVOS: Core 18080, Python 18081, Grafana 13001, Prometheus 19091',flush=True)
            while True:time.sleep(30)
    finally:
        for nome in list(processos):parar(nome)
        for f in arquivos:f.close()
