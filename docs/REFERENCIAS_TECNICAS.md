# Referências técnicas consultadas

- FastAPI e modelos de requisição: https://fastapi.tiangolo.com/reference/fastapi/
- FastAPI código e documentação oficial: https://github.com/fastapi/fastapi
- Paho MQTT Python API, confirmação manual e QoS: https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html
- Limites de sessão do cliente Paho e wait_for_publish: https://github.com/eclipse-paho/paho.mqtt.python
- Spring Boot 3.5 métricas: https://docs.spring.io/spring-boot/3.5/reference/actuator/metrics.html

As dependências diretas e o lock Python registram as versões efetivamente usadas. O Core permanece Spring Boot 3.5.5 da base, sem migração para a linha mais recente das páginas oficiais. Resultados de testes/experimentos são evidências próprias, não inferidos da documentação.

## IA real

- Pesos e model card oficiais Qwen2.5 0.5B Instruct: https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct
- Revisão fixada: 7ae557604adf67be50417f59c2c2f167def9a775, licença Apache 2.0.
- Separação por grupos de perfis: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html
- Classificador: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
- Incompatibilidade observada de SciPy 1.15 com macOS recente: https://github.com/scipy/scipy/issues/25635. O ambiente validado usa SciPy 1.17.0.
