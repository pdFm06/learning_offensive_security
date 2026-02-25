
#Definir parâmetros
param(
    [Parameter(Mandatory=$true, HelpMessage="Nome do log a ler (System, Application, Security)")] #Torna o parâmetro obrigatório e mostra o texto de ajuda
    [ValidateSet("System","Application","Security")] #Valores possíveis
    [string]$LogName, #Declara o parâmetro como string

    [Parameter(Mandatory=$false)] #Opcional
    [int]$MaxEvents = 50 #Declara o parâmetro MaxEvents como inteiro e com valor por defeito = 50
)
#Documentação - quando usamos Get-Help
#SYNOPSIS - Descrição curta, uma linha é o que aparece no Get-Help
#DESCRIPTION - Explicação detalhada do que a ferramenta faz
#PARAMETER LogName - Explica o que é o parâmetro $LogName
#PARAMETER MaxEvents - Explica o que é o parâmetro $MaxEvents
#EXAMPLE - Exemplo de uso da ferramenta

<#
.SYNOPSIS
    Extrai eventos de um log do Windows Event Viewer.

.DESCRIPTION
    Lê eventos de um log especificado e exporta o resultado para CSV.

.PARAMETER LogName
    Nome do log: System, Application ou Security.

.PARAMETER MaxEvents
    Número máximo de eventos a recolher (default: 50).

.EXAMPLE
    .\read_logs.ps1 -LogName System

.EXAMPLE
    .\read_logs.ps1 -LogName Application -MaxEvents 200
#>
#Write-host - escrever texto diretamente no ecrâ
Write-Host "[*] A ler log: $LogName" 

#Selecionar eventos e exportá-los para um CSV
Get-WinEvent -LogName $LogName -MaxEvents $MaxEvents | 
Select-Object TimeCreated, Id, LevelDisplayName, ProviderName, Message |
Export-Csv ".\${LogName}_logs.csv" -NoTypeInformation -Encoding UTF8

Write-Host "[+] Exportado para ${LogName}_logs.csv"
