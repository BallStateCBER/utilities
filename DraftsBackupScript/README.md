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
- type `python BackupDrafts.py -p <directory_path> [-p]` and execute
  - (`-p` is a "preview" option that doesn't actually make backups)

#### (OR)
- Make sure  `Run_Backup.bat` is in the same directory as `BackupDrafts.py`
- (if this is the first time running backups, ensure the proper locations are being backed up)
- Run the batch script

## CHANGING SCRIPT BEHAVIOR:
- Open `BackupDrafts.py` for editing.
- Near the top, you should see some constant lists:
  - `BACKUP_KEYWORDS`: A case-insensitive list of all keywords to be considered for backup (draft, prelim, etc)
  - `FILE_EXTENSIONS_TO_BACKUP`: a case-insensitive list of all file extensions to be considered for backup (for example, only Word and Excel Documents)
  - `BACKUP_FLDR`: the name of the folder that should contain backups (historically, this is the `old` folder, but this can be changed if desired)

## ADD/ALTER BACKUP LOCATIONS:
To back up different/additional locations:
- Open `Backup_Locations.txt` with a text editor
- Add one folder path per line (all of these locations will be backed up individually)
  - (Note that the script will crawl subfolders, so there is no need to specify nested folders.)

## TASK SCHEDULING:
  To automatically run this script periodically:
  - Open the Windows Task Scheduler,
  - Schedule the `run_backup.bat` file run as often as you desire. (weekly or bi-weekly is suggested)
    - Make sure the run the script from the same folder (so that `Backup_Locations.txt` will be properly detected).
