import time
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result

# 1. Inicialização do Cérebro (Nornir)
# Justificativa: O Nornir utiliza Threads para gerenciar 100 ativos 
# sem travar a execução do script principal.
nr = InitNornir(config_file="topology/config.yaml")

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

def pipeline_ia():
    print("[*] Iniciando Duto de Telemetria - Frequência: 5s")
    try:
        while True:
            # 2. Execução Paralela em 100 Switches
            # Justificativa: Redução de OPEX ao centralizar a coleta.
            stats = nr.run(task=coletar_telemetria_grpc)
            
            # 3. Preparação dos Dados para Regressão Linear
            # Aqui os dados de 'bytes' tornam-se o nosso 'x' na equação.
            for host, result in stats.items():
                # Lógica de extração de métricas específicas
                # bytes_sent = result.result['GigabitEthernet0/1']['tx_bytes']
                # bytes_recv = result.result['GigabitEthernet0/1']['rx_bytes']
                pass
            
            print(f"[+] Ciclo de telemetria concluído para {len(stats)} ativos.")
            
            # 4. Meta de Intervalo: 5 segundos
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n[*] Desativando duto de telemetria...")

if __name__ == "__main__":
    pipeline_ia()
