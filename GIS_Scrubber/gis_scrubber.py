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
import openpyxl
import re

MAX_FLD_LEN = 16
END_CHR_CNT = 4

DEFAULT_DIRTY = 'dirty'
DEFAULT_CLEAN = 'clean'

TARGET_EXTENSIONS = {'txt': 'csv'
                     ,'csv': 'csv'
                     ,'tsv': 'csv'
                     ,'xlsx': 'xlsx'
                     }


def scrub_string(dirty_str):
    """
    Given a string, clean it up to match GIS conventions
    """

    if dirty_str is None:
        return None

    clean_str = str(dirty_str)

    if len(clean_str) > 0 and clean_str[0] is '=':
        return clean_str

    # no special characters
    clean_str = re.sub(r'[^a-zA-Z0-9_]', '_', clean_str)

    # move leading numbers to the end
    matches = re.match(r'[\d_]+', clean_str)
    if matches is not None:
        leading_nums = matches.group()
        clean_str = clean_str[len(leading_nums):] + '_' + leading_nums

    # If the leading character is _still_ a number, add a filler character
    if len(clean_str) > 0 and clean_str[0] in "0123456789_":
        clean_str = "N" + clean_str

    # remove double-underscores
    clean_str = re.sub(r'_+', '_', clean_str)

    # no leading or trailing underscores
    clean_str = re.sub(r'^_*', '', clean_str)
    clean_str = re.sub(r'_+$', '', clean_str)

    # limit header lengths
    if len(clean_str) > MAX_FLD_LEN:
        clean_str = clean_str[:MAX_FLD_LEN - END_CHR_CNT - 1] + '_' + clean_str[-END_CHR_CNT:]

    # remove double-underscores (again)
    clean_str = re.sub(r'_+', '_', clean_str)

    return clean_str


def scrub_headers(header_list):
    """
    Given list of header strings, scrub its string contents, and return the scrubbed list
    """
    scrubbed_header = []
    for entry in header_list:
        scrubbed_header.append(scrub_string(entry))
    return scrubbed_header


def scrub_xlsx(dir_dirty, infile_name, dir_clean):
    """
    Scrub an Excel file
    """
    infile_path = r"{}\{}".format(dir_dirty, infile_name)
    outfile_path = r"{}\{}".format(dir_clean, infile_name)

    print(r'Scrubbing "{}":'.format(infile_path))


    wb = openpyxl.load_workbook(infile_path)
    for sheet in wb:
        print('\t Scrubbing Sheet: {}'.format(sheet.title))

        sheet_name_errors = False
        scrubbed_title = scrub_string(sheet.title)
        if scrubbed_title != sheet.title:
            sheet_name_errors = True
            sheet.title = scrubbed_title

        header_errors = False
        for cell in sheet.rows[0]:
            scrubbed_value = scrub_string(cell.value)
            if scrubbed_value != cell.value:
                header_errors = True
                cell.value = scrubbed_value

        if sheet_name_errors:
            print("\t\tSHEET NAME ERRORS FOUND AND CORRECTED.")

        if header_errors:
            print("\t\tHEADER ERRORS FOUND AND CORRECTED.")


    wb.save(outfile_path)
    print('\tNew file located at "{}\\{}"\n'.format(dir_clean, outfile_path))


def scrub_csv(dir_dirty, infile_name, dir_clean):
    """
    Scrubs a CSV-formatted file
    """

    infile_path = r'{}\{}'.format(dir_dirty, infile_name)
    outfile_path = scrub_string(infile_name.split('.')[0]) + '.' + infile_name.split('.')[-1]
    outfile = r'{}\{}'.format(dir_clean, outfile_path)

    print(r'Scrubbing "{}":'.format(infile_path))
    filename_errors = infile_name == outfile_path
    header_errors = False

    with open(infile_path) as d_file, open(outfile, 'w', newline='\n') as c_file:
        dialect = csv.Sniffer().sniff(d_file.read(1024))
        d_file.seek(0)
        reader = csv.reader(d_file, dialect)
        writer = csv.writer(c_file, dialect)

        # Process the header
        header = next(reader)
        scrubbed_header = scrub_headers(header)
        if scrubbed_header != header:
            header_errors = True
        writer.writerow(scrubbed_header)

        # write the remaining data to the file verbatim
        for row in reader:
            writer.writerow(row)

    if filename_errors:
        print("\tFILENAME ERRORS FOUND AND CORRECTED.")

    if header_errors:
        print("\tHEADER ERRORS FOUND AND CORRECTED.")

    print('\tNew file located at "{}\\{}"\n'.format(dir_clean, outfile_path))


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
        if scrub_method == 'xlsx':
            scrub_xlsx(dir_dirty, filename, dir_clean)
    elif filename != '_empty':  # Don't give warnings for the filler file
        print(r'WARNING: DID NOT SCRUB "{}\{}"!'.format(dir_dirty, filename))
        print('\tREASON: FILE TYPE NOT SUPPORTED\n')


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
    """
    Process a command line arguments and begin scrubbing data files if appropriate
    """
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
