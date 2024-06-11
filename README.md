# animerenamer
A python script that is designed to monitor a directory for newly added or modified anime episode files that do not follow Plex's preferred naming convention. It creates symbolic links to these files in another directory, with the episode numbering modified to include an "E" before the episode number. This helps Plex recognize and organize the episodes correctly. This script is only useful if those episodes are not in the same folder, if they're in the same folder then plex has no issue recognising them.

## Prerequisites

### Python Version

- Ensure you have Python 3.6 or higher installed. You can download Python from the [official website](https://www.python.org/downloads/).

### Required Libraries

- Install the required Python libraries using `pip`:

```sh
~pip install watchdog~
pip install colorama
