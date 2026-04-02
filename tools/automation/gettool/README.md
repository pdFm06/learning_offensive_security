# gettool

A lightweight CLI tool designed to automate the process of locating and collecting tools during penetration testing, CTFs, and lab environments.

gettool helps eliminate the manual effort of searching, copying, and organizing binaries or scripts by quickly finding them on a system and moving them to your working directory.

---

## Features

* Locate tools by exact filename
* Search tools using partial names (keyword-based)
* Automatically copy discovered tools to a chosen directory
* Prevent overwriting existing files
* Limit results for faster triage
* Simple and fast CLI interface using argparse

---

## Modes

### Exact Mode

Search for a specific tool and copy it to your desired directory.

```bash id="f9x2c1"
python script.py -f linpeas.sh -d /tmp
```

---

### Search Mode

Find tools when you do not remember the exact name.

```bash id="a8k3d2"
python script.py -s peas
```

---

## Arguments

| Argument         | Description                          |
| ---------------- | ------------------------------------ |
| `-f`, `--file`   | Tool filename to search (exact mode) |
| `-d`, `--dest`   | Destination directory                |
| `-p`, `--path`   | Base path to search from             |
| `-s`, `--search` | Keyword search mode                  |
| `--limit`        | Limit number of results              |

---

## Example Usage

### Retrieve a known tool

```bash id="k2l9p0"
python script.py -f pspy64 -p / -d /tmp
```

---

### Find tools without knowing the full name

```bash id="m4n8q7"
python script.py -s linpeas
```

---

### Search in common tool directories

```bash id="z7x6v5"
python script.py -s enum -p /opt --limit 5
```

---

## Use Cases

* Reusing tools already present on compromised systems
* Quickly collecting binaries from common locations such as:

  * `/tmp`
  * `/opt`
  * `/home`
* Avoiding repeated uploads of tools like linpeas or pspy
* Speeding up post-exploitation workflows

---

## Notes

* Searching from `/` can be slow and may trigger permission errors
* Use `-p` to limit scope for better performance
* Permission errors are ignored automatically

---

## Requirements

* Python 3.x
* No external dependencies

---

## Limitations

* Search is based on filename only
* Exact mode returns the first match found
* Performance depends on filesystem size

---

## Future Improvements

* Multi-keyword search
* Auto-prioritize common directories (`/tmp`, `/opt`, `/home`)
* Highlight executable files
* Save results to a loot file
* Parallel search for improved speed

---

## Philosophy

gettool is built to be simple, fast, and practical in real engagements.
It focuses on automating repetitive tasks without unnecessary complexity.

---

## Legal Disclaimer

This tool is intended for authorized security testing, lab environments, and educational purposes only.
Do not use it against systems without explicit permission.

---

## Author

Created as part of a personal penetration testing toolkit.
Feel free to modify and extend.
