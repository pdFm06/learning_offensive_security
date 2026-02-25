# WebEnum

Basic tool for automated initial web reconnaissance using:
- Nmap (NSE)
- Gobuster (vhost)
- Dirsearch
- WhatWeb

Designed for CTFs, labs and authorized security assessments.

## Requirements

- Python 3.9+
- nmap
- gobuster
- dirsearch
- whatweb
- SecLists

## Installation

```bash
sudo apt install nmap gobuster dirsearch whatweb seclists
git clone https://github.com/pdFm06/learning_offensive_security/tree/main/tools/web_enum
cd web_enum
```
## Usage

```bash
sudo python3 webenum.py -u cap.htb -p 80 -w wordlist.txt

With options:

--no-gobuster
--no-dirsearch
--no-whatweb
--verbose
```

Some Nmap scans may require elevated privileges.