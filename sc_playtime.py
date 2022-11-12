import os
import re
import glob
import dateutil.parser
from colorama import Fore
from datetime import timedelta
from easygui import diropenbox
white = Fore.LIGHTWHITE_EX
pink = Fore.LIGHTMAGENTA_EX

"""Readme

This is a playtime calculator for Star Citizen. It works by reading all log files and getting the timestamps from them

If you deleted your StarCitizen/Live folder in the past, it sadly wont be accurate. I suggest just deleting the files, but keeping the "logbackups" folder intact :)

XOXO ClaraCrazy
"""

def get_files(search_dir):
    os.chdir(search_dir)
    globlog = glob.glob("*.log")
    files = [os.path.join(search_dir, f) for f in globlog] # add path to each file
    os.chdir("..")
    recent_session_file = [os.path.join(os.path.abspath(os.curdir), f) for f in globlog]
    files += recent_session_file
    return files

def extract_dates(contents):
    dates = []
    for line in contents:
        match= re.search(r'^<(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*',line)
        if match:
            dates.append(match.group(1))
    return dates

def convert_to_datetime(s):
    return dateutil.parser.parse(s, fuzzy=True)

def get_totals(path):
    total_deltas = timedelta()
    for file in get_files(path):
        fhandle = open(file,'r')
        text_content = fhandle.read().split("\n")
        dates = extract_dates(text_content)
        if len(dates) > 0:
            start_log = convert_to_datetime(dates[0])
            end_log = convert_to_datetime(dates[-1])
            delta = end_log-start_log
            total_deltas += delta
    totsec = total_deltas.total_seconds()
    h = totsec//3600
    m = (totsec%3600) // 60
    sec =(totsec%3600)%60 #just for reference
    total_deltas = f"{pink}{int(h)}{white}hour{'s' if not int(h) == 1 else ''}, {pink}{int(m)}{white}minute{'s' if not int(m) == 1 else ''} and {pink}{int(sec)}{white}second{'s' if not int(sec) == 1 else ''}"
    return total_deltas

def just_do_it(path):
    totals = get_totals(path)
    print(f"\n{white}Congrats, Soldier. You have served for " + totals)

def main():
    os.system("cls")
    os.system("title Star Citizen Playtime Calculator")
    print("Please select your Install folder for StarCitizen (RSI/StarCitizen/Live)")
    path = diropenbox("Please Select your RSI Install folder here", "Select RSI Folder", 'C:\\')
    path = f"{path}/logbackups"
    os.system("cls")
    just_do_it(path)

if __name__ == '__main__':
    main()