import ipaddress
import socket
import subprocess
import os
import argparse
import shutil
import ssl
import threading
import logging
import json
import time

# =========================
# CONFIG
# =========================

TIMEOUT = 600

# =========================
# CLI
# =========================

parser = argparse.ArgumentParser(
    description="Web enumeration orchestrator"
)

parser.add_argument("-u", "--target", required=True)
parser.add_argument("-p", "--port", type=int, default=80)
parser.add_argument("-w", "--wordlist", required=True)
parser.add_argument("-t", "--threads", type=int, default=20)

parser.add_argument("--no-nmap", action="store_true")
parser.add_argument("--no-gobuster", action="store_true")
parser.add_argument("--no-dirsearch", action="store_true")
parser.add_argument("--no-whatweb", action="store_true")

args = parser.parse_args()

# =========================
# UTILS
# =========================

def setup_logging(target):
    os.makedirs(f"{target}_outputs", exist_ok=True)

    logging.basicConfig(
        filename=f"{target}_outputs/run.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def check_tool(name):
    if shutil.which(name) is None:
        raise RuntimeError(f"{name} not found")

def detect_scheme(ip, port):
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((ip, port), timeout=3) as sock:
            with context.wrap_socket(sock):
                return "https"
    except:
        return "http"

def is_ip(v):
    try:
        ipaddress.ip_address(v)
        return True
    except:
        return False

def resolve_domain(host):
    infos = socket.getaddrinfo(host, None)
    return sorted({i[4][0] for i in infos})

def is_port_open(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        return s.connect_ex((ip, port)) == 0

# =========================
# PROGRESS BAR
# =========================

def progress_bar(done, total):
    percent = int((done / total) * 100) if total else 100
    bar = "#" * (percent // 5)
    print(f"\r[{bar:<20}] {percent}% ", end="")

# =========================
# RUN TOOL (OUTPUT NO FINAL)
# =========================

def run_tool(name, cmd, results, outputs, lock, print_lock):
    with print_lock:
        print(f"[+] [{name}] Running...")

    logging.info(f"{name} start")

    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=TIMEOUT
        )

        output = process.stdout

        with lock:
            outputs[name] = output

        if process.returncode == 0:
            results[name] = True

            with print_lock:
                print(f"[✔] [{name}] Done")
                print(f"\n----- {name} Output -----")
                print(output.strip())
                print(f"-------------------------\n")
        else:
            results[name] = False

            with print_lock:
                print(f"[✖] [{name}] Failed")
                print(f"\n----- {name} Output -----")
                print(output.strip())
                print(f"-------------------------\n")

    except subprocess.TimeoutExpired:
        results[name] = False
        with print_lock:
            print(f"[✖] [{name}] Timeout")

# =========================
# PARSERS
# =========================

def parse_outputs(outputs):
    findings = {
        "directories": [],
        "technologies": [],
        "vhosts": []
    }

    for tool, out in outputs.items():

        # DIRSEARCH → diretórios
        if tool == "Dirsearch":
            for line in out.splitlines():
                if any(code in line for code in ["200", "301", "302", "403"]):
                    findings["directories"].append(line.strip())

        # GOBUSTER → vhosts
        if tool == "Gobuster":
            for line in out.splitlines():
                if "found:" in line.lower() or "status:" in line.lower():
                    findings["vhosts"].append(line.strip())

        # WHATWEB → tecnologias
        if tool == "WhatWeb":
            for line in out.splitlines():
                if "[" in line and "]" in line:
                    findings["technologies"].append(line.strip())

    return findings

# =========================
# REPORT
# =========================

def save_report(target, results, findings):
    os.makedirs(f"{target}_outputs", exist_ok=True)

    with open(f"{target}_outputs/report.txt", "w") as f:
        f.write("=== RESULTS ===\n")
        for k, v in results.items():
            f.write(f"{k}: {v}\n")

        f.write("\n=== FINDINGS ===\n")
        for k, v in findings.items():
            f.write(f"{k}:\n")
            for item in v:
                f.write(f"  - {item}\n")

    with open(f"{target}_outputs/report.json", "w") as f:
        json.dump({"results": results, "findings": findings}, f, indent=4)

# =========================
# COMMANDS
# =========================

def nmap_cmd(target, port):
    return ["nmap", "-sV", "-p", str(port), target]

# 🔥 GOBUSTER → VHOST
def gobuster_cmd(target, wordlist, threads, port, scheme):
    return [
        "gobuster",
        "vhost",
        "-u", f"{scheme}://{target}:{port}",
        "-w", wordlist,
        "-t", str(threads),
        "--append-domain"
    ]

# 🔥 DIRSEARCH → FILES + DIRS (FIXED)
def dirsearch_cmd(target, port, scheme):
    output_dir = f"{target}_outputs"

    return [
        "dirsearch",
        "-u", f"{scheme}://{target}:{port}",
        "-e", "*",
        "-t", "20",
        "--random-agent",
        "--no-color",
        "--quiet",
        "--output", f"{output_dir}/dirsearch.txt",
        "--format", "plain"
    ]

def whatweb_cmd(target, port, scheme):
    return [
        "whatweb", f"{scheme}://{target}:{port}",
        "-v"
        ]

# =========================
# MAIN
# =========================

def main():
    target = args.target
    port = args.port

    if is_ip(target):
        ip = target
        domain = None
    else:
        ip = resolve_domain(target)[0]
        domain = target

    setup_logging(ip)

    scheme = detect_scheme(ip, port)
    print(f"[+] {ip}:{port} → {scheme.upper()}")

    results = {}
    outputs = {}
    lock = threading.Lock()
    print_lock = threading.Lock()

    tasks = []

    if not args.no_nmap:
        check_tool("nmap")
        tasks.append(("Nmap", nmap_cmd(ip, port)))

    if is_port_open(ip, port):

        # 🔥 só correr vhost se for domínio
        if not args.no_gobuster and domain:
            check_tool("gobuster")
            tasks.append(("Gobuster", gobuster_cmd(domain, args.wordlist, args.threads, port, scheme)))

        if not args.no_dirsearch:
            check_tool("dirsearch")
            tasks.append(("Dirsearch", dirsearch_cmd(ip, port, scheme)))

        if not args.no_whatweb:
            check_tool("whatweb")
            tasks.append(("WhatWeb", whatweb_cmd(ip, port, scheme)))

    total = len(tasks)
    threads = []

    for name, cmd in tasks:
        t = threading.Thread(
            target=run_tool,
            args=(name, cmd, results, outputs, lock, print_lock)
        )
        threads.append(t)
        t.start()

    while any(t.is_alive() for t in threads):
        done = sum(1 for t in threads if not t.is_alive())
        progress_bar(done, total)
        time.sleep(0.5)

    for t in threads:
        t.join()

    print("\n")

    findings = parse_outputs(outputs)
    save_report(ip, results, findings)

    print("===== Summary =====")
    for k, v in results.items():
        print(f"{k}: {'OK' if v else 'FAIL'}")

    print("\n===== Findings =====")
    for k, v in findings.items():
        print(f"{k}: {len(v)}")

    print(f"\nReport saved in {ip}_outputs/")

    if os.path.exists("reports"):
        try:
            shutil.rmtree("reports")
        except Exception:
            pass

if __name__ == "__main__":
    main()