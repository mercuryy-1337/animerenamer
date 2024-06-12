import os
import time
import argparse
import colorama
from colorama import Fore, Style
from scan_and_process import scan_source_directory, process_file
from remove_symlinks import remove_broken_symlinks

colorama.init()

def main():
    parser = argparse.ArgumentParser(description="Anime Renamer Script")
    parser.add_argument('source_dir', help="Source directory to monitor for anime files")
    parser.add_argument('dest_dir', help="Destination directory to create symlinks")
    parser.add_argument('--clean-symlinks', action='store_true', help="Enable removal of broken symlinks")
    args = parser.parse_args()

    while True:
        scan_source_directory(args.source_dir, args.dest_dir)
        if args.clean_symlinks:
            remove_broken_symlinks(args.dest_dir)
        print(f"{Fore.CYAN}[{time.strftime('%d/%m/%y %H:%M:%S')}] Scanned {args.source_dir}. Sleeping for 1 minute...{Style.RESET_ALL}")
        time.sleep(60)

if __name__ == "__main__":
    main()
