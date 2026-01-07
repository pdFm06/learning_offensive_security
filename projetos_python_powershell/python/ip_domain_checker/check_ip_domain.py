#Biblioteca standard do Python para trabalhar com expressões regulares
import re

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
ipv4_regex = re.compile(ipv4_pattern, re.VERBOSE)
service_pattern = r"^(\d+)\/(tcp|udp)\s+open\s+(\S+)\s*(.*)$"


domain_pattern = r"""
^
(?!-) #A string não pode começar com "-"
([a-zA-Z0-9]+ #Pelo menos uma 1 letra ou número
(-[a-zA-Z0-9]+)*\.)+ #Outra vez + separador "."
[a-zA-Z]{2,} #TLD apenas letras
$
"""

#Transforma a string num objeto otimizado
#re.VERBOSE - Ignorar espaços, quebras de linha, comentários
ipv4_regex = re.compile(ipv4_pattern, re.VERBOSE)
domain_regex = re.compile(domain_pattern, re.VERBOSE)

#Ler ficheiro
with open("sample.txt", "r", encoding="utf-8") as ficheiro:
    #ler linhas do ficheiro
    for linha in ficheiro:
        #separar cada palavra de cada linha
        entradas = linha.strip().split()

        #Percorrer cada palavra de cada linha
        for entrada in entradas:
            if not entrada: #Se não haver palavra, continuar
                continue

            #Verificar se o IPv4 é valido
            elif ipv4_regex.fullmatch(entrada):
                print(f"[IPv4 válido] {entrada}")

            #Verificar se o domínio é válido
            elif domain_regex.fullmatch(entrada):
                print(f"[Domínio válido] {entrada}")

            #Caso inválido
            else:
                print(f"[Inválido] {entrada}")
        


