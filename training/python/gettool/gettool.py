# Finalidade do script: recebe o nome de uma ferramenta -> procura no file system -> move para a pasta atual
# O que precisamos:
# - Nome do ficheiro
# - Caminho do ficheiro
# - Caminho atual

# Bibliotecas
import os
from pathlib import Path
import shutil

def get_pwd():
    pwd = os.getcwd()
    return pwd

def get_file(file):
    for file_path in Path("/").rglob(file):
        return file_path
    return None

def move_file(file, destination):
    file_name = file.name
    source = str(file)
    print(file)
    destination = Path(destination) / file_name

    shutil.copy(source, destination)
        
def main():
    pwd = get_pwd()
    str(pwd)
    print(pwd)
    file = get_file("final_urls.txt")
    print(type(file))

    move_file(file, pwd)

if __name__ == "__main__":
    main()

