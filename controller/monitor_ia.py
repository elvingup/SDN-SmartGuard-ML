import time
import pandas as pd
from nornir import InitNornir
from sklearn.linear_model import LinearRegression
# ... outras importações (nornir_scrapli, etc)

# Inicialização do Nornir
nr = InitNornir(config_file="topology/config.yaml")

# --- FUNÇÃO 1: O COLETOR (Já existente no seu informe) ---
def coletar_telemetria_grpc(task):
    """
    Tarefa para extrair métricas de bytes_sent e bytes_recv.
    Justificativa: Usamos gRPC (Porta 50051) para baixa latência e 
    formato binário eficiente (Protocol Buffers).
    """
    # Em um cenário real de SDN, usaríamos bibliotecas como PyGNMI
    # Aqui, simulamos a requisição de contadores de interface
    comando = "show interfaces telemetry statistics" 
    
    # Execução do comando via Scrapli (alta performance)
    resultado = task.run(task=send_command, command=comando)
    
    # O Parser converte o output bruto em dados estruturados para a IA
    # Meta: Extrair bytes_sent e bytes_recv
    return resultado.scrapli_response.genie_parse_output()

# --- FUNÇÃO 2: O ANALISTA (A implementação técnica de ML) ---
def treinar_modelo_preditivo(historico_dados):
    """
    Justificativa: Esta função aplica a equação y = b0 + b1*x + e.
    Ela transforma o histórico em uma linha de tendência.
    """
    df = pd.DataFrame(historico_dados)
    if len(df) < 5: return None # Precisamos de massa crítica para treinar
    
    X = df[['timestamp']].values.reshape(-1, 1)
    y = df['utilizacao'].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo

# --- FUNÇÃO 3: O MAESTRO (Sua pipeline_ia evoluída) ---
def pipeline_ia():
    print("[*] Iniciando Cérebro SDN - Módulo 3")
    historico_global = [] # Buffer para armazenar os 'x' e 'y'
    
    try:
        while True:
            # AÇÃO 1: Coleta simultânea nos 100 ativos
            resultados = nr.run(task=coletar_telemetria_grpc)
            
            # AÇÃO 2: Processamento e Armazenamento
            agora = time.time()
            for host, res in resultados.items():
                # Simulando a extração do valor de utilização do link
                valor_utilizacao = 45 # Exemplo vindo do seu parser
                historico_global.append({
                    'timestamp': agora, 
                    'utilizacao': valor_utilizacao,
                    'host': host
                })
            
            # AÇÃO 3: O Salto de Inteligência (Treinamento)
            if len(historico_global) > 10:
                modelo = treinar_modelo_preditivo(historico_global)
                if modelo:
                    # PREVISÃO: Onde estaremos daqui a 300 segundos (5 min)?
                    futuro = np.array([[agora + 300]])
                    predicao = modelo.predict(futuro)[0]
                    
                    print(f"[!] TENDÊNCIA: Utilização prevista em 5 min: {predicao:.2f}%")
                    
                    # LOGICA SDN: Se predicao > 80%, disparar alerta ou reencaminhar tráfego
                    if predicao > 80:
                        print("[ALERTA] Saturação iminente detectada! Reduzindo custos via gestão proativa.")

            time.sleep(5) # Meta de intervalo de 5 segundos
            
    except KeyboardInterrupt:
        print("[*] Encerrando operações...")

if __name__ == "__main__":
    pipeline_ia()
