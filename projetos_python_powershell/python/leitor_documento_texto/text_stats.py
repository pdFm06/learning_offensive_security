#Abrir o ficheiro
with open("sample.txt", "r", encoding="utf-8") as ficheiro:
    #Guardar o texto numa variável
    texto = ficheiro.read()

#Contar o número de caracteres
qtd_caracteres = len(texto)

#Guardar o número de linhas
#Separar cada linha num array, vamos usar como distinçor o "\n"
linhas = texto.split("\n")
#contador
total_linhas = 0
for i in linhas:
    if i:
        total_linhas += 1

#Guardar cada palavra num array.
#Colocar cada palavra como elemento de um array
x = texto.split()

#Contar o número de elementos do array: número de palavras.
nr_palavras = len(x)

#linhas do ficheiro
print(f"Número de linhas: {total_linhas}")
print(f"Número de palavras:  {nr_palavras}")
print(f"Número de caracteres: {qtd_caracteres}")



