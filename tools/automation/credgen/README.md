# credgen

A lightweight CLI tool that generates authentication commands to test a credential pair against multiple network services.

**credgen** is designed to help automate common penetration testing tasks by quickly producing ready-to-use commands for protocols such as SSH, SMB, RDP, WinRM, FTP, and MySQL.

---

## Features

* Accepts **IP address or domain** as target
* Supports **username + password** OR **username + hash (Pass-the-Hash)**
* Generates commands for multiple protocols at once
* Simple CLI interface using `argparse`
* Input validation for IP addresses and domains
* Clean, copy-paste friendly output

---

## Supported Protocols

| Protocol | Password | Hash  |
| -------- | -------- | ----- |
| SSH      | ✅ Yes    | ❌ No  |
| FTP      | ✅ Yes    | ❌ No  |
| SMB      | ✅ Yes    | ✅ Yes |
| RDP      | ✅ Yes    | ✅ Yes |
| WinRM    | ✅ Yes    | ✅ Yes |
| MySQL    | ✅ Yes    | ❌ No  |

---

## Requirements

* Python **3.8+**
* External tools installed depending on protocol:

  * `ssh`
  * `ftp`
  * `netexec`
  * `xfreerdp3`
  * `evil-winrm`
  * `mysql`

Make sure these binaries are available in your system `PATH`.

---

## Usage

### Password authentication

```bash
python credgen.py -i 192.168.1.10 -u admin --password 'Password123!' --protocols ssh smb rdp
```

### Pass-the-Hash authentication

```bash
python credgen.py -i 192.168.1.10 -u admin --hash aad3b435b51404eeaad3b435b51404ee --protocols smb winrm rdp
```

---

## Example Output

```
[-------------------------------------------------]
[+] SSH
    ssh admin@192.168.1.10
[+] SMB
    netexec smb 192.168.1.10 -u admin -p 'Password123!' --shares
[+] RDP
    xfreerdp3 /v:192.168.1.10 /u:admin /p:'Password123!'
[-------------------------------------------------]
```

---

## Arguments

| Argument           | Description                                      |
| ------------------ | ------------------------------------------------ |
| `-i`, `--target`   | Target IP address or domain                      |
| `-u`, `--username` | Username to test                                 |
| `--password`       | Plaintext password                               |
| `--hash`           | Password hash (mutually exclusive with password) |
| `--protocols`      | One or more protocols to generate commands for   |

---

## Notes

* Only **one authentication mode** can be used at a time (`--password` OR `--hash`).
* Some protocols do **not support hash authentication**.
* This tool **does not execute commands**, it only generates them.

---

## Legal Disclaimer

This tool is intended **for authorized security testing, lab environments, and educational purposes only**.
Do not use it against systems without explicit permission.

---

## Author

Created as part of a personal penetration testing automation toolkit.

Feel free to modify and extend.
