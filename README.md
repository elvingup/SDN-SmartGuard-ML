# 🚀 SDN-SmartGuard-ML: Inteligência Artificial na Gestão de Infraestrutura

## 📝 Visão Geral

Este projeto é um **Laboratório de Aprendizado de Máquina aplicado a Redes Definidas por Software (SDN)**. Desenvolvido para execução em ambiente **Linux**, ele demonstra como utilizar Python e IA para automatizar a gestão de ativos de TIC, promovendo segurança adaptativa e eficiência operacional.

O objetivo central é a **redução de custos operacionais (OpEx)** e de capital (CapEx) ao substituir ferramentas proprietárias de monitoramento por uma solução programável e inteligente.

---

## 🏗️ Arquitetura do Sistema

O projeto utiliza a separação clássica de SDN entre o Plano de Controle e o Plano de Dados:

* **Plano de Controle (O Cérebro):** Um container Docker rodando o **Ryu Controller** com um motor de IA integrado.
* **Plano de Dados (O Corpo):** Uma topologia emulada no **Mininet** com **Open vSwitch (OVS)**.
* **Protocolo de Comunicação:** **OpenFlow 1.3**, responsável por enviar estatísticas do switch para a IA e receber regras de fluxo.

---

## 🧠 Como a IA Funciona

Utilizamos o algoritmo **Isolation Forest** (Floresta de Isolamento). Diferente de IAs tradicionais que tentam aprender o que é "normal", o Isolation Forest foca em "isolar" o que é estranho.

* **Lógica:** O algoritmo cria árvores de decisão para isolar cada ponto de dado. Anomalias (como ataques DDoS) são isoladas em poucas etapas, pois possuem características discrepantes (ex: pacotes com tamanhos incomuns ou frequência excessiva).
* **Vantagem:** É extremamente leve para execução em tempo real dentro do controlador SDN, permitindo uma resposta rápida a incidentes.

---

## 💰 Valor de Negócio: Redução de Custos

Gestores de TI podem utilizar este projeto para:

1. **Eliminar Vendor Lock-in:** Redução de custos ao utilizar hardware *commodity* controlado por software *open-source*.
2. **Automação de Segurança:** Menos necessidade de intervenção humana manual para detectar ataques volumétricos.
3. **Visibilidade Granular:** Monitoramento detalhado do tráfego sem a necessidade de dispositivos de *mirroring* caros.

---

## 🛠️ Pré-requisitos

* Sistema Operacional: **Linux** (Ubuntu 22.04+ recomendado).
* **Docker** instalado.
* **Mininet** instalado nativamente no host.
* Python 3 e biblioteca **Scapy** (para os testes de estresse).

---

## 🚀 Procedimento Passo a Passo

Siga rigorosamente uma etapa por vez para garantir a integridade da infraestrutura.

### 1. Construção do Cérebro (Controller)

Entre na pasta do projeto e faça o build da imagem Docker.

```bash
docker build -t sdn-ia-controller ./controller

```

* **Explicação:** Este comando lê o `Dockerfile` e instala todas as dependências (Ryu, Scikit-Learn, Eventlet).
* **Justificativa:** Usar Docker garante que o controlador funcione de forma idêntica em qualquer máquina Linux, evitando conflitos de versão do Python.

### 2. Inicialização do Monitoramento Inteligente

Execute o container do controlador mapeando as portas de rede.

```bash
docker run -it --rm --name ryu_manager -v $(pwd):/app -p 6633:6633 sdn-ia-controller ryu-manager controller/monitor_ia.py

```

* **Explicação:** Inicia o Ryu e carrega o script de IA. A porta 6633 é aberta para ouvir o switch.
* **Justificativa:** O parâmetro `-v` permite que você altere o código no host e veja o efeito imediato no container.

### 3. Provisionamento da Infraestrutura (Topology)

Em um novo terminal, execute o script de automação do Mininet.

```bash
chmod +x topology/setup_mininet.sh
sudo ./topology/setup_mininet.sh

```

* **Explicação:** Limpa redes antigas e sobe uma topologia de 1 switch e 3 hosts usando OpenFlow 1.3.
* **Justificativa:** A automação via script (`.sh`) evita erros de digitação nos comandos complexos do Mininet.

### 4. Teste de Conectividade Base

Dentro do prompt do Mininet, valide se a IA está permitindo o tráfego comum.

```bash
mininet> pingall

```

* **Explicação:** Tenta enviar pacotes entre todos os hosts da rede.
* **Justificativa:** Confirma que a lógica de *switching* no script Python está funcionando antes de testarmos a segurança.

### 5. Simulação de Ataque e Reação da IA

Em um terceiro terminal, dispare o ataque de estresse para testar a IA.

```bash
sudo python3 tools/ataque_ddos.py 10.0.0.2

```

* **Explicação:** O Scapy envia uma inundação de pacotes para o host 2.
* **Justificativa:** Serve para validar se o algoritmo de IA no terminal do Ryu exibirá os alertas de "Tráfego Anômalo Detectado".

---

## 👤 Autor

* **Usuário:** elvingup
* **Contexto:** Projeto de Aprendizado SDN/IA para Gestão de TICs.
