# Script que lê um ficheiro .log e filtra linhas por palavra-chave

# 1º - Ler o ficheiro
# 2º - Selecionar palavras-chave
# 3º - Filtrar o conteúdo do ficheiro pelas palavras-chave definidas

palavras_chave = {
    "SEVERIDADE": [
        "CRITICAL", "ERROR", "WARNING", "FATAL", "ALERT", "EMERGENCY"
    ],
    
    "AUTENTICACAO": [
        "Failed login", "authentication failed", "unauthorized", "invalid credencials", "access denied", "permission denied", "account locked", "bruteforce", 
        "multiple access attempts"
    ],

    "REDE": [
        "blocked", "firewall", "port scan", "nmap", "connection refused", "reset by peer", "timeout", "IDS", "IPS"
    ],

    "SERVICOS": [
        "service down", "service stopped", "restart", "crash", "segmentation fault", "core dumped", "unresponsive", "connection timeout"
    ],

    "RECURSOS": [
        "disk space", "out of memory", "CPU overload", "I/O error", "filesystem", "read-only", "quota exceeded"
    ],

    "IOC": [
        "shell", "reverse", "meterpreter", "payload", "exploit", "backdoor", "rootkit", "webshell"
    ],

    "ADMIN": [
        "sudo", "privilege escalation", "root login", "administrator", "group added", "user added", "policy changed"
    ]
}

def analisar_linha(linha):
    resultados = []

    for categoria, palavras in palavras_chave.items():
        for termo in palavras:
            if termo.lower() in linha.lower():
                resultados.append((categoria, termo))

    return resultados


with open("big_sample.log", "r", encoding="utf-8") as ficheiro:
    for linha in ficheiro:
        resultados = analisar_linha(linha)

        if resultados:
            print("LOG:", linha.strip())
            for categoria, termo in resultados:
                print(f"  -> [{categoria}] termo detectado: {termo}")
            print("-" * 60)