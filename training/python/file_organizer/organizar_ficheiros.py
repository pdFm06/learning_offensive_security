#Ler ficheiros de uma pasta
#Ler a extensão dos ficheiros
#Ordenar as extensões segundo um critério
#Ordenar os ficheiros

#Ler ficheiros da pasta
#Importar a biblioteca os - permite-nos usar funções dependentes do sistema operatibo
import os

#Ler todos os ficheiros da pasta ficheiros
ficheiros = os.listdir("ficheiros/")
#Criar um array para guardar as extensões
extensoes = []

#Percorrer cada ficheiro da lista de ficheiros.
#Extrair a extensão do ficheiro e adicionar ao array de extensões
for ficheiro in ficheiros:
    #Ler a extensão dos ficheiros
    extensao = ficheiro.split(".")[-1]
    extensoes.append(extensao)

#Ordenar extensões
extensoes.sort()
#print(extensoes)

#Criar um dicionário onde cada extensão aponta para uma posição da lista
prioridade = {extensao: i for i, extensao in enumerate(extensoes)}
#print(prioridade)

#Ordenar os ficheiros
ficheiros.sort(
    key=lambda f: prioridade.get(
        os.path.splitext(f)[1].lstrip("."),
        float("inf")
    )
)

#Mostar os ficheiros ordenados
print(ficheiros)
