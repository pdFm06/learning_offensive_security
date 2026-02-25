# Saber que grupos existem no SO
# Dos grupos que existem, saber quais são os membros
# Criar alguma estrutura que mostre de forma clara cada grupo com os seus respetivos membros

# Saber que grupos existem no SO
# Só precisamos saber o nome do grupo
#Get-LocalGroup | Select-Object -Property Name

# Saber os membros de um determinado grupo
#Get-LocalGroupMember -Group "Administradores" | Select-Object -Property Name

#Criar o array
$grupos = Get-LocalGroup

# Percorrer cada grupo e obter os seus membros
foreach($group in $grupos) {
    Write-Host ("Membros do Grupo {0}: " -f $group.Name)
    #Posso usar .nome-da-propriedade
    # -ErrorAction SilentlyContinue: ignora os erros que não terminam a execução do programa
    # Format-Table serve para criar uma tabela
    Get-LocalGroupMember -Group $group.Name -ErrorAction SilentlyContinue | Format-Table -AutoSize 
    Write-Host "-----------------------------"
}
