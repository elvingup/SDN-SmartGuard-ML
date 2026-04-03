# Usando imagem base Python slim para reduzir superfície de ataque
FROM python:3.11-slim

# Instalar dependências de sistema para compilação de libs de ML e rede
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar apenas os requisitos primeiro para otimizar cache de camadas
COPY controller/monitor_ia.py .
# O controlador precisa do inventário para realizar a HABILIDADE de automação
COPY topology/ ./topology/

# Instalação das tecnologias de IA, SDN e Observabilidade
RUN pip install --no-cache-dir \
    nornir \
    nornir_netmiko \
    pandas \
    numpy \
    scikit-learn \
    prometheus_client

# Expor a porta do Prometheus Exporter
EXPOSE 8000

# Comando para iniciar o cérebro SDN
CMD ["python", "monitor_ia.py"]
