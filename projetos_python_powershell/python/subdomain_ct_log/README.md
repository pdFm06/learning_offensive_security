# subdomain_ct_log

Extracts domains and subdomains from Certificate Transparency logs using crt.sh.

## Features

- Queries crt.sh for a target domain
- Extracts domains from `common_name` and `name_value` (SANs)
- Removes duplicates
- Outputs to stdout or text file
- Optional verbose mode

## Installation

### Requirements

- Python 3.9+

### Setup

```bash
git clone https://github.com/<user>/subdomain_ct_log.git
cd subdomain_ct_log
pip install -r requirements.txt

(Optional) Use a virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

## Usage

```bash
python subdomain_ct_log.py -d example.com
python subdomain_ct_log.py -d example.com -o example -v
```
