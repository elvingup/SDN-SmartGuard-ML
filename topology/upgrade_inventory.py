import yaml

# 1. Carrega o inventário atual (Módulo 2)
# O script busca o arquivo na pasta inventory/ para promover a gestão centralizada
with open('topology/inventory/hosts.yaml', 'r') as f:
    hosts = yaml.safe_load(f)

# 2. Evolução Tática para o Módulo 3
# Percorre os 100 hosts injetando os pontos de coleta de telemetria
for host_name, host_data in hosts.items():
    # Injeta a porta gRPC essencial para Streaming Telemetry
    host_data['data']['telemetry_port'] = 50051
    # Define a função do ativo para os algoritmos de ML
    host_data['data']['role'] = "access"

# 3. Salva o inventário de elite (Sobrescreve com os novos dados)
with open('topology/inventory/hosts.yaml', 'w') as f:
    yaml.dump(hosts, f, default_flow_style=False, sort_keys=False)

print("[+] MISSÃO CUMPRIDA: Inventário evoluído para o Módulo 3 com sucesso!")
