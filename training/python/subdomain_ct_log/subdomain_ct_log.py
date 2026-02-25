# Bibliotecas necessárias.
from crtsh import crtshAPI
import json
import argparse
import re

# Help-Menu
parser = argparse.ArgumentParser(
    description= "Extracts domains and subdomains from crt.sh" # Descrição da ferramenta
)

# Receber o domínio
parser.add_argument( 
    "-d", "--domain",
    required=True,
    help="Target domain"
)

# Output do resultado para um ficheiro de texto
parser.add_argument(
    "-o", "--output",
    required=False,
    help="Write output to a txt file instead of stdout"
)

# Verbose
parser.add_argument(
    "-v", "--verbose",
    action="store_true", # Valor booleano
    help="Enable verbose output"

)

args = parser.parse_args()
domain = args.domain
output = args.output
verbose = args.verbose

# Verificar domínio fornecido
domain_pattern = r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
domain_regex = re.compile(domain_pattern, re.IGNORECASE)

# Normalizar input (Permite http://exemplo.com ou exemplo.com)
domain = domain.strip().lower()
domain = domain.removeprefix("http://").removeprefix("https://")
domain = domain.rstrip("/")

# Verbose
def vprint(msg):
    if verbose:
        print(f"[i] {msg}")

if domain_regex.fullmatch(domain):
    vprint(f"Target domain: {domain}")
    # Fazer uma busca com a API e o domínio pretendido.
    vprint(f"Querying crt.sh")
    result = crtshAPI().search(domain)
    if not result:
        print(f"[!] No results returned for {domain}")
        print("[!] crt.sh returned None (possible error or rate limit)")
        exit(1)

    vprint(f"Raw entries received: {len(result)}")
 
    # Lista de domínios/subdomínios
    domain_list = []

    # Percorrer o "common_name" e "name_value"
    for entry in result:
        # Obter o common_name
        common_name = entry.get("common_name")
        
        # Se existir, adicionamos o valor ao array
        if common_name:
            domain_list.append(common_name.strip().lower())

        # Obter o name_value
        name_value = entry.get("name_value")
        
        # Se existir, separamos as quebra de linhas
        if name_value:
            for name in name_value.split("\n"):

                # Adicionar o valor ao array
                domain_list.append(name.strip().lower())

    # Converter a lista num dicionário para retirar os duplicados - Os dicionários não podem ter duplicados, por isso serão automaticamente descartados
    domain_list = list(dict.fromkeys(domain_list))
    vprint(f"Unique domains found: {len(domain_list)}")
    # Mostrar o output
    if args.output:
        # Guardar num ficheiro txt
        with open(f"{output}.txt", "w", encoding="utf-8") as file:
            
            # Percorrer os domínios/subdominios encontrados
            for domain_entry in domain_list:

                
                file.write(domain_entry + "\n") 
        print(f"[+] Output saved to: {output}.txt")
    else:
        for domain_entry in domain_list:     
            if verbose:
                print(f"[+] {domain_entry}")
            else:
                print(domain_entry)
                
    exit(0)
else:
    print(f"[!] Bad domain.")





