"""!stock <search term> return a stock photo for <search term>"""

from random import shuffle
import re
try:
    from urllib import quote
except ImportError:
    from urllib.request import quote

import requests
from bs4 import BeautifulSoup

def stock(searchterm):
    searchterm = quote(searchterm)
    url = "http://www.shutterstock.com/cat.mhtml?searchterm={0}&search_group=&lang=en&language=en&search_source=search_form&version=llv1".format(searchterm)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    images = [x["src"] for x in soup.select(".gc_clip img")]
    shuffle(images)

    return images[0] if images else ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!stock (.*)", text)
    if not match:
        return

    return stock(match[0].encode("utf8"))
