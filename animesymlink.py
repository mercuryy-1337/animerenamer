import os
import re
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# some logging for troubleshooting purposes
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()


SOURCE_DIR = '/path/to/sourcefolder'
DEST_DIR = '/path/to/destinationfolder'

# Regex to match files
EPISODE_PATTERN = re.compile(r'(.*) - (\d{2})( .*)')

def create_symlink(source, destination):
    """Creates a symbolic link from source to destination if it doesn't already exist."""
    try:
        if not os.path.exists(destination):
            os.symlink(source, destination)
            logger.info(f"Symlink created: {destination} -> {source}")
        else:
            logger.info(f"Symlink already exists: {destination}")
    except FileExistsError:
        logger.info(f"Symlink creation failed, already exists: {destination}")

def process_file(file_path):
    """Processes a single file and creates a symlink if it matches the pattern."""
    logger.info(f"Processing file: {file_path}")
    match = EPISODE_PATTERN.match(os.path.basename(file_path))
    if match:
        logger.info(f"Pattern matched for file: {file_path}")
        show_name = match.group(1)
        episode_number = match.group(2)
        title = match.group(3)
        new_filename = f"{show_name} - E{episode_number}{title}"
        new_path = os.path.join(DEST_DIR, new_filename)
        create_symlink(file_path, new_path)
    else:
        logger.info(f"Pattern did not match for file: {file_path}")

def scan_existing_files(directory):
    """Scans the directory and processes existing files that match the pattern."""
    for root, _, files in os.walk(directory):
        for file in files:
            process_file(os.path.join(root, file))

class EpisodeHandler(FileSystemEventHandler):
    """Handles file system events and creates symlinks for matching files."""
    def on_created(self, event):
        logger.info(f"Created event detected: {event.src_path}")
        if not event.is_directory:
            process_file(event.src_path)
        else:
            scan_existing_files(event.src_path)

    def on_modified(self, event):
        logger.info(f"Modified event detected: {event.src_path}")
        if not event.is_directory:
            process_file(event.src_path)

def main():
    scan_existing_files(SOURCE_DIR)

    event_handler = EpisodeHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=True)
    observer.start()
    logger.info(f"Started monitoring {SOURCE_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
