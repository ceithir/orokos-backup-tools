#!/usr/bin/python3

# Ref: https://www.geeksforgeeks.org/convert-html-table-into-csv-file-in-python/

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from pathvalidate import sanitize_filename
from urllib.parse import unquote_plus

def import_rolls(campaign, page = 1):
    offset = (page-1)*20
    url = f'https://orokos.com/roll/{campaign}?offset={str(offset)}'
    raw_html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(raw_html,'html.parser')

    table = soup.find("table")
    if not table:
        return []

    data = []
    for element in table.find_all("tr")[1:]:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    return data

def export_csv(campaign):
    page = 1
    all_rolls = []

    while True:
        current_rolls = import_rolls(campaign, page)
        if not current_rolls:
            break
        all_rolls += current_rolls
        page += 1

    dataFrame = pd.DataFrame(
        all_rolls,
        columns = ['Time', 'Roller', 'Character','Campaign', 'Description', 'Results']
    )
    filename = sanitize_filename(unquote_plus(campaign[2:]))
    dataFrame.to_csv(
        f'rolls/{filename}.csv',
        index = False
    )

if __name__ == "__main__":
    campaign = 'c-Children+of+the+Sky'

    export_csv(campaign)
