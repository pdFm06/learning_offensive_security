# loot-organizer

A lightweight CLI tool that organizes penetration testing and CTF loot into structured categories such as credentials, hashes, configs, and more.

**loot-organizer** is designed to help streamline post-enumeration workflows by automatically sorting collected files based on content and file type.

---

## Features

* Organizes loot into meaningful categories automatically
* Detects **credentials** (`user:password`)
* Identifies **config files containing secrets** (ENV, YAML, INI, etc.)
* Recognizes **hashes** (NTLM, bcrypt-like, hex, etc.)
* Detects **SSH keys and private keys**
* Supports **dry-run mode** (preview changes safely)
* Optional **recursive scanning**
* Clean CLI interface using `argparse`

---

## Categories

| Category    | Description                                        |
| ----------- | -------------------------------------------------- |
| Keys        | Private keys and certificates                      |
| SSH         | SSH-related files                                  |
| Credentials | `user:password` style credentials                  |
| Hashes      | Hash dumps and hash-like data                      |
| Dumps       | Databases and structured exports                   |
| Notes       | General text/log files                             |
| Scans       | Tool outputs (e.g., nmap, masscan)                 |
| Scripts     | Scripts (`.py`, `.js`, `.rb`, etc.)                |
| Configs     | Configuration files without secrets                |
| CredConfig  | Configuration files containing credentials/secrets |

---

## Requirements

* Python **3.8+**
* No external dependencies required

---

## Usage

### Basic usage

```bash
python loot_organizer.py <path>
```

### Recursive scan

```bash
python loot_organizer.py <path> -r
```

### Dry run (no changes made)

```bash
python loot_organizer.py <path> --dry-run
```

### Debug mode

```bash
python loot_organizer.py <path> --debug
```

---

## Example Output

```
===== Loot Summary =====
Keys: 1 files
SSH: 1 files
Credentials: 2 files
Hashes: 2 files
Dumps: 2 files
Notes: 5 files
Scans: 0 files
Scripts: 2 files
Configs: 2 files
CredConfig: 3 files

Total: 20 files
```

---

## Arguments

| Argument            | Description                          |
| ------------------- | ------------------------------------ |
| `path`              | Directory containing loot files      |
| `-r`, `--recursive` | Scan directories recursively         |
| `--dry-run`         | Preview changes without moving files |
| `--debug`           | Enable debug output                  |

---

## Notes

* Classification is based on **file extensions and content heuristics**
* Only the first few lines of each file are analyzed for performance
* Files are categorized based on **priority rules** to reduce conflicts

---

## Legal Disclaimer

This tool is intended **for authorized security testing, lab environments, and educational purposes only**.
Do not use it against systems without explicit permission.

---

## Author

Created as part of a personal penetration testing toolkit.

Feel free to modify and extend.
