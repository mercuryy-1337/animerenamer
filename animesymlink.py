import os
import re
import time
import colorama
from colorama import Fore, Style

colorama.init()

SOURCE_DIR = '/path/to/source'
DEST_DIR = '/path/to/destination'

# Regex to match files
EPISODE_PATTERN = re.compile(r'(.*) - (\d{2,4})(?: (\[?\(?\d{3,4}p\)?\]?))?')
# Regex to exclude files with season/episode format like S00E00
SEASON_EPISODE_PATTERN = re.compile(r'.*S\d{2}E\d{2}.*', re.IGNORECASE)

def create_symlink(source, destination):
    """Creates a symbolic link from source to destination if it doesn't already exist."""
    try:
        if not os.path.exists(destination):
            os.symlink(source, destination)
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Pattern Matched for file {source}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink created: {destination} -> {source}{Style.RESET_ALL}")
    except FileExistsError:
        print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink creation failed, already exists: {destination}{Style.RESET_ALL}")

def process_file(file_path):
    """Processes a single file and creates a symlink if it matches the pattern."""
    filename = os.path.basename(file_path)
    if SEASON_EPISODE_PATTERN.match(filename):
        print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Skipping file with season/episode format: {filename}{Style.RESET_ALL}")
        return
    match = EPISODE_PATTERN.match(filename)
    if match:
        show_name = match.group(1)
        episode_number = match.group(2)
        resolution = match.group(3)
        if resolution:
            new_filename = f"{show_name} - E{episode_number} {resolution}"
        else:
            new_filename = f"{show_name} - E{episode_number}"
        new_path = os.path.join(DEST_DIR, new_filename)
        create_symlink(file_path, new_path)

def scan_source_directory():
    """Scans the source directory and processes new/modified files that match the pattern."""
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            process_file(os.path.join(root, file))

def main():
    while True:
        scan_source_directory()
        print(f"{Fore.CYAN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Scanned {SOURCE_DIR}. Sleeping for 1 minute...{Style.RESET_ALL}")
        time.sleep(60)

if __name__ == "__main__":
    main()
