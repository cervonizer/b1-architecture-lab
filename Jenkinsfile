pipeline {
    agent any
    tools { jdk 'JDK17'; maven 'Maven' }
    options { skipDefaultCheckout(true); disableConcurrentBuilds(); timestamps() }
    parameters {
        string(name: 'SOURCE_DIR', defaultValue: '', description: 'Somente laboratorio sem remoto: pasta local do projeto. Vazio usa checkout scm.')
        string(name: 'PYTHON_BIN', defaultValue: 'python3', description: 'Python 3.12 para preparar o ambiente isolado')
        string(name: 'LLM_DIR', defaultValue: '', description: 'Cache local dos pesos Qwen; vazio usa .cache/modelos no workspace')
        string(name: 'MAVEN_REPO', defaultValue: '.cache/m2', description: 'Cache Maven do agente')
        booleanParam(name: 'EXECUTAR_MICROLABS', defaultValue: true, description: 'Requer Docker Desktop e portas 18080/18081/18883/19091/13001 livres')
    }
    environment {
        B1_LLM_DIR = "${params.LLM_DIR?.trim() ?: '.cache/modelos/qwen2.5-0.5b'}"
        B1_TESTAR_LLM = '1'
        PATH = "/usr/local/bin:/opt/homebrew/bin:/Applications/Docker.app/Contents/Resources/bin:${env.PATH}"
    }
    stages {
        stage('1 Checkout ou fonte local') {
            steps {
                script {
                    if (params.SOURCE_DIR?.trim()) {
                        withEnv(["B1_SOURCE=${params.SOURCE_DIR}"]) {
                            sh 'cp -R "$B1_SOURCE"/. .'
                        }
                    } else { checkout scm }
                }
            }
        }
        stage('2 Core testes e artefato') {
            steps { sh 'mvn -B -Dmaven.repo.local="$MAVEN_REPO" clean verify' }
            post { always { junit 'target/surefire-reports/*.xml' } }
        }
        stage('3 Python testes') {
            steps {
                sh '''
                    "$PYTHON_BIN" -m venv .venv
                    .venv/bin/python -m pip install -r services/python/requirements.lock.txt
                    .venv/bin/python scripts/preparar_llm.py
                    PYTHONPATH=services/python .venv/bin/python -m pytest services/python/tests -q --junitxml=python-tests.xml
                '''
            }
            post { always { junit 'python-tests.xml' } }
        }
        stage('4 Fronteiras de arquitetura') {
            steps { sh '.venv/bin/python scripts/verificar_fronteira.py' }
        }
        stage('5 Implantacao e experimentos') {
            when { expression { params.EXECUTAR_MICROLABS } }
            steps {
                sh '''
                    docker compose -f compose.lab.yml up -d
                    B1_JAVA="$JAVA_HOME/bin/java" .venv/bin/python scripts/rodar_microlabs.py
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'target/*.jar,docs/arquitetura/**,docs/adr/**,docs/evidencias/**,infra/**,state-lab/*.log,python-tests.xml', allowEmptyArchive: false
        }
        success { echo 'ASRs verificados pelos testes e experimentos registrados.' }
        failure { echo 'Falha bloqueia a continuidade; consultar o estagio e os relatorios.' }
    }
}
