echo off

REM Purpose: proved a user-friendly way to run the web scraper for economic data release dates
REM Author: Brandon Patterson


REM scrape the economic release calendars for the current year by default
python date_scraper.py


REM scrape the calendars for a year of your choosing
REM python date_scraper.py -y 2016


pause
