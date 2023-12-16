#!/usr/bin/python3

import urllib.request
from bs4 import BeautifulSoup

def import_campaigns(page = 1):
    url = 'https://orokos.com/roll/?action=view_all&offset='+str((page-1)*20)
    raw_html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(raw_html, 'html.parser')
    campaigns = set(map(lambda elt: elt['href'], soup.css.select('a[href^="c-"]')))
    return campaigns

if __name__ == "__main__":
    campaigns = set()

    for i in range(1, 50000):
        new_campaigns = import_campaigns(i+1)
        campaigns = campaigns.union(new_campaigns)

    with open('campaigns.txt', 'w') as f:
        for line in sorted(campaigns):
            f.write(f"{line}\n")
