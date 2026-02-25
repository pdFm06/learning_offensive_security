# Psedocódigo
# 1º Vamos receber um ficheiro de output da pasta inputs
# 2º Vamos identificar o tipo de output: Nmap, hashcat, netexec, etc.
# 3º Vamos definir o que é 'útil' e o que é 'lixo'
# 4º Vamos percorrer o conteúdo do ficheiro e categorizar cada linha em relação às categorias definidas
# 5º Guardar o Output na pasta Outputs

# Como primeira versão, vou só trabalhar com ficheiros do Nmap.

# O que é importante de recolher
# - IP/Domain

# Bibliotecas necessárias
import re
import json
import argparse

# Parser
parser = argparse.ArgumentParser(
    description="Cleans Nmap output"
)
# Receber/Abrir o ficheiro
parser.add_argument(
    "-f", "--file",
    required=True,
    help="Nmap output file"
)

# Inicializar parser 
args = parser.parse_args()
input_file = args.file

# Obter o nome do ficheiro
location = input_file.split("\\")
file = location[-1]
file = file.split(".")
file_name = file[0]

with open(f"{input_file}") as f:

    hosts = {}
    current_host = None
    reading_ports = False

    states = ['open', 'closed', 'filtered', 'unfiltered']

    for line in f:
        line = line.rstrip()
        # Selecionar a linha com o IP/Domain
        if line.startswith("Nmap scan report for"):
            host_actual = line.replace("Nmap scan report for ", "")
            hosts[host_actual] = []
            a_ler_portas = False
            continue
            #print(host)

        if line.startswith("PORT"):
            reading_ports = True
            continue

        if reading_ports:
            # fim da tabela
            if not line or line.startswith("|") or line.startswith("MAC Address"):
                a_ler_portas = False
                continue

            words = line.split()

            # validar que é linha de serviço
            if len(words) >= 3 and words[1] in states:

                hosts[host_actual].append({
                    "Port": words[0],
                    "State": words[1],
                    "Service": words[2],
                    "Version": ' '.join(words[3:])
                })

    hosts = {h: s for h, s in hosts.items() if s}

with open(f"outputs/{file_name}.json", "w") as jf:
    json.dump(hosts, jf, indent=4)