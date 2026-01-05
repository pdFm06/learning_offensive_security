#Script simples que exporta todos os processos em execução para um ficheiro csv.
Get-Process | Select-Object -Property ProcessName, Id, SI | Export-Csv -Path .\processos.csv -NoTypeInformationcle