import time
import numpy as np
import pandas as pd
from nornir import InitNornir
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# Adicionadas as dependências do Prometheus para o Módulo 4
from prometheus_client import start_http_server, Gauge

# =================================================================
# PROJETO: SDN-SmartGuard-ML
# COMPONENTE: Cérebro do Controlador (monitor_ia.py)
# OBJETIVO: Automatizar a gestão de TICs e reduzir custos via IA
# =================================================================

# --- DEFINIÇÃO DE MÉTRICAS (PROMETHEUS) ---
# Gauge: Métrica que pode subir e descer (ideal para utilização e predição)
UTILIZACAO_ATUAL = Gauge('sdn_utilizacao_link_percent', 'Utilização atual do link em %', ['host'])
PREDICAO_SATURACAO = Gauge('sdn_predicao_saturacao_5min', 'Predição de saturação para os próximos 5 min', ['host'])
STATUS_ANOMALIA = Gauge('sdn_anomalia_ddos_status', 'Status de anomalia (0=Normal, 1=Ataque)', ['host'])

# Inicialização do Nornir (O Orquestrador)
# Justificativa: Permite interrogar os 100 switches simultaneamente utilizando o inventário.
nr = InitNornir(config_file="topology/config.yaml")

# --- FUNÇÃO 1: COLETOR DE TELEMETRIA (STREAMING TELEMETRY) ---
def coletar_telemetria_grpc(task):
    """
    Objetivo: Extrair dados de performance via gRPC.
    Justificativa: Diferente do SNMP, o streaming fornece dados em tempo 
    real necessários para que o modelo de ML tenha alta precisão.
    """
    # Aqui entraria a lógica de conexão gRPC utilizando a telemetria_port (50051)
    # Por fins de instrução, simulamos o retorno de bytes e pacotes
    host_name = task.host.name
    utilizacao_link = np.random.uniform(10, 95) # Simulação de carga (%)
    pps = np.random.randint(50, 1000)           # Pacotes por segundo
    ips_unicos = np.random.randint(1, 50)       # IPs de origem
    
    return {
        "host": host_name,
        "utilizacao": utilizacao_link,
        "pps": pps,
        "ips_unicos": ips_unicos
    }

# --- FUNÇÃO 2: MODELO PREDITIVO (REGRESSÃO LINEAR) ---
def treinar_modelo_preditivo(historico_dados):
    """
    Equação: y = beta_0 + beta_1*x + epsilon
    Justificativa: Prever a saturação ANTES que ela ocorra permite 
    o reencaminhamento de tráfego proativo, evitando paradas de rede.
    """
    df = pd.DataFrame(historico_dados)
    if len(df) < 10: 
        return None # Aguarda massa crítica de dados
    
    # Feature: Tempo (x) | Target: Utilização (y)
    X = df[['timestamp']].values.reshape(-1, 1)
    y = df['utilizacao'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    return modelo

# --- FUNÇÃO 3: DETECÇÃO DE ANOMALIAS (K-MEANS CLUSTERING) ---
def detectar_anomalias_ddos(dados_trafego):
    """
    Objetivo: Identificar ataques DDoS ou comportamentos fora do padrão.
    Justificativa: Aprendizado não supervisionado detecta ataques que
    não possuem assinaturas conhecidas (Zero-day).
    """
    if len(dados_trafego) < 5:
        return None, None

    # Normalização: Essencial para algoritmos baseados em distância euclidiana
    scaler = StandardScaler()
    dados_norm = scaler.fit_transform(dados_trafego[['pps', 'ips_unicos']])
    
    # K=2 (0: Normal, 1: Anomalia/DDoS)
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(dados_norm)
    
    return clusters, kmeans

# --- FUNÇÃO 4: O MAESTRO (PIPELINE_IA) ---
def pipeline_ia():
    print(f"{'='*50}\n INICIANDO CÉREBRO SDN - OPERAÇÃO SENTINELA E VISIBILIDADE\n{'='*50}")
    
    # Inicia o servidor de métricas na porta 8000
    start_http_server(8000)
    print("[+] Servidor de métricas Prometheus ativo na porta 8000")
    
    historico_global = []
    
    try:
        while True:
            # 1. Coleta Paralela em 100 ativos via Nornir
            resultados = nr.run(task=coletar_telemetria_grpc)
            agora = time.time()
            dados_rodada = []
            
            for host, response in resultados.items():
                info = response.result
                info['timestamp'] = agora
                historico_global.append(info)
                dados_rodada.append(info)
                
                # ATUALIZANDO MÉTRICAS NO EXPORTER (Utilização Atual)
                UTILIZACAO_ATUAL.labels(host=host).set(info['utilizacao'])
            
            # Manter buffer de histórico (últimas 100 amostras)
            if len(historico_global) > 100:
                historico_global.pop(0)

            # 2. Análise Preditiva (Olhando para o Futuro)
            modelo_reg = treinar_modelo_preditivo(historico_global)
            if modelo_reg:
                # Previsão para daqui a 5 minutos (300s)
                futuro = np.array([[agora + 300]])
                predicao = modelo_reg.predict(futuro)[0]
                print(f"[PREDIÇÃO] Saturação estimada em 5 min: {predicao:.2f}%")
                
                # ATUALIZANDO PREDIÇÃO NO EXPORTER (Usamos 'global' pois a predição atual engloba o link como um todo)
                PREDICAO_SATURACAO.labels(host='global').set(predicao)
                
                if predicao > 85:
                    print("ALERTA: Risco de saturação iminente! Iniciando SDN Traffic Engineering.")

            # 3. Detecção de Anomalias (Olhando para o Presente)
            df_rodada = pd.DataFrame(dados_rodada)
            clusters, _ = detectar_anomalias_ddos(df_rodada)
            
            if clusters is not None:
                for idx, cluster_id in enumerate(clusters):
                    host_atual = df_rodada.iloc[idx]['host']
                    
                    # ATUALIZANDO STATUS DE ANOMALIA NO EXPORTER
                    STATUS_ANOMALIA.labels(host=host_atual).set(cluster_id)
                    
                    if cluster_id == 1: # Suposto comportamento anômalo
                        print(f"CRÍTICO: Anomalia detectada no host {host_atual}!")

            print(f"[*] Ciclo concluído. Aguardando nova telemetria...\n")
            time.sleep(5) # Intervalo de coleta

    except KeyboardInterrupt:
        print("\n[!] Encerrando controlador SDN. Operação desmobilizada.")

if __name__ == "__main__":
    pipeline_ia()
