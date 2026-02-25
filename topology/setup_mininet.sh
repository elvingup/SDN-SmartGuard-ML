#!/bin/bash

# =====================================================================
# PROJETO: SDN-SmartGuard-ML
# DESCRIÇÃO: Automação da Infraestrutura de Rede (Plano de Dados)
# AUTOR: elvingup
# DATA: 2026-02-25
# =====================================================================

echo "🚀 Iniciando faxina tática no Mininet..."
sudo mn -c > /dev/null 2>&1

echo "Levantando topologia SDN (Single Switch, 3 Hosts)..."
echo "Conectando ao controlador remoto em 127.0.0.1:6633"

# Comando principal para instanciar a rede
# - controller=remote: busca o Ryu fora do ambiente do Mininet
# - topo=single,3: cria 1 switch e 3 computadores
# - switch=ovsk: usa o Open vSwitch (padrão SDN)
# - protocols=OpenFlow13: versão necessária para os dados da IA
sudo mn --controller=remote,ip=127.0.0.1,port=6633 --topo=single,3 --switch=ovsk,protocols=OpenFlow13
