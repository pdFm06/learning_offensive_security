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
import pathlib

# Dump extensions
dump_ext = [".sql", ".db", ".sqlite", ".csv"]

def get_files(path=None):
    # Receber o diretório e listar os ficheiros dentro dele.
    
    if path is None:
        dir_list = pathlib.Path.cwd()
    else:
        dir_list = pathlib.Path(path)
    
    files = []

    if dir_list.exists() and dir_list.is_dir():

        # Filtrar se é um diretório ou se é um ficheiro
        for item in dir_list.iterdir():
            if item.is_file():
                files.append(item)

        return files
    else:
        raise FileNotFoundError("Path does not exist")
    
def classify_files(files):
    # Categorias
    plan = {
        "Keys": [],
        "Credentials": [],
        "Hashes": [],
        "Dumps": [],
        "Notes": []
    }

    for file in files:
        ext = file.suffix.lower()
        
        if ext == ".hash":
            plan["Hashes"].append(file)
        elif ext in dump_ext:
            plan["Dumps"].append(file)
        elif ext == ".txt":
            plan["Notes"].append(file)
        
    print(plan)


def main():
    #print(get_files("C:/Users/pedro/Documents/learning_offensive_security/training/python/loot_organizer/loot"))
    files = get_files("C:/Users/pedro/Documents/learning_offensive_security/training/python/loot_organizer/loot")
    classify_files(files)



if __name__ == "__main__":
    main()