# CBER Auto-Backup Script

## DESCRIPTION:
Looks through a specified directory,
and automatically backs up files according to CBER's expected file structure.

## Requirements:
Python

## Author:
Brandon Patterson

## USAGE:
- In a command prompt
- type `python BackupDrafts.py -p <directory_path>` and executes

#### (OR)
- Make sure  `Run_Backup.bat` is in the same directory as `BackupDrafts.py`
- (if this is the first time running backups, ensure the proper locations are being backed up)
- Run the batch script


## TASK SCHEDULING:
To automatically run this script periodically:
- Open the Windows Task Scheduler,
- schedule the `run_backup.bat` file run as often as you desire. (weekly or bi-weekly is suggested)

## CHANGING SCRIPT BEHAVIOR:
- Open `BackupDrafts.py` for editing.
- Near the top, you should see some constant lists:
  - `BACKUP_KEYWORDS`: A case-insensitive list of all keywords to be considered for backup (draft, prelim, etc)
  - `FILE_EXTENSIONS_TO_BACKUP`: a case-insensitive list of all file extensions to be considered for backup (for example, only Word and Excel Documents)
  - `BACKUP_FLDR`: the name of the folder that should contain backups (historically, this is the `old` folder, but this can be changed if desired)

## ADD/ALTER BACKUP LOCATIONS:
To back up different/additional locations:
- Open `run_backup.bat` with a text editor (DON'T run it, but edit!)
- Find the group of lines that read `set backup_location=...`, `echo backing up files...`, and `python BackupDrafts.py...`
- This code sets the backup location, notifies that a backup is happenning, and then executes it
- Edit/duplicate these lines to backup different/more locations.
(You can call the script multiple times on different locations if you wiSh to back up several folders)
