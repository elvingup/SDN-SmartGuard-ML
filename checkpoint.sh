#!/bin/bash

# =================================================================
# SCRIPT DE CHECK-OUT AUTOMATIZADO - SDN-SmartGuard-ML
# Objetivo: Persistência, Saneamento e Desmobilização de Recursos
# Para que o script funcione corretamente, siga estas etapas no seu terminal:
# 1. chmod +x checkpoint.sh
# 2. ./checkpoint.sh
# =================================================================

echo "--- INICIANDO PROTOCOLO DE CHECK-OUT DEVOPS ---"

# 1. PERSISTÊNCIA NO REPOSITÓRIO (GIT)
echo "[1/5] Registrando progresso no Git..."
echo "Fazer o git commit."

# 2. PARADA DE ORQUESTRAÇÃO (DOCKER)
echo "[2/5] Desligando containers ativos..."
if [ "$(docker ps -q)" ]; then
    docker stop $(docker ps -q)
    echo "Containers interrompidos."
else
    echo "Nenhum container ativo encontrado."
fi

# 3. FINALIZAÇÃO DE PROCESSOS DE REDE (MININET/PYTHON)
echo "[3/5] Limpando topologia Mininet e processos Python..."
sudo mn -c > /dev/null 2>&1
pkill -f monitor_ia.py
pkill -f deploy_nornir.py
echo "Processos de rede e monitoramento encerrados."

# 4. SANITIZAÇÃO DO AMBIENTE (LIMPEZA DE CACHE)
echo "[4/5] Removendo artefatos temporários e caches..."
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf .pytest_cache
rm -f *.log
echo "Ambiente sanitizado (__pycache__ e logs removidos)."

# 5. FINALIZAÇÃO DO WORKSPACE
echo "[5/5] Protocolo concluído."
echo "---------------------------------------------------------"
echo "ATENÇÃO RECRUTA: Execute 'deactivate' manualmente para sair do venv."
echo "--- 🫡 MISSÃO CUMPRIDA. AMBIENTE SEGURO PARA ENCERRAMENTO ---"
