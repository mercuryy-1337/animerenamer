import os
import re
import time
import colorama
from colorama import Fore, Style
from collections import defaultdict

colorama.init()

# Regex to match files
EPISODE_PATTERN = re.compile(r'(.*) - (\d{2,4})(?: (\[?\(?\d{3,4}p\)?\]?))?')
# Regex to exclude files with season/episode format like S00E00
SEASON_EPISODE_PATTERN = re.compile(r'.*S\d{2}E\d{2}.*', re.IGNORECASE)
# Regex to match season/episode format like S01 - 01
SEASON_PATTERN = re.compile(r'S(\d{1,2}) - (\d{2})')

def create_symlink(source, destination):
    """Creates a symbolic link from source to destination if it doesn't already exist."""
    try:
        if not os.path.exists(destination):
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            file_extension = os.path.splitext(source)[1]  # Extract the file extension
            symlink_destination = destination + file_extension
            os.symlink(source, symlink_destination)
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Pattern Matched for file {source}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink created: {symlink_destination} -> {source}{Style.RESET_ALL}")
    except FileExistsError:
        print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink creation failed, already exists: {destination}{Style.RESET_ALL}")

def process_file(file_path, dest_dir):
    """Processes a single file and creates a symlink if it matches the pattern."""
    filename = os.path.basename(file_path)
    # Remove square brackets and anything inside them at the start of the filename
    filename = re.sub(r'^\[.*?\]\s*', '', filename)
    if SEASON_EPISODE_PATTERN.match(filename):
        print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Skipping file with season/episode format: {filename}{Style.RESET_ALL}")
        return
    match = EPISODE_PATTERN.match(filename)
    if match:
        show_name = match.group(1)
        folder_name = ' '.join(show_name.split(' ')[:-1])
        episode_number = match.group(2)
        resolution = match.group(3)
        if resolution:
            # Remove any square or round brackets from the resolution
            resolution = re.sub(r'[\[\]\(\)]', '', resolution)
            new_filename = f"{show_name} - E{episode_number} {resolution}"
        else:
            new_filename = f"{show_name} - E{episode_number}"
        
        # Determine the destination folder and create it
        season_match = SEASON_PATTERN.search(filename)
        if season_match:
            season_number = season_match.group(1)
            season_folder = f"Season {int(season_number)}"
            show_name = ' '.join(show_name.split(' ')[:-1]) 
        else:
            season_folder = "Season 1"

        show_folder = os.path.join(dest_dir, show_name.strip(), season_folder)
        new_path = os.path.join(show_folder, new_filename)
        
        create_symlink(file_path, new_path)

def scan_source_directory(source_dir, dest_dir):
    """Scans the source directory and processes new/modified files that match the pattern."""
    folders_files = defaultdict(list)
    
    # Gather files in each directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            filename = os.path.basename(file_path)
            if EPISODE_PATTERN.match(filename):
                folders_files[root].append(file_path)
    
    # Process files
    for folder, files in folders_files.items():
        if len(files) > 1:
            print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Skipping folder with multiple matching files: {folder}{Style.RESET_ALL}")
            continue
        for file_path in files:
            process_file(file_path, dest_dir)
