"""!wiki <topic> returns a wiki link for <topic>"""
import json
import re
from urllib import quote
import sys

import requests
from bs4 import BeautifulSoup

def wiki(searchterm):
    """return the top wiki search result for the term"""
    searchterm = quote(searchterm)

    url = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={0}&format=json"
    url = url.format(searchterm)

    result = requests.get(url).json()

    pages = result["query"]["search"]

    # try to reject disambiguation pages
    pages = [p for p in pages if not 'may refer to' in p["snippet"]]

    if not pages:
        return ""

    page = quote(pages[0]["title"].encode("utf8"))
    link = "http://en.wikipedia.org/wiki/{0}".format(page)

    r = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=parse&page={}".format(page)).json()
    soup = BeautifulSoup(r["parse"]["text"]["*"])
    p = str(soup.find('p'))
    p = re.sub('href="(.[^\/])', r'href="http://en.wikipedia.org\1', p)
    p = p[:8000]

    return p

def on_message(msg):
    text = msg.get("text", "")
    match = re.findall(r"!wiki (.*)", text)
    if not match: return

    searchterm = match[0]
    return wiki(searchterm)
