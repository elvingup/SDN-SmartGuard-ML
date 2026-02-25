# Passo 1: Base estável e leve para SDN e IA
FROM python:3.9-slim

# Passo 2: Instalação de dependências de sistema para compilação
# Necessário para que bibliotecas de rede e IA sejam montadas corretamente
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Passo 3: Definição do diretório de trabalho interno
WORKDIR /app

# Passo 4: O "Pulo do Gato" DevOps
# Travamos o setuptools abaixo da v58 para garantir que o Ryu instale sem erros
RUN pip install --no-cache-dir "setuptools<58.0.0" "pip<23.2" wheel

# Fixar a versão do eventlet, visto que o Ryu busca pelo atributo 'ALREADY_HANDLED' do arquivo eventlet.wsgi
RUN pip install --no-cache-dir "eventlet==0.30.2"

# Passo 5: Instalação das Tecnologias Alvo
# Ryu para SDN + Stack de IA para gestão inteligente
RUN pip install --no-cache-dir ryu pandas scikit-learn numpy matplotlib

# Passo 6: Exposição de portas (OpenFlow usa a 6633 ou 6653)
EXPOSE 6633 6653

# Comando padrão para iniciar o controlador
CMD ["ryu-manager"]
