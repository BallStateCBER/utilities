@echo off

REM ######################################
REM THIS FILE SHOULD NOT NEED MODIFICATION
REM     TO ALTER BACKED-UP LOCATIONS,
REM      EDIT "BACKUP_LOCATIONS.TXT"
REM ######################################




REM #############################
REM Setup the log output location
REM #############################

set month=%date:~4,2%
set day=%date:~7,2%
set year=%date:~10,4%
set log_folder=%userprofile%\logs
set log_file=backup_log-%year%-%month%-%day%.txt
set log_path=%log_folder%\%log_file%


REM make sure the log location exists!
if not exist %log_folder% mkdir %log_folder%



REM #########################################################
REM run the script, and redirect its output to a log location
REM #########################################################


for /F "tokens=*" %%D in (Backup_Locations.txt) do (
echo backing up files in "%%D"
python BackupDrafts.py -d "%%D" >> %log_path%
)



REM #########################################
REM Let us know when the backups are finished
REM #########################################

echo Backups complete:
echo     log saved to %log_path%
pause
