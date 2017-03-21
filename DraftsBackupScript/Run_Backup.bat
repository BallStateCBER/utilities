@echo off

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


REM Duplicate the below block of code (without the "REM"s) for each location you wish to back up.
REM (Nested folders are backed up automatically, so you only need to 

REM set backup_location="some\folder\you\wish\to\backup"
REM echo backing up files in %backup_location%
REM python BackupDrafts.py -d %backup_location% >> %log_path%


set backup_location="%userprofile%\Box Sync\CBER Box\CBER Box - Research"
echo backing up files in %backup_location%
python BackupDrafts.py -d %backup_location% >> %log_path%



REM #########################################
REM Let us know when the backups are finished
REM #########################################

echo Backups complete:
echo     log saved to %log_path%
pause
