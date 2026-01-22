# Definir o que são permissões fracas
# Listar todos os serviços do sistema operativo
# Listar as permissões de cada serviços
# Selecionar os serviços com permissões fracas

# Permissões fracas

# Informações a recolher
# Qual é o utilizador que é executado quando corre o serviço (perigoso se for SYSTEM)
# Qual é o BinaryPath do serviço e se ele é sujeito a mudanças por utilizadores de baixo privilégio.
# ACL do serviço (Quem pode iniciar, parar, reiniciar).
# ACL do binário (Quem pode mudar o binário do serviço).
# ACL diretório do binário do serviço (Quem pode mudar o que está dentro do diretório do binário do serviço)

# Recolher os serviços do computador que correm como SYSTEM
#Get-CimInstance Win32_Service | Where-Object { $_.StartName -eq "LocalSystem" }

# Extrair o caminho do executável do PathName
function Get-ExecPathFromPathName {
    # Receber o PathName
    param([string]$PathName)

    # Verificar se está vazio ou se só tem espaços " "
    if ([string]::IsNullOrWhiteSpace($PathName)) { return $null }

    # Tirar os espaços no início e fim
    $p = $PathName.Trim()

    # Caso A - Se começar com aspas, exemplo: "C:\ProgramFiles\..."
    if($p.StartsWith('"')) {
        $m = [regex]::Match($p, '^"([^"]+)"')
        if ($m.Success) { return $m.Groups[1].Value }
        return $null
    }

    # Caso B - Se não começar com aspas
    return ($p -split '\s+')[0]

}


$services = Get-CimInstance Win32_Service | Where-Object { $_.StartName -eq "LocalSystem" } | Select-Object Name, DisplayName, State, PathName
$findings = foreach ($service in $services) {
    $RawPath = $service.PathName

    # Verificar o PathName (Verificar se o PathName tem aspas e espaços - É um possível vetor)

    # Extrair o ExecPath 
    $ExecPath = Get-ExecPathFromPathName -PathName $RawPath
    $dir = Split-Path -LiteralPath $ExecPath -Parent
    
    if (-not $ExecPath) { continue }

    # Verificar se o ExecPath existe
    if(Test-Path -LiteralPath $ExecPath) {
        
        # Se o ExecPath existir:
        # Obter informação sobre as permissões do Path
        $acl = Get-Acl -LiteralPath $ExecPath
        $dir_acl = Get-Acl -LiteralPath $dir

        # ACEs vulneravéis
        $weakIdentities = @(
            'BUILTIN\Users',
            'NT AUTHORITY\Authenticated Users',
            'Everyone'
        )

        # Permissões vulneráveis
        $weakRules = $acl.Access | Where-Object {
            $_.AccessControlType -eq 'Allow' -and
            ($weakIdentities -contains $_.IdentityReference.Value) -and
            (($_.FileSystemRights.ToString() -match 'Write|Modify|FullControl'))
        }

        $weakRulesDir = $dir_acl.Access | Where-Object {
            $_.AccessControlType -eq 'Allow' -and
            ($weakIdentities -contains $_.IdentityReference.Value) -and
            (($_.FileSystemRights.ToString() -match 'Write|Modify|FullControl'))
        }

        $weakType = @()

        if ($weakRules) {
            $weakType += "File"
        }

        if ($weakRulesDir) {
            $weakType += "Directory"
        }

        # Guardar os serviços vulneráveis        
        if ($weakRules -or $weakRulesDir) {
            [PSCustomObject]@{
                ServiceName = $service.Name
                ExecPath = $ExecPath
                WeakTarget = ($weakType -join ', ')
                WeakAces = ($weakRules | ForEach-Object { "$($_.IdentityReference): $($_.FileSystemRights)" }) -join '; '
            }
        }


    }
}
"Findings count: $($findings.Count)" | Write-Host
$findings | Format-Table -AutoSize


