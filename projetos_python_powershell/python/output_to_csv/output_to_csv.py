# Bibliotecas necessárias
import re
import csv

# Regex
timestamp = r"""\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})[ T](?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})\]"""
timestamp_regex = re.compile(timestamp)

# Categorias
valid_categories = {"INFO", "WARNING", "ERROR", "DEBUG"}

# Ler o ficheiro de Output e criar o csv
with open("generic_outputs.txt", "r", encoding="utf-8") as file, \
     open("output.csv", "w", newline="", encoding="utf-8") as output:
        
        # Escrever no ficheiro
        writer = csv.writer(output)
        # Escrever uma linha
        writer.writerow(["Timestamp", "Category", "Description"])

        # Percorrer cada linha do ficheiro
        for line in file:
            line = line.strip()

            # Confirmar a timestamp
            timestamp = timestamp_regex.match(line)
            
            # Validar timestamp
            if timestamp:
                
                text_timestamp = timestamp.group(0)
                rest_log = line[:timestamp.start()] + line[timestamp.end():]
                rest_log = rest_log.strip().split() #Armazenar o resto do log em arrays

                if rest_log and rest_log[0] in valid_categories:
                    category = rest_log[0]

                    description = " ".join(rest_log[1:])
                            
                    print("A escrever:", text_timestamp, category, description)
                    writer.writerow([text_timestamp.strip("[]"), category, description])
                
                



            

        
        
        
        