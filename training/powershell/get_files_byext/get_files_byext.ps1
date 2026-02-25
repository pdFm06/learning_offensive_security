<#
.SYNOPSIS
Procura ficheiros no sistema de ficheiros com base num perfil de extensões (documentos, backups, logs, etc.).

.DESCRIPTION
Este script percorre recursivamente um caminho e lista ficheiros cuja extensão pertence a um perfil pré-definido.
Os resultados são apresentados no ecrã agrupados por extensão (ex.: pdf, txt, ...).

Perfis disponíveis:
- documents: .txt .doc .docx .pdf .xls .xlsx .ppt .pptx .odt .csv .rtf
- credentials: .ini .cfg .conf .config .env .json .yml .yaml .xml .toml
- scripts: .ps1 .bat .cmd .sh .py .rb .js .vbs .go .java .c .cpp .cs .php
- binaries: .exe .dll .sys .msi .bin .elf .app
- backups: .zip .rar .7z .tar .gz .bak .old .backup
- dumps: .db .sqlite .sqlite3 .sql .mdf .ldf .dump
- logs: .log .out .err .trace
- keys: .key .pem .crt .cer .pfx .p12 .pub

.PARAMETER Profile
Perfil de pesquisa. Determina as extensões a procurar.

.PARAMETER Path
Caminho base onde a pesquisa começa. Por omissão: C:\Users

.PARAMETER FullDisk
Se indicado, pesquisa o disco inteiro (C:\). Nota: pode ser lento e gerar muitos "Access denied" (que são ignorados).

.EXAMPLE
.\get_files_byext.ps1 -Profile documents
Procura ficheiros do perfil documents em C:\Users e lista-os por extensão.

.EXAMPLE
.\get_files_byext.ps1 -Profile logs -Path "C:\Temp"
Procura logs apenas em C:\Temp.

.EXAMPLE
.\get_files_byext.ps1 -Profile credentials -FullDisk
Procura ficheiros de configuração/credenciais em todo o disco C:\.

.NOTES
Projeto de aprendizagem (PowerShell). A pesquisa recursiva em C:\ pode demorar.
#>
# Receber o tipo de extensão
param(
    [Parameter(Mandatory=$true, HelpMessage="Perfil de pesquisa (documents, credentials, scripts, binaries, backups, dumps, logs, keys)")]
    [ValidateSet("documents", "credentials", "scripts", "binaries", "backups", "dumps", "logs", "keys")]
    [string]$Profile,

    [Parameter(Mandatory=$false, HelpMessage="Caminho base para pesquisa (default: C:\Users)")]
    [string]$Path = "C:\Users",

    [Parameter(Mandatory=$false, HelpMessage="Pesquisar o disco inteiro (C:\). Pode ser lento.")]
    [switch]$FullDisk
)

# Mapear os perfis aos tipos de ficheiros
$Profiles = @{
    documents = @(".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".csv", ".rtf")
    credentials = @(".ini", ".cfg", ".conf", ".config", ".env", ".json", ".yml", ".yaml", ".xml", ".toml")
    scripts = @(".ps1", ".bat", ".cmd", ".sh", ".py", ".rb", ".js", ".vbs", ".go", ".java", ".c", ".cpp", ".cs", ".php")
    binaries = @(".exe", ".dll", ".sys", ".msi", ".bin", ".elf", ".app")
    backups = @(".zip", ".rar", ".7z", ".tar", ".gz", ".bak", ".old", ".backup")
    dumps = @(".db", ".sqlite", ".sqlite3", ".sql", ".mdf", ".ldf", ".dump")
    logs = @(".log", ".out", ".err", ".trace")
    keys = @(".key", ".pem", ".crt", ".cer", ".pfx", ".p12", ".pub")
}

if (-not $Profiles.ContainsKey($Profile)) {
    throw "Perfil inválido: $Profile"
}

# Extensões de cada perfil
$Extensions = $Profiles[$Profile]


# O que fazer amanhâ: começar a procura e se der tempo, melhorar a UI
$RootPath = if ($FullDisk) { "C:\" } else { $Path }

# Normalizar as extensões
$ExtensionsNorm = $Extensions | ForEach-Object { $_.ToLowerInvariant() }

# Iniciar a procura
Write-Host "A procurar em $RootPath ..."

$Results = Get-ChildItem -Path $RootPath -File -Recurse -ErrorAction SilentlyContinue |
    Where-Object { $ExtensionsNorm -contains $_.Extension.ToLowerInvariant() }

$Grouped = $Results | Group-Object { $_.Extension.ToLowerInvariant() } | Sort-Object Name

# Percorrer cada grupo (extensão)
foreach ($g in $Grouped) {
    Write-Host ""
    Write-Host ($g.Name.TrimStart("."))
    $g.Group | ForEach-Object { Write-Host $_.FullName }
}


# Pesquisa
#Get-ChildItem -Path $RootPath -File -Recurse -ErrorAction SilentlyContinue | 
 #   Where-Object { $ExtensionsNorm -contains $_.Extension.ToLowerInvariant( } |
  #  Select-Object FullName, Length, LastWriteTime

# O que fazer amanhã: melhorar o desempenho da procura (utilizar select-object) e melhorar a UI