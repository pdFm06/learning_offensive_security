# Script goals:
# Receive a credential pair - username/password, username/hash, etc.
# Receive the available services.
# Suggest commands to test the provided credentials against the selected services

# Plan:
# Receive credential pair
# Receive a list/sequence of services
# Generate commands

### Receive credentials ###
## Initialize parser ##
import argparse
import re
import ipaddress

parser = argparse.ArgumentParser(
    description="Generate commands to test a credential pair against selected services"
)

parser.add_argument(
    "-i", "--target",
    required=True,
    help="Target IP address or domain"
)

parser.add_argument(
    "-u", "--username",
    required=True,
    help="Username"
)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--password", help="Plaintext password")
group.add_argument("--hash", help="Password hash")

parser.add_argument(
    "--protocols",
    nargs="+",
    required=True,
    choices=["ssh", "ftp", "smb", "rdp", "winrm", "mysql"],
    help="Protocols to test"
)

args = parser.parse_args()
target = args.target
username = args.username
password = args.password
password_hash = args.hash
protocols = args.protocols

### Validate target ###
## Validate IP ##
def is_valid_ip(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

## Validate domain ##
pattern = r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$"
domain_regex = re.compile(pattern, re.IGNORECASE)

def is_valid_domain(target):
    return re.fullmatch(domain_regex, target) is not None

if not (is_valid_ip(target) or is_valid_domain(target)):
    parser.error("Invalid target: please provide a valid IP address or domain")

## Build command dictionaries ##
# Password-based commands
commands_password = {
    "ssh": lambda: f"ssh {username}@{target}",
    "ftp": lambda: f"ftp {username}@{target}",
    "smb": lambda: f"netexec smb {target} -u {username} -p '{password}' --shares",
    "rdp": lambda: f"xfreerdp3 /v:{target} /u:{username} /p:'{password}'",
    "winrm": lambda: f"evil-winrm -i {target} -u {username} -p '{password}'",
    "mysql": lambda: f"mysql -u {username} -p'{password}' -h {target}"
}

# Hash-based commands (Pass-the-Hash)
commands_hash = {
    "smb": lambda: f"netexec smb {target} -u {username} -H '{password_hash}' --shares",
    "rdp": lambda: f"xfreerdp3 /v:{target} /u:{username} /pth:'{password_hash}'",
    "winrm": lambda: f"evil-winrm -i {target} -u {username} -H '{password_hash}'",
}

# Select command set
commands = commands_hash if password_hash is not None else commands_password

# Output commands
print("-" * 100)
for proto in protocols:
    if proto in commands:
        print(f"[+] {proto.upper()}")
        print(f"    {commands[proto]()}")
    else:
        print(f"[-] {proto.upper()} does not support this authentication mode")
print("-" * 100)