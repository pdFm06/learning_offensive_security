### loot Organizer ###
## Objetivo ##
# Este script tem como objetivo, receber como input uma pasta e organizar os ficheiros em categorias #
# Exemplo: vamos supor que estamos a fazer um exame, e já recolhemos dezenas de ficheiros, quer sejam de dump ou ficheiros transferidos do
# utilizador e queremos organizá-los por categorias (loot, scans, hashes, tickets), podemos correr o script e apontar para essa pasta.
# Até agora será esse o objetivo.

## Implementação ##
# 1º Passo - receber o diretório.
# 2º Passo - ler os ficheiros contidos no diretório e categorizá-los.
# 3º Passo - criar os subdiretórios/diretórios necessários para organizar os ficheiros encontrados
# 4º Passo - mover os ficheiros para lá.

### Código ###
# Bibliotecas necessárias
from pathlib import Path
import argparse
import logging

# Dump extensions
dump_ext = [".sql", ".db", ".sqlite", ".csv"]

# Scan extensions
scan_ext = [".nmap", ".xml", ".gnmap", ".masscan"]

# Script extensions
script_ext = [".py", ".js", ".rb", ".vbs", ".sh"]

# Config extensions
config_ext = [
    ".ini",
    ".conf",
    ".cfg",
    ".json",
    ".yaml",
    ".yml",
    ".env",
    ".properties",
    ".xml",
    ".config"
]

# Key extensions
key_ext = [
    ".pem",
    ".key",
    ".pfx",
    ".p12",
    ".crt",
    ".cer",
    ".der"
]

# SSH
SSH_PATTERNS = [
    "-----begin openssh private key-----",
    "-----begin rsa private key-----",
    "ssh-rsa",
    "ssh-ed25519"
]

# Key patterns
KEY_PATTERNS = [
    "-----begin rsa private key-----",
    "-----begin openssh private key-----",
    "-----begin private key-----",
    "-----begin ec private key-----",
    "-----begin dsa private key-----",
    "-----begin certificate-----",
    "-----begin encrypted private key-----",
    "-----begin pgp private key block-----"
]

config_keywords_strong = [
    "password",
    "pass",
    "pwd",
    "token",
    "secret",
    "apikey",
    "api_key"
]

config_keywords_weak = [
    "user",
    "username",
    "login"
]

# Logging

def get_files(path=None, recursive=False):
    # Receber o diretório e listar os ficheiros dentro dele.
    
    if path is None:
        dir_list = Path.cwd()
    else:
        dir_list = Path(path)
    
    files = []

    if dir_list.exists() and dir_list.is_dir():

        if recursive:
            iterator = dir_list.rglob("*")
        else:
            iterator = dir_list.iterdir()

        logging.debug(f"Scanning directory: {dir_list}")

        # Filtrar se é um diretório ou se é um ficheiro
        for item in iterator:
            if item.is_file():
                files.append(item)

        logging.debug(f"Found {len(files)} files")

        return files
    else:
        raise FileNotFoundError(f"{path} does not exist")
    
def classify_files(files):
    plan = {
        "Keys": [],
        "SSH": [],
        "Credentials": [],
        "Hashes": [],
        "Dumps": [],
        "Notes": [],
        "Scans": [],
        "Scripts": [],
        "Configs": [],
        "CredConfig": []
    }

    for file in files:
        logging.debug(f"Checking file {file.name}")

        ext = file.suffix.lower()

        # --- EXTENSÕES FORTES ---
        if ext in scan_ext:
            plan["Scans"].append(file)
            continue

        if ext in script_ext:
            plan["Scripts"].append(file)
            continue

        if ext in dump_ext:
            plan["Dumps"].append(file)
            continue

        if ext in key_ext:
            plan["Keys"].append(file)
            continue

        # --- FLAGS ---
        found_ssh = False
        found_key = False
        found_hash = False
        found_credential = False
        found_config_cred = False

        try:
            with file.open(errors="ignore") as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        break

                    line = line.strip().lower()

                    # --- SSH ---
                    if any(line.startswith(p) for p in SSH_PATTERNS):
                        found_ssh = True
                        break

                    # --- KEYS ---
                    if any(line.startswith(p) for p in KEY_PATTERNS):
                        found_key = True
                        break

                    # --- HASH ---
                    clean = line.replace(" ", "")
                    hex_chars = "0123456789abcdef"

                    is_hex = (
                        clean and len(clean) >= 32
                        and all(c in hex_chars for c in clean)
                        and clean.isalnum()
                    )

                    many_colons = (
                        line.count(":") >= 2
                        and " " not in line
                        and "/" not in line
                    )

                    if "$" in line or many_colons or is_hex:
                        found_hash = True
                        break

                    # --- CONFIG CRED (YAML + ENV) ---
                    if not line.startswith(("#", "//", ";")):

                        # YAML: password: value
                        if ":" in line:
                            key = line.split(":", 1)[0].strip()
                            if key in config_keywords_strong:
                                found_config_cred = True

                        # ENV: password=value
                        if any(f"{k}=" in line for k in config_keywords_strong):
                            found_config_cred = True

                        # weak
                        if any(line.startswith(f"{k}=") for k in config_keywords_weak):
                            if len(line) < 50:
                                found_config_cred = True

                    # --- CREDENTIAL ---
                    if (
                        line.count(":") == 1
                        and "=" not in line
                        and not line.startswith(("http", "#", "-----"))
                    ):
                        found_credential = True

        except Exception:
            continue

        # --- PRIORIDADE FINAL ---
        if found_ssh:
            plan["SSH"].append(file)
        elif found_key:
            plan["Keys"].append(file)
        elif found_hash:
            plan["Hashes"].append(file)
        elif found_config_cred:
            plan["CredConfig"].append(file)
        elif found_credential:
            plan["Credentials"].append(file)
        elif ext in config_ext:
            plan["Configs"].append(file)
        elif ext in [".txt", ".log"]:
            plan["Notes"].append(file)

    return plan

def create_directories(plan, dry_run):
    #Verificar que categorias é que existem
    for categoria, value in plan.items():
        if value:
            if dry_run:
                logging.info(f"Would create directory: {categoria}")
            else:
                logging.info(f"Creating directory {categoria}...")
                Path(categoria).mkdir(exist_ok=True)

def move_files(plan, dry_run):
    for categoria, value in plan.items():
        dest_dir = Path(categoria)
        
        for file in value:
            destination = dest_dir / file.name
            if destination.exists():
                number = 1

                while True:
                    new_destination = dest_dir / f"{file.stem}_{number}{file.suffix}"
                    
                    if not new_destination.exists():
                        destination = new_destination
                        break

                    number += 1
            if dry_run:
                logging.info(f"Would move {file.name} -> {destination}")
            else:
                dest_dir.mkdir(exist_ok=True)
                logging.info(f"Moving {file.name} -> {destination}")
                file.rename(destination)

def print_summary(plan):

    total = 0
    print("===== Loot Summary =====")
    for categoria, value in plan.items():
        print(f"{categoria}: {len(value)} files")
        total = total + len(value)
    
    print("\n")
    print(f"Total: {total} files")


def main():

    # Parser
    parser = argparse.ArgumentParser()

    parser.add_argument("path", nargs="?", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--recursive", action="store_true")

    args = parser.parse_args()
    level = None

    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )

    files = get_files(args.path, args.recursive)
    plan = classify_files(files)
    create_directories(plan, args.dry_run)
    move_files(plan, args.dry_run)
    print_summary(plan)

if __name__ == "__main__":
    main()