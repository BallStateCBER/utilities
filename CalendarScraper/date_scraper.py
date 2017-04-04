

from bs4 import BeautifulSoup
import requests
import datetime
import csv
import sys
import os
import getopt

today = datetime.datetime.now().strftime(r'%Y-%m-%d')
RESULTS_DIR = 'results'
BEA_OUTFILE = 'BEA_Updates_{}.csv'.format(today)
BLS_OUTFILE = 'BLS_Updates_{}.csv'.format(today)
CB_ECON_IND_OUTFILE = 'CB_Economic_Indicator_Updates_{}.csv'.format(today)


def get_bls_release_calendar(
            year=datetime.datetime.now().year
            ,outfile=BLS_OUTFILE
        ):
    """
    Scrape the BLS release calendar from their website

    :param year: which year's calendar to read (defaults to current year)
    :param outfile: what to name the csv output file (has a default value)
    """

    url = 'http://www.bls.gov/schedule/{}/home.htm'.format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    releases_odd = soup.find_all('tr', {'class': ['release-list-odd-row']})
    releases_even = soup.find_all('tr', {'class': ['release-list-even-row']})
    releases = releases_odd + releases_even

    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['Date', 'Time', 'Release'])
        writer.writeheader()
        for release in releases:
            date = release.find('td', {'class': 'date-cell'}).text
            time = release.find('td', {'class': 'time-cell'}).text
            desc = release.find('td', {'class': 'desc-cell'}).text
            if time.strip() != '':
                writer.writerow({'Date': date, 'Time': time, 'Release': desc})


def get_bea_release_calendar(
            year=datetime.datetime.now().year
            ,outfile=BEA_OUTFILE
        ):
    """
    Scrape the BEA release calendar from their website

    :param year: which year's calendar to read (defaults to current year)
    :param outfile: what to name the csv output file (has a default value)
    """

    url = 'http://www.bea.gov/newsreleases/{}rd.htm'.format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['Date', 'Time', 'Release'])
        writer.writeheader()
        for r_id, row in enumerate(soup.find_all('tr')):
            cells = row.find_all('td')
            if r_id != 0 and len(cells) == 4:
                desc = cells[1].text
                date = str.replace(cells[2].text, ' New!','')
                time = cells[3].text
                if time.strip() != '':
                    writer.writerow({'Date': date, 'Time': time, 'Release': desc})


def get_cb_econ_release_calendar(
            year=datetime.datetime.now().year
            ,outfile=CB_ECON_IND_OUTFILE
        ):
    """
    Scrape the Census Bureau's Economic Indicators release calendar from their website

    :param year: which year's calendar to read (defaults to current year)
    :param outfile: what to name the csv output file (has a default value)
    """

    url = 'https://www.census.gov/economic-indicators/calendar-listview-{}.html'.format(year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['Date', 'Time', 'Release'])
        writer.writeheader()
        for r_id, row in enumerate(soup.find_all('tr')):
            cells = row.find_all('td')
            if r_id != 0 and len(cells) == 4:
                desc = '{}, {}'.format(cells[0].text, cells[3].text)
                date = str.replace(cells[1].text, ' New!', '')
                time = cells[2].text
                if time.strip() != '':
                    writer.writerow({'Date': date, 'Time': time, 'Release': desc})


def main(argv):
    """
    The main entry point of the code

    :param argv:
    """
    year = None
    try:
        opts, args = getopt.getopt(argv, "hy:", [])
    except getopt.GetoptError:
        print('type "python date_scraper.py -h" for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python date_scraper.py -y <year>\n')
            print('a utility for automatically crawling commonly referenced release calendars')
            print('OPTIONS:')
            print('\t-y the year you wish to crawl for (defaults to the current year)')
            print('\t-h display the help text for date_scraper.py')
            sys.exit()
        elif opt == '-y':
            year = arg
        else:
            print('Bad inputs. Try "python date_scraper.py -h" for help.')
            sys.exit()

    if year is None:
        print('No year provided. Scraping calendar releases in the current year.')
        year = datetime.datetime.today().strftime('%Y')

    if not os.path.exists(RESULTS_DIR):
        os.mkdir(RESULTS_DIR)

    try:
        destination = '{}/{}_{}'.format(RESULTS_DIR, year, BLS_OUTFILE)
        get_bls_release_calendar(year, destination)
        print('BLS Calendar scraped and saved to {}'.format(destination))
    except:
        print('Something went wrong with the BLS scrape.')

    try:
        destination = '{}/{}_{}'.format(RESULTS_DIR, year, BEA_OUTFILE)
        get_bea_release_calendar(year, destination)
        print('BEA Calendar scraped and saved to {}'.format(destination))
    except:
        print('Something went wrong with the BEA scrape.')

    try:
        destination = '{}/{}_{}'.format(RESULTS_DIR, year, CB_ECON_IND_OUTFILE)
        get_cb_econ_release_calendar(year, destination)
        print('Census Economic Indicators Calendar scraped and saved to {}'.format(destination))
    except:
        print('Something went wrong with the Census Bureau  Economic Indicators scrape.')

if __name__ == '__main__':

    main(sys.argv[1:])

