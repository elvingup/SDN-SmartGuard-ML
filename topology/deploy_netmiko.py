import os  # Biblioteca necessária para interagir com o Sistema Operacional
import json
from netmiko import ConnectHandler

# 1. Carregamos a "Intenção" de rede do nosso arquivo JSON
def carregar_dados():
    with open('switches.json', 'r') as f:
        return json.load(f)

def executar_autonomo():
    
    # Coletando as credenciais do sistema operacional
    # O segundo argumento é um valor padrão caso a variável não exista
    usuario_env = os.getenv('NET_USER', 'usuario_padrao')
    senha_env = os.getenv('NET_PASS')

    if not senha_env:
        print("ERRO CRÍTICO: Variável NET_PASS não definida no sistema!")
        return
    
    dados = carregar_dados()
    
    print("--- INICIANDO PROTOCOLO DE CONECTIVIDADE DE ELITE ---")

    for sw in dados['switches']:
        # Definimos os parâmetros técnicos do ativo
        dispositivo = {
            'device_type': 'cisco_ios',  # Tipo de OS do switch (ajustável)
            'host': sw['ip'],
            'username': usuario_env,     # Mapeamento dinâmico
            'password': senha_env,       # Mapeamento dinâmico
            'port': 22,                  # Porta SSH padrão
        }

        try:
            print(f"[*] Tentando conexão SSH com {sw['hostname']} ({sw['ip']})...")
            
            # 2. O Netmiko realiza o Handshake SSH automaticamente
            with ConnectHandler(**dispositivo) as net_connect:
                print(f"[+] Conectado com sucesso ao {sw['hostname']}!")

                # 3. Preparando o conjunto de comandos gerados pelo nosso parser
                config_commands = [
                    f"interface {sw['interface']}",
                    f"description {sw['description']}",
                    f"switchport access vlan {sw['vlan']}",
                    "no shutdown"
                ]

                # 4. Enviando as configurações (Modo Global Config)
                output = net_connect.send_config_set(config_commands)
                print(f"[RECORDE DE EXECUÇÃO]:\n{output}")
                
                # 5. Persistência de dados (Salvando na NVRAM)
                net_connect.send_command("write memory")
                print(f"[!] Configuração salva em {sw['hostname']}.\n")

        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha ao gerir {sw['hostname']}: {e}")

if __name__ == "__main__":
    executar_autonomo()
