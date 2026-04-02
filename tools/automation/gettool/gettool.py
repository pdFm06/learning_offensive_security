import os
from pathlib import Path
import shutil
import argparse

def get_pwd():
    return os.getcwd()

def parse_args():
    parser = argparse.ArgumentParser(description="Find and copy file")
    parser.add_argument("-f", "--file", help="File to search")
    parser.add_argument("-d", "--dest", default=os.getcwd(), help="Destination directory (Default: current directory)")
    parser.add_argument("-p", "--path", default="/", help="Search base path (Default: '/')")
    parser.add_argument("-s", "--search", help="Search for files/directories by keyword")
    parser.add_argument("--limit", type=int, help="Limit number of results (Default: None)")
    return parser.parse_args()

def get_file(file, search_path="/"):
    base_path = Path(search_path)

    for file_path in base_path.rglob(file):
        print(f"[+] Found: {file_path}")
        return file_path
    
    print("[!] No file found")
    return None

def move_file(file, destination):
    if not file:
        print("[!] File not found")
        return

    file_name = file.name
    destination_path = Path(destination) / file_name

    counter = 1
    while destination_path.exists():
        destination_path = Path(destination) / f"{file.stem}_{counter}{file.suffix}"
        counter += 1

    print(f"[+] Copying {file} -> {destination_path}")
    shutil.copy(str(file), destination_path)

def search_files(keyword, search_path="/", limit=None):
    base_path = Path(search_path)
    count = 0

    print(f"[+] Searching for keyword: {keyword}")

    for path in base_path.rglob("*"):
        try:
            if keyword.lower() in path.name.lower():
                print(f"[+] Match: {path}")
                count += 1

                if limit and count >= limit:
                    print("[*] Limit reached")
                    return

        except PermissionError:
            continue

    if count == 0:
        print("[!] No matches found")

def main():
    args = parse_args()

    if args.search:
        search_files(args.search, args.path, args.limit)
        return
    
    print(f"[+] Searching for: {args.file}")
    file = get_file(args.file)

    move_file(file, args.dest)

if __name__ == "__main__": 
    main()