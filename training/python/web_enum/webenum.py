import ipaddress
import re
import socket
import subprocess
import os
import argparse

parser = argparse.ArgumentParser(
    description="Executes Nmap NSE + Gobuster (Vhost fuzzing) + Dirsearch (Dirbrute) + Whatweb (fingerprinting) in one script"
)

parser.add_argument(
    "-u", "--target",
    required=True,
    help="Target's IP or domain"
)

parser.add_argument(
    "-p", "--port",
    type=int,
    default=80,
    help="HTTP port (default: 80)"
)

parser.add_argument(
    "-w", "--wordlist",
    required=True,
    help="Gobuster wordlist (DNS)"
)

parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Enable verbose output"
)

parser.add_argument(
    "--no-nmap",
    action="store_true",
    help="Skip Nmap"
)

parser.add_argument(
    "--no-gobuster",
    action="store_true",
    help="Skip Gobuster Vhost fuzzing"
)

parser.add_argument(
    "--no-dirsearch",
    action="store_true",
    help="Skip Dirsearch bruteforcing"
)

parser.add_argument(
    "--no-whatweb",
    action="store_true",
    help="Skip WhatWeb fingerprinting"
)

parser.add_argument(
    "-t", "--threads",
    required=False,
    type=int,
    default=20,
    help="Threads for bruteforce tools (default: 20)"
)

args = parser.parse_args()
target = args.target
port = args.port
wordlist = args.wordlist
verbose = args.verbose
threads = args.threads


def ensure_outputs_dir(ip):
    os.makedirs(f"{ip}_outputs", exist_ok=True)


def run_nmap(target, port, timeout=600):
    scripts = "http-enum,http-title,http-headers"

    cmd = [
        "nmap",
        "-sV",
        "-p", str(port),
        "--script", scripts,
    ]

    if verbose:
        cmd += [
                "-vvv",
                "--stats-every=10s" 
        ]
        print("\n[+] Running Nmap...\n")
    cmd += [target, "-oA", os.path.join(f"{target}_outputs", f"{target}_nmapScan")]

    
    p = subprocess.run(cmd, text=True, timeout=timeout)
    return {"cmd": cmd, "returncode": p.returncode}


def run_gobuster(target, domain, wordlist, threads, port, timeout=600):
    url = f"http://{target}:{port}/"

    cmd = [
            "gobuster", "vhost",
            "-u", url,
            "-w", wordlist,
            "-t", str(threads),
            "--output", os.path.join(f"{target}_outputs", f"{target}_vhostFuzzing.txt"),
        ]
    
    if not verbose:
        cmd += ["--np"]

    if domain:
        cmd += ["--domain", domain, "--append-domain"]
    else:
        print("[!] No domain...")

    if verbose:
        print("\n[+] Running Gobuster...\n")
    p = subprocess.run(cmd, text=True, timeout=timeout)
    return {"cmd": cmd, "returncode": p.returncode}


def run_dirsearch(target, threads, port, timeout=600):
    url = f"http://{target}:{port}/"

    cmd = [
        "dirsearch",
        "-u", url,
        "-t", str(threads),
        "--output", os.path.join(f"{target}_outputs", f"{target}_dirsearchFuzzing.txt")
    ]

    if verbose:
        print("\n[+] Running Dirsearch...\n")
    p = subprocess.run(cmd, text=True, timeout=timeout)
    return {"cmd": cmd, "returncode": p.returncode}


def run_whatweb(target, port, timeout=600):
    url = f"http://{target}:{port}"

    cmd = [
        "whatweb",
        "-v",
        url,
        "--log-verbose", os.path.join(f"{target}_outputs", f"{target}_whatwebAnalysis.txt")
    ]

    if verbose:
        print("\n[+] Running Whatweb...\n")
    p = subprocess.run(cmd, text=True, timeout=timeout)
    return {"cmd": cmd, "returncode": p.returncode}


def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def resolve_domain_to_ips(host):
    infos = socket.getaddrinfo(host, None)
    ip_set = set()
    for family, socktype, proto, canonname, sockaddr in infos:
        ip_set.add(sockaddr[0])
    return sorted(ip_set)


def main():
    domain_pattern = r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
    domain_regex = re.compile(domain_pattern, re.IGNORECASE)

    domain = None
    ip = None

    if is_ip(target):
        ip = target
    elif domain_regex.fullmatch(target):
        domain = target.lower().strip()
        ips = resolve_domain_to_ips(domain)
        if not ips:
            raise ValueError("Could not resolve domain")
        ip = ips[0]
    else:
        raise ValueError("Invalid target")

    ensure_outputs_dir(ip)

    if not os.path.isfile(wordlist):
        raise FileNotFoundError(f"{wordlist} not found!")

    if not args.no_nmap:
        resNmap = run_nmap(ip, port=port, timeout=600)
        if resNmap["returncode"] != 0:
            print("[!] Nmap error!")

    if not args.no_gobuster:
        if domain is None:
            print("[!] No domain: skipping Vhost fuzzing...")
        else:
            resGobuster = run_gobuster(ip, domain, wordlist, threads=threads, port=port, timeout=600)
            if resGobuster["returncode"] != 0:
                print("[!] Gobuster error!")

    if not args.no_dirsearch:
        resDirSearch = run_dirsearch(ip, threads=threads, port=port, timeout=600)
        if resDirSearch["returncode"] != 0:
            print("[!] Dirsearch error!")

    if not args.no_whatweb:
        resWhatWeb = run_whatweb(ip, port=port, timeout=600)
        if resWhatWeb["returncode"] != 0:
            print("[!] Whatweb error!")


if __name__ == "__main__":
    main()
