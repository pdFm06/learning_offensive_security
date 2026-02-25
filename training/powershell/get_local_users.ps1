#Formato do raciocinio: Obter todas as contas locais -> Selecionar apenas o Nome, Estado e SID -> filtrar por contas ativas
#Get-LocalUser | Select-Object -Property Name, Enabled, SID | Where-Object Enabled -EQ $true

#Coisas que aprendi:
#O PowerShell só trabalha com objetos
#Enabled é igual a True, por isso não é necessário comparar a Ture
#É sempre melhor filtrar antes de selecionar propriedades

Get-LocalUser | Where-Object Enabled | Select-Object -Property Name, Enabled, SID 
