# Objetivos do script:
# Receber um par de credenciais - username/password, username/hash, etc.
# Receber os serviços disponíveis.
# Sugerir comandos para testar o par de credenciais fornecedio nos serviços selecionados

# Plano:
# Receber um par de credenciais
# Receber uma lista/sequência dos serviços
# Gerar os comandos

### Receber o par de credenciais ###
## Inicializar o parser ##
import argparse
import re

parser = argparse.ArgumentParser(
    description="Gera comandos para testar um par de crendeciais num determinado número de serviços"
)

parser.add_argument(
    "-i", "--target",
    required=True,
    help="Target's IP or domain"
)

parser.add_argument(
    "-u", "--username",
    required=True,
    help="username"
)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--password", help="Plaintext password")
group.add_argument("--hash", help="Password hash")

parser.add_argument(
    "--protocols",
    nargs="+",
    choices=["ssh", "ftp", "smb", "rdp", "winrm"]
)

args = parser.parse_args()
target = args.target
username = args.username
password = args.password
hash = args.hash
protocols = args.protocols

### Validar Target ###
## Validar IP ##
regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

def check(target):
    if(re.search(regex, target)):
        return True
    else:
        return False
    
## Validar Domain ##
def is_valid_domain(target):
    pattern = r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
    domain_regex = re.compile(pattern, re.IGNORECASE)

    if re.fullmatch(domain_regex, target) is None:
        return False
    else:
        return True

if check(target) or is_valid_domain(target):

    # fazer o dicionário
    
    # Percorrer os protocolos selecionados
    selected_protocols = []

else:
    print("Alvo inválido!")
    exit()


