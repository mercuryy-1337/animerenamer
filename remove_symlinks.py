import os
import time
import colorama
from colorama import Fore, Style

colorama.init()

def remove_broken_symlinks(dest_dir):
    """Removes broken symlinks from the destination directory."""
    for root, _, files in os.walk(dest_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.islink(file_path) and not os.path.exists(os.readlink(file_path)):
                os.remove(file_path)
                print(f"{Style.BRIGHT}{Fore.WHITE}[{time.strftime('%d/%m/%y %H:%M:%S')}] | {Style.NORMAL}{Fore.RED} Removed broken symlink: {file_path}{Style.RESET_ALL}")
