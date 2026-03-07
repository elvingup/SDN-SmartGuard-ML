from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializa o Nornir com os arquivos de inventário
nr = InitNornir(config_file="config.yaml")

def configurar_rede_em_massa(task):
    # O Nornir injeta automaticamente os dados do host aqui
    vlan_id = task.host['vlan']
    
    comandos = [
        f"interface GigabitEthernet0/1",
        f"description Gerido por SDN-SmartGuard-ML",
        f"switchport access vlan {vlan_id}",
        "no shutdown"
    ]
    
    # Executa via Netmiko, mas de forma paralela!
    task.run(task=netmiko_send_config, config_commands=comandos)

# Disparo em massa
print("--- DISPARANDO ORQUESTRAÇÃO EM PARALELO ---")
result = nr.run(task=configurar_rede_em_massa)
print_result(result)
