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

# SSH
SSH_PATTERNS = [
    "-----begin openssh private key-----",
    "-----begin rsa private key-----",
    "ssh-rsa",
    "ssh-ed25519"
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
    # Categorias
    plan = {
        "Keys": [],
        "Credentials": [],
        "Hashes": [],
        "Dumps": [],
        "Notes": [],
        "Scans": [],
        "Scripts": []
    }


    for file in files:
        logging.debug(f"Checking file {file.name}")
        ssh_key = False
        credential_found = False
        hash_found = False

        with file.open(errors="ignore") as f:
            counter = 0

            for line in f:
                line = line.strip().lower()

                #Deteção de hashes
                has_dollar = "$" in line
                many_colons = line.count(":") >= 2
                
                clean_line = line.replace(" ", "")
                hex_chars = "0123456789abcdef"
                is_hex = clean_line and all(c in hex_chars for c in clean_line)
                long_enough = len(clean_line) >= 32
                hex_hash = is_hex and long_enough

                is_hash = has_dollar or many_colons or hex_hash

                #Deteção de credenciais
                one_colon = line.count(":") == 1

                not_http = not line.startswith("http")
                not_comment = not line.startswith("#")
                not_key = not line.startswith("-----")

                is_credential = one_colon and not_http and not_comment and not_key

                if any(line.startswith(pattern) for pattern in SSH_PATTERNS):
                    ssh_key = True
                    logging.debug(f"{file.name}: SSH pattern detected")
                    break

                if is_hash:
                    hash_found = True
                    logging.debug(f"{file.name}: Hash pattern detected")
                    break
                
                if is_credential:
                    credential_found = True
                    logging.debug(f"{file.name}: credential pattern detected")
                    break

                counter += 1
                if counter >= 10:
                    break

        if ssh_key:
            plan["Keys"].append(file)
            logging.debug(f"{file.name}: classified as Keys")
            continue

        if hash_found:
            plan["Hashes"].append(file)
            logging.debug(f"{file.name}: classified as Hashes")
            continue
        
        if credential_found:
            plan["Credentials"].append(file)
            logging.debug(f"{file.name}: classified as Credentials")
            continue

        ext = file.suffix.lower()
        logging.debug(f"{file.name}: extension {ext}")
        
        if ext in dump_ext:
            plan["Dumps"].append(file)
            logging.debug(f"{file.name}: classified as Dumps")
        elif ext == ".txt":
            plan["Notes"].append(file)
            logging.debug(f"{file.name}: classified as Notes")
        elif ext == ".nmap":
            plan["Scans"].append(file)
            logging.debug(f"{file.name}: classified as Scans")
        elif ext == ".py":
            plan["Scripts"].append(file)
            logging.debug(f"{file.name}: classified as Scripts")
        else:
            logging.debug(f"{file.name}: no category matched")
        
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