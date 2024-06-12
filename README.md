# animerenamer
A python script that is designed to monitor a directory for newly added or modified anime episode files that do not follow Plex's preferred naming convention. It creates symbolic links to these files in another directory, with the episode numbering modified to include an "E" before the episode number. This helps Plex recognize and organize the episodes correctly. This script is only useful if those episodes are not in the same folder, if they're in the same folder then plex has no issue recognising them.

## Features
- Automatically scans a source directory for new or modified anime files.
- Matches anime files based on customizable naming patterns.
- Creates symbolic links to organized folders in a destination directory
- Optionally removes broken symlinks to maintain a clean destination directory.

## Prerequisites
- Python 3.x installed on your system.
- colorama library for terminal color formatting. Install it using 
``` sh
pip install colorama.
```

## Installation and setup
1. Clone this repo 
``` sh
git clone https://github.com/mercuryy-1337/animerenamer.git
```
2. Navigate to the project directory
``` sh 
cd animerenamer
```
## Usage
- Run the script using Python, specifying the source and destination directories. **Optionally**, you can enable the removal of broken symlinks.
``` sh
python3 animesorter.py /path/to/sourcefolder /path/to/symlinkdestination [--clean-symlinks]
```
- The script will continuously monitor the source directory for new anime files and organize them into the destination directory
- The "--clean-symlinks" flag enables the removal of broken symlinks in the destination directory.
