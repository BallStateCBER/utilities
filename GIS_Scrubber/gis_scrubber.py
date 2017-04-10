"""
Purpose: Read in data files (csv's and excel docs) intended for GIS use.
    Scrub these documents to remove invalid characters, formats, etc.

Author: Brandon Patterson

Notes: Only scrubs the contents of the current directory (no subfolders)
"""

import os
import sys
import getopt
import csv
import re

MAX_FLD_LEN = 16
END_CHR_CNT = 4

DEFAULT_DIRTY = 'dirty'
DEFAULT_CLEAN = 'clean'

TARGET_EXTENSIONS = {'txt': 'csv'
                     ,'csv': 'csv'
                     ,'tsv': 'csv'
                     # ,'xls': 'xls'
                     # ,'xlsx': 'xlsx'
                     }


def scrub_header(header_list):
    """
    Given a header as a listlist, scrub its string contents, and return the scrubbed list
    """
    scrubbed_header = []
    for entry in header_list:
        # no special characters
        new_entry = re.sub(r'[^a-zA-Z0-9_]', '_', entry)

        # no leading underscores
        new_entry = re.sub(r'^_*', '', new_entry)

        # limit header lengths
        if len(new_entry) > MAX_FLD_LEN:
            new_entry = new_entry[:MAX_FLD_LEN - END_CHR_CNT - 1] + '_' + new_entry[-END_CHR_CNT:]

        # add scrubbed entry to the list
        scrubbed_header.append(new_entry)
    return scrubbed_header


def scrub_csv(dir_dirty, filename, dir_clean):
    """ Scrubs a CSV-formatted file """

    infile = r'{}\{}'.format(dir_dirty, filename)
    outfile = r'{}\{}'.format(dir_clean, filename)
    print(r'Scrubbing {}:'.format(infile))

    header_errors = False

    with open(infile) as d_file, open(outfile, 'w', newline='\n') as c_file:
        dialect = csv.Sniffer().sniff(d_file.read(1024))
        d_file.seek(0)
        reader = csv.reader(d_file, dialect)
        writer = csv.writer(c_file, dialect)

        header = next(reader)
        scrubbed_header = scrub_header(header)
        if scrubbed_header != header:
            header_errors = True
        writer.writerow(scrubbed_header)

        for row in reader:
            # TODO: are there any restrictions on DATA characters/length?
            writer.writerow(row)

    if header_errors:
        print("\tHeader errors found and fixed.")
    else:
        print("\tNo header errors found.")


def scrub_file(dir_dirty, filename, dir_clean):
    """
    Scrub a file in a dirty directory, placing the cleaned file in the clean directory
    (Assumes the existence of both given directories)

    :param dir_dirty: the directory where the file is located
    :param filename: the name of the file to be scrubbed
    :param dir_clean: the directory where the cleaned file should be placed
    """

    ext = filename.split('.')[-1]
    if ext in TARGET_EXTENSIONS:
        scrub_method = TARGET_EXTENSIONS[ext]
        if scrub_method == 'csv':
            scrub_csv(dir_dirty, filename, dir_clean)
        # if scrub_method == 'xls':
        #     scrub_xls(dir_dirty, filename, dir_clean)
        # if scrub_method == 'xlsx':
        #     scrub_xlsx(dir_dirty, filename, dir_clean)


def scrub_directory(dir_dirty, dir_clean):
    """
    Given a `dirty` and `clean` directory,
        scrub data files in the `dirty` directory, and output them into `clean`
    """
    if not os.path.exists(dir_dirty):
        print('The specified "dirty" directory does not exist. Exiting')
        sys.exit(2)
    if not os.path.exists(dir_clean):
        print('The specified "clean" directory does not exist. Creating it.')
        os.mkdir(dir_clean)

    for file in os.listdir(dir_dirty):
        scrub_file(dir_dirty, file, dir_clean)


def main(argv):
    """ Process a command line arguments and begin scrubbing data files if appropriate """
    dir_dirty = DEFAULT_DIRTY
    dir_clean = DEFAULT_CLEAN

    try:
        opts, args = getopt.getopt(argv, "hc:d:", [])
    except getopt.GetoptError:
        print('python gis_scrubber.py -d <dirty_files_directory> -c <clean_files_directory>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('USAGE: python gis_scrubber.py -d <dirty_files_directory> -c <clean_files_directory>')
            print('-------------------------------------------------------------------------------')
            print('scrub any data files in the given dirty directory,')
            print('output scrubbed files into the given clean directory\n')
            print('\tdefault dirty directory: {}'.format(DEFAULT_DIRTY))
            print('\tdefault clean directory: {}'.format(DEFAULT_CLEAN))
            sys.exit()
        elif opt == "-d":
            dir_dirty = arg
        elif opt == "-c":
            dir_clean = arg
        else:
            print('bad arguments passed. Use "python BackupDrafts.py -h" for help.')
            sys.exit()

    if os.path.isdir(dir_dirty):
        print('Scrubbing files in `{}`...\n'.format(dir_dirty))
        scrub_directory(dir_dirty, dir_clean)
    else:
        print('Bad directory path: no files were scrubbed')
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])