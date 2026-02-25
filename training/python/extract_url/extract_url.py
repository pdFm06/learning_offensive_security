#Importar bibliotecas necessárias
import re #Trabalhar com Regex
import argparse #Trabalhar com parseres
from urllib.parse import urlparse #Trabalhar com a formatação e validação de URLs

#Parser
parser = argparse.ArgumentParser(
    description="Extrai URLs válidas de um ficheiro de texto." #Descrição da ferramenta
)

#Adicionar o argumento para enviar um ficheiro
parser.add_argument(
    "-f", "--file",
    required=True,
    help="Caminho para o ficheiro a analisar"
)
#Criar o parser
args = parser.parse_args()
#Atribuir o caminho do ficheiro à regra do parser
file_path = args.file

#Padrão utilizado para identificar a URL
url_pattern = r"""
https?://                # http ou https
(?:[a-zA-Z0-9.-]+|\d{1,3}(?:\.\d{1,3}){3})  # domínio ou IPv4 simples
(?::\d+)?                # porto opcional
(?:/[^\s"']*)?          # path opcional
"""
url_regex = re.compile(url_pattern, re.VERBOSE)
url_validos = []

#Padrão utilizado para identificar o IPv4
ipv4_pattern = r"""
^
((25[0-5])|(2[0-4][0-9])|(1[0-9]{2})|([1-9]?[0-9]))
(\.
((25[0-5])|(2[0-4][0-9])|(1[0-9]{2})|([1-9]?[0-9]))
){3}
$
"""
ipv4_regex = re.compile(ipv4_pattern, re.VERBOSE)

#Padrão utilizado para identificar o domínio
domain_pattern = r"""
^
(?!-)
([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+
[a-zA-Z]{2,}
$
"""
domain_regex = re.compile(domain_pattern, re.VERBOSE)

#Abrir ficheiro fornecido pelo parcer
with open(file_path, "r", encoding="utf-8") as ficheiro:
    #Percorrer todas as linhas do ficheiro
    for linha in ficheiro:
        
        #Colocar cada url num espaço de array
        entradas = linha.strip().split()

        #Percorrer cada elemento (URL) de cada linha (array)
        for entrada in entradas:
            if not entrada: #Se não haver palavra, continuar
                continue

            #Verificar se o domínio é válido
            match = url_regex.fullmatch(entrada)

            #Se o domínio for válido
            if match:
                parsed = urlparse(entrada) #Divide a URL em partes: schema, netloc, path, etc...
                host = parsed.hostname #Tira apenas o host: domínio ou IPv4

                #Validar o domínio ou o IPv4
                if ipv4_regex.fullmatch(host) or domain_regex.fullmatch(host):
                    #Adicionar os URLs válidos a uma noval ista
                    url_validos.append(entrada)

#Escrever os domínios válidos num ficheiro final_urls.txt
with open("final_urls.txt", 'w', encoding='utf-8') as ficheiro:
    for dominio in url_validos:
        ficheiro.write(dominio + '\n')

