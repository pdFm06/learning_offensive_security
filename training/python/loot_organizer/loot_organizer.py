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

# Dump extensions
dump_ext = [".sql", ".db", ".sqlite", ".csv"]

# SSH
SSH_PATTERNS = [
    "-----begin openssh private key-----",
    "-----begin rsa private key-----",
    "ssh-rsa",
    "ssh-ed25519"
]


def get_files(path=None):
    # Receber o diretório e listar os ficheiros dentro dele.
    
    if path is None:
        dir_list = Path.cwd()
    else:
        dir_list = Path(path)
    
    files = []

    if dir_list.exists() and dir_list.is_dir():

        # Filtrar se é um diretório ou se é um ficheiro
        for item in dir_list.iterdir():
            if item.is_file():
                files.append(item)

        return files
    else:
        raise FileNotFoundError(f"{path} does not exist")
    
def classify_files(files, dry_run):
    # Categorias
    plan = {
        "Keys": [],
        "Credentials": [],
        "Hashes": [],
        "Dumps": [],
        "Notes": []
    }


    for file in files:
        ssh_key = False
        credential_found = False

        with file.open(errors="ignore") as f:
            counter = 0

            for line in f:
                line = line.strip().lower()
            
                if any(line.startswith(pattern) for pattern in SSH_PATTERNS):
                    ssh_key = True
                    break

                elif ":" in line:
                    credential_found = True
                    break

                counter += 1
                if counter >= 10:
                    break

        if ssh_key:
            plan["Keys"].append(file)
            continue

        if credential_found:
            plan["Credentials"].append(file)
            continue

        ext = file.suffix.lower()
        
        if ext == ".hash":
            plan["Hashes"].append(file)
        elif ext in dump_ext:
            plan["Dumps"].append(file)
        elif ext == ".txt":
            plan["Notes"].append(file)
        
    return plan

def create_directories(plan, dry_run):
    #Verificar que categorias é que existem
    for categoria, value in plan.items():
        if value:
            if dry_run:
                print("Would create...")
                print(f"{categoria}")
            else:
                Path(categoria).mkdir(exist_ok=True)
    
    print("Pastas com ficheiros criadas")

def move_files(plan):
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

    args = parser.parse_args()

    files = get_files(args.path)
    plan = classify_files(files, args.dry_run)
    create_directories(plan, args.dry_run)
    move_files(plan)
    print_summary(plan)

if __name__ == "__main__":
    main()