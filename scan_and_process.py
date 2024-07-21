import os
import re
import json
import time
import colorama
from colorama import Fore, Style
from collections import defaultdict

colorama.init()

def load_arc_to_season(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

ARC_TO_SEASON = load_arc_to_season('arcs.json')

# Regex to match files
EPISODE_PATTERN = re.compile(r'(.*) - (\d{2,4})(?: (\[?\(?\d{3,4}p\)?\]?))?')
# Regex to exclude files with season/episode format like S00E00
SEASON_EPISODE_PATTERN = re.compile(r'.*S\d{2}E\d{2}.*', re.IGNORECASE)
# Regex to match season/episode format like S01 - 01
SEASON_PATTERN = re.compile(r'S(\d{1,2}) - (\d{2})')

def create_symlink(source, destination, symlinks_created):
    """Creates a symbolic link from source to destination if it doesn't already exist."""
    try:
        if not os.path.exists(destination):
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            file_extension = os.path.splitext(source)[1]  # Extract the file extension
            symlink_destination = destination + file_extension
            os.symlink(source, symlink_destination)
            symlinks_created.append(symlink_destination)  # Track created symlinks
            relative_source = os.path.join(os.path.basename(os.path.dirname(source)), os.path.basename(source))
            print(f"{Style.BRIGHT}{Fore.WHITE}[{time.strftime('%d/%m/%y %H:%M:%S')}] | {Fore.GREEN} Symlink created: {Fore.LIGHTCYAN_EX}{os.path.basename(symlink_destination)} {Fore.LIGHTMAGENTA_EX}-> {relative_source}{Style.RESET_ALL}")
    except FileExistsError:
        relative_source = os.path.join(os.path.basename(os.path.dirname(source)), os.path.basename(source))
        #print(f"{Style.BRIGHT}[{time.strftime('%d/%m/%y %H:%M:%S')}] | {Style.NORMAL}{Fore.YELLOW} Error, symlink already exists: {Fore.CYAN}'{os.path.basename(symlink_destination)}' {Fore.WHITE}->{Fore.LIGHTMAGENTA_EX} /{relative_source} {Style.RESET_ALL}")

def process_file(file_path, dest_dir, symlinks_created):
    """Processes a single file and creates a symlink if it matches the pattern."""
    filename = os.path.basename(file_path)
    # Remove square brackets and anything inside them at the start of the filename
    filename = re.sub(r'^\[.*?\]\s*', '', filename)
    if SEASON_EPISODE_PATTERN.match(filename):
        #print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Skipping file with season/episode format: {filename}{Style.RESET_ALL}")
        return
    match = EPISODE_PATTERN.match(filename)
    if match:
        show_name = match.group(1)
        folder_name = ' '.join(show_name.split(' ')[:-1])
        episode_number = match.group(2)
        resolution = match.group(3)
        
        # Determine the destination folder and create it
        season_number = 1
        arc_found = False
        for arc, season in ARC_TO_SEASON.items():
            if arc in show_name:
                season_number = season
                arc_found = True
                show_name = show_name.replace(f" - {arc}", "").strip()  # Remove arc from show name
                #print(show_name)
                break
        
        if not arc_found:
            season_match = SEASON_PATTERN.search(filename)
            if season_match:
                season_number = int(season_match.group(1))
                show_name = ' '.join(show_name.split(' ')[:-1])
        
        if resolution:
            # Remove any square or round brackets from the resolution
            resolution = re.sub(r'[\[\]\(\)]', '', resolution)
            new_filename = f"{show_name} - s{int(season_number):02d}e{int(episode_number):02d} {resolution}"
        else:
            new_filename = f"{show_name} - s{int(season_number):02d}e{int(episode_number):02d}"        
        
        season_folder = f"Season {int(season_number):02d}"
        
        show_folder = os.path.join(dest_dir, show_name.strip(), season_folder)
        new_path = os.path.join(show_folder, new_filename)
        
        create_symlink(file_path, new_path, symlinks_created)

def scan_source_directory(source_dir, dest_dir):
    """Scans the source directory and processes new/modified files that match the pattern."""
    folders_files = defaultdict(list)
    symlinks_created = []
    
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
            #print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Skipping folder with multiple matching files: {folder}{Style.RESET_ALL}")
            continue
        for file_path in files:
            process_file(file_path, dest_dir, symlinks_created)
    
    return symlinks_created
