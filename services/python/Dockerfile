FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.6.0 \
    && pip install --no-cache-dir -r requirements.txt
COPY *.py .
COPY dados ./dados
COPY modelos ./modelos
ENV B1_LLM_DIR=/modelos/llm
# Monte o cache preparado pelo scripts/preparar_llm.py em /modelos/llm:ro.
CMD ["uvicorn", "ia_service:app", "--host", "0.0.0.0", "--port", "8000"]
