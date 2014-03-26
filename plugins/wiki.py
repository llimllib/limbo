"""!wiki <topic> returns a wiki link for <topic>"""
import sys
import argparse
import requests
from urllib import quote
import re
import json

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

    return link

def on_message(msg):
    text = msg.get("text", "")
    match = re.findall(r"!wiki (.*)", text)
    if not match: return

    searchterm = match[0]
    return wiki(searchterm)
