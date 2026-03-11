import yaml
import os

def gerar_forca_tarefa(quantidade=100):
    inventory_dir = 'inventory'
    
    # Garante que a pasta de inventário existe
    if not os.path.exists(inventory_dir):
        os.makedirs(inventory_dir)
        print(f"[*] Pasta '{inventory_dir}' criada com sucesso.")

    hosts = {}

    print(f"[*] Mobilizando {quantidade} switches para o inventário...")

    for i in range(1, quantidade + 1):
        hostname = f"sw-acesso-{i:03d}"  # Gera sw-acesso-001 até sw-acesso-100
        ip_final = i % 254 # Lógica simples para evitar IPs inválidos
        ip_rede = f"192.168.1.{ip_final}"
        
        # Estrutura do Host compatível com Nornir
        hosts[hostname] = {
            "hostname": ip_rede,
            "groups": ["switches_acesso"],
            "data": {
                "interface": "GigabitEthernet0/1",
                "vlan": 10 if i <= 50 else 20, # Divisão tática de VLANs
                "setor": "Financeiro" if i <= 50 else "Operacional"
            }
        }

    # Escrita tática no arquivo YAML
    caminho_arquivo = os.path.join(inventory_dir, 'hosts.yaml')
    with open(caminho_arquivo, 'w') as f:
        yaml.dump(hosts, f, default_flow_style=False, sort_keys=False)

    print(f"[+] MISSÃO CUMPRIDA: {caminho_arquivo} gerado com 100 ativos.")

if __name__ == "__main__":
    gerar_forca_tarefa()
