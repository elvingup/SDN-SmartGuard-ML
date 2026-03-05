import json

# Função para gerar comandos CLI a partir dos dados JSON
def gerar_configuracoes(arquivo_json):
    try:
        # 1. Abre o arquivo e carrega os dados
        with open(arquivo_json, 'r') as f:
            dados = json.load(f)
        
        print(f"Iniciando geração de scripts para {len(dados['switches'])} ativos...\n")

        # 2. Itera sobre a lista de switches
        for sw in dados['switches']:
            print(f"--- Gerando comandos para: {sw['hostname']} ({sw['ip']}) ---")
            
            # 3. Construção da String de Comando (Template)
            config_script = (
                f"configure terminal\n"
                f" interface {sw['interface']}\n"
                f"  description {sw['description']}\n"
                f"  switchport access vlan {sw['vlan']}\n"
                f"  switchport mode access\n"
                f"  no shutdown\n"
                f"exit\n"
                f"write memory\n"
            )
            
            print(config_script)
            print("-" * 40)

    except FileNotFoundError:
        print("Erro: Arquivo JSON não encontrado!")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Executa a função que DEFINE A INTENÇÃO, visto que o argumento é um arquivo que representa três switches que precisam de atualizações de VLAN em portas específicas.

if __name__ == "__main__":
    gerar_configuracoes('switches.json')
