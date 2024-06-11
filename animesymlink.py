import os
import re
import time
import colorama
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

colorama.init()


SOURCE_DIR = '/path/to/source'
DEST_DIR = '/path/to/symlinkdestination'

# Regex to match files
EPISODE_PATTERN = re.compile(r'(.*) - (\d{2,4})(?: (\[?\(?\d{3,4}p\)?\]?))?')

def create_symlink(source, destination):
    """Creates a symbolic link from source to destination if it doesn't already exist."""
    try:
        if not os.path.exists(destination):
            os.symlink(source, destination)
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Pattern Matched for file {source}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink created: {destination} -> {source}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink already exists: {destination}{Style.RESET_ALL}")
    except FileExistsError:
        print(f"{Fore.YELLOW}[{time.strftime('%d/%m/%y %H:%M:%S')}] Symlink creation failed, already exists: {destination}{Style.RESET_ALL}")

def process_file(file_path):
    """Processes a single file and creates a symlink if it matches the pattern."""
    match = EPISODE_PATTERN.match(os.path.basename(file_path))
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
    else:
        print(f"[{time.strftime('%d/%m/%y %H:%M:%S')}] Pattern did not match for file: {file_path}")

def scan_existing_files(directory):
    """Scans the directory and processes existing files that match the pattern."""
    for root, _, files in os.walk(directory):
        for file in files:
            process_file(os.path.join(root, file))

class EpisodeHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed_files = set()

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path not in self.processed_files:
                self.processed_files.add(file_path)
                process_file(file_path)

    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            if file_path not in self.processed_files:
                self.processed_files.add(file_path)
                process_file(file_path)

def main():
    scan_existing_files(SOURCE_DIR)

    event_handler = EpisodeHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=True)
    observer.start()
    print(f"{Fore.CYAN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Started monitoring {SOURCE_DIR}{Style.RESET_ALL}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
