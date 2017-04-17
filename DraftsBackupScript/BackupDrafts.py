"""
OBJECTIVE:
    Recursively crawl through a specified directory, backing up any un-backed-up draft work.

AUTHOR(S): Brandon Patterson

NOTES:
    This is intended to be run automaticlly as a ~weekly job to automate
"""

import os
import sys
import datetime
import shutil
import getopt

# A list of all keywords to be searched for and backed up
BACKUP_KEYWORDS = ['DRAFT', 'WORKING', 'PRELIM', 'CALC']
FILE_EXTENSIONS_TO_BACKUP = ['DOC', 'DOCX', 'XLS', 'XLSX']
BACKUP_FLDR = 'old'


def is_backup_target(dir_path, file_name):
    """ determine whether a file needs to be backed up """

    if os.path.basename(dir_path) == 'old':  # don't back up the backups!
        return False
    elif any(kw.upper() in file_name.upper() for kw in BACKUP_KEYWORDS)\
            and file_name.upper().split('.')[-1] in FILE_EXTENSIONS_TO_BACKUP:
        return True
    else:
        return False


def already_backed_up(dir_path, file_name):
    """
    check whether a file has already been backed up
    (currently uses file size as the ONLY indicator, which could be improved in the future)
    """
    backup_dir = '{}\\{}'.format(dir_path, BACKUP_FLDR)
    if not os.path.exists(backup_dir):
        # if the backups folder doesn't exist, then the file hasn't been backed up!
        return False

    file_length = os.path.getsize('{}\\{}'.format(dir_path, file_name))
    backup_lengths = []
    for (fldr, nested_fldrs, files) in os.walk(backup_dir):
        for file in files:
            backup_lengths.append(os.path.getsize('{}\\{}'.format(fldr, file)))
    return file_length in backup_lengths


def backup_file(dir_path, file_name):
    """ create a backup of the given file """
    print("{}\\{}".format(dir_path, file_name))

    backup_dir_path = '{}\\{}'.format(dir_path, BACKUP_FLDR)
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    backup_name = '{}__{}.{}'.format(file_name.split('.')[0], date, file_name.split('.')[1])
    original_file_path = '{}\\{}'.format(dir_path, file_name)
    backup_file_path = '{}\\{}'.format(backup_dir_path, backup_name)

    # Actually make the backups
    if not os.path.exists(backup_dir_path):
        os.mkdir(backup_dir_path)
    shutil.copy(original_file_path, backup_file_path)


def backup_all(directory):
    """ crawl all subfolders of a given directory, making backups where appropriate """
    for (dir_path, nested_dirs, files) in os.walk(directory):
        for file_name in files:
            if is_backup_target(dir_path, file_name) and not already_backed_up(dir_path, file_name):
                backup_file(dir_path, file_name)


def main(argv):
    """ Process a command line argument, and run a backup if appropriate """
    dir_path = ''
    try:
        opts, args = getopt.getopt(argv, "hd:", ["directory="])
    except getopt.GetoptError:
        print('python BackupDrafts.py -p <directory_path>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('USAGE: python BackupDrafts.py -p <directory_path>')
            print('-------------------------------------------------------------------------------')
            print('recursively crawl a given directory')
            print('back up any documents containing the following keywords in their file name:')
            print('\t{}'.format(BACKUP_KEYWORDS))
            sys.exit()
        elif opt in ("-d", "--directory"):
            dir_path = arg
        else:
            print('bad arguments passed. Use "python BackupDrafts.py -h" for help.')
            sys.exit()

    if os.path.isdir(dir_path):
        print('backing up files in "{}" '.format(dir_path))
        backup_all(dir_path)
    else:
        print('Bad directory path: no backup performed')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
