# Objetivo do script: integrar num só comando 4 ferramentas/analises de uma webapp.
# 1º - Nmap NSE
# 2º - Vhost enum
# 3º - Dirbusting
# 4º - WhatWeb

# 1º Passo: Receber um IP ou domínio e verificar se ele é válido
# Estou a pensar em usar Regex para isto
# Após falar com o Chat, seria ideal usar Regex para domínios e a bilbioteca ipaddress para o ip.

# Bibliotecas necessárias
import ipaddress
import re
import socket

target = input("Target: ")
target.strip()
target_type = None

domain_pattern = r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$" 
domain_regex = re.compile(domain_pattern, re.IGNORECASE)

def is_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False


# Verificar se é um IP ou se é um domínio
if is_ip(target):
    target_type = "IP"

elif domain_regex.fullmatch(target):
    target_type = "Domain"

else:
    raise ValueError("Invalid target")

def resolve_domain_to_ips(host: str) -> list[str]: # host: str -> list[str] são type hints: neste caso, esperamos receber uma string e devolver uma lista de strings
    infos = socket.getaddrinfo(host, None) # Resolve o nome do domínio com nenhuma porta especificada e devolve uma lista de registos com informações da rede, nomeadamente: family, socktype, protocol, cannonname, sockaddr

    unique_ips = set() #Criar um set. Um set não tem duplicados e não garante ordem
    for family, socktype, proto, canonname, sockaddr in infos:
        ip = sockaddr[0] # O sockaddr tem o ip[0] e a porta[0]. Só queremos o IP.
        unique_ips.add(ip)

    return sorted(unique_ips)

if target_type == "Domain":
    ips = resolve_domain_to_ips(target)
    print(ips)

