"""!wiki <topic> returns a wiki link for <topic>"""
import re
try:
    from urllib import quote
except ImportError:
    from urllib.request import quote

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
    pages = [p for p in pages if 'may refer to' not in p["snippet"]]

    if not pages:
        return ""

    page = quote(pages[0]["title"].encode("utf8"))
    link = "http://en.wikipedia.org/wiki/{0}".format(page)

    r = requests.get(
        "http://en.wikipedia.org/w/api.php?format=json&action=parse&page={0}".
        format(page)).json()
    soup = BeautifulSoup(r["parse"]["text"]["*"], "html5lib")
    p = soup.find('p').get_text()
    p = p[:8000]

    return u"{0}\n{1}".format(p, link)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!wiki (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return wiki(searchterm.encode("utf8"))


on_bot_message = on_message
