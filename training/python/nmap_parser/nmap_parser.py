#Receber um ficheiro do tipo xml/texto do nmap
#Ler esse ficheiro
#Organizar os dados por estrutura.
#Dados importantes:
#Host
#Portas abertas
#Serviços dessas portas
#Versão dos serviços

#Biblioteca standard do Python para trabalhar com expressões regulares
import re
#Biblioteca para trabalhar com JSON 
import json
import argparse #Trabalhar com parseres
import xml.etree.ElementTree as ET #trabalhar com xml
import os


#Parser
parser = argparse.ArgumentParser(
    description="Extrai informação relevantede de uma análise nmap" #Descrição da ferramenta
)

#Adicionar o argumento para enviar um ficheiro
parser.add_argument(
    "-f", "--file",
    required=True,
    help="Caminho para o ficheiro a analisar (.txt/.xml)"
)
#Criar o parser
args = parser.parse_args()
#Atribuir o caminho do ficheiro à regra do parser
file_path = args.file


#definir standard correto
ipv4_pattern = r"""
^ # Início de string
( #Abre o grupo do primeiro octecto
  (25[0-5])|           # 250–255 (Começa com 25x e depois vai 250,251,252,253,254,255) 
  (2[0-4][0-9])|       # 200–249 (Começa com 2xx e depois vai a 21x, 22x, 23x e 24x, depois em cada caso, vai de 0 a 9)
  (1[0-9]{2})|         # 100–199 (começa com 1xx e depois vai a 10x, 11x, 12x, 13x, 14x, 15x, 16x, 17x, 18x, 19x, depois em cada caso vai de 0 a 9)
  ([1-9]?[0-9])
) #Fecha o grupo do segundo octecto
(\. #Ponto literal . o \ é para escapar.
( # Início do segundo octeto, mesma lógica
  (25[0-5])| 
  (2[0-4][0-9])|
  (1[0-9]{2})|
  ([1-9]?[0-9])
)){3} # Repete-se 3 vezes para ficar ao tudo 4 octetos
$ #Fim da string
"""
#Compilar o regex
ipv4_regex = re.compile(ipv4_pattern, re.VERBOSE)
#Regex de serviços
service_pattern = r"^(\d+)\/(tcp|udp)\s+open\s+(\S+)\s*(.*)$"
service_regex = re.compile(service_pattern, re.VERBOSE)

#Guardar a extensão do ficheiro
ext = os.path.splitext(file_path)[1].lower()

#Array dos resultados finais
resultados = {}

#Se for texto = .txt
def parse_text(file_path):
    current_ip = None

    #Importar o ficheiro
    with open(file_path, "r", encoding="utf-8") as ficheiro:
        #Percorrer cada linha
        for linha in ficheiro:
            linha.strip()
            
            #Se uma linha começar com 'Nmap scan report for...' a última palavra é um IP
            if linha.startswith("Nmap scan report for"):
                ip = linha.split()[-1]
                
                #Verificar se o IP existe
                if ipv4_regex.fullmatch(ip):
                    current_ip = ip
                    resultados[current_ip] = []
                continue
            
            #Verificar se existem serviços
            match = service_regex.match(linha)
            if match and current_ip:
                port = int(match.group(1)) #Porta
                protocol = match.group(2) #Protocolo
                service = match.group(3) #Serviço
                version = match.group(4).strip() #Versão

                #Guardar os resultados
                resultados[current_ip].append(
                    {
                        "port": port,
                        "protocol": protocol,
                        "service": service,
                        "version": version
                    }
                )

        return resultados


#Caso o ficheiro seja xml (.xml)
def parse_xml(file_path):
    #Guardar a árvore
    tree = ET.parse(file_path)
    #Selecionar a raíz da árvore
    root = tree.getroot()

    #Procurar o endereço do host
    for host in root.findall("host"):
        addr = host.find("address")

        #Se não encontrar, passar à frente
        if addr is None:
            continue

        #Guardar o endereço
        ip = addr.get("addr")
        resultados[ip] = []

        #Guardar as portas
        ports = host.find("ports")
        if ports is None:
            continue

        #Percorrer as portas encontradas
        for port in ports.findall("port"):
            #Procurar o state
            state = port.find("state")
            #Se tiverem fechadas ou não existirem, seguimos em frente
            if state is None or state.get("state") != "open":
                continue

            #Encontrar o nome do serviço
            service = port.find("service")

            #Guardar tudo nos resultados
            resultados[ip].append({
                "port": int(port.get("portid")),
                "protocol": port.get("protocol"),
                "service": service.get("name") if service is not None else "",
                "version": f"{service.get('product','')} {service.get('version','')}".strip() if service is not None else ""
            })

            #Devolver os resultados
            return resultados

#Selecionar o fluxo do texto
if ext == ".txt":
    resultados = parse_text(file_path)

#Selecionar o fluxo dos xmls
elif ext == ".xml":
    resultados = parse_xml(file_path)

#Formato inválido
else:
    print("Formato não suportado")
    exit(1)

#Guardar resultados
with open("nmap_resultados.json", "w", encoding="utf-8") as ficheiro:
        json.dump(resultados, ficheiro, indent=4, ensure_ascii=False)