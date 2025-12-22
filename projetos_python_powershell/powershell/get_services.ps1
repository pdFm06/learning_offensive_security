#Script simples para listar todos os serviços em execução
Get-Service | Where-Object {$_.Status -EQ "Running"}

#Alternativa:
#Get-Service -Stutus Running (Não funciona em PowerShell 5.1)

#O que aprendi a criar este script:
# - Que tenho o PowerShell 5.1 instalado e devido a tal não consegui correr uma alternativa
# - É preferível utilizar o $_.<propriedade> ao invés da forma curta, porque é mais fléxivel.

