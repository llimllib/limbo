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
    url = "https://www.shutterstock.com/search?searchterm={0}".format(
        searchterm)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html5lib")
    images = ["https:" + x["src"] for x in soup.select(".img-wrap img")]
    shuffle(images)

    return images[0] if images else ""


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!stock (.*)", text)
    if not match:
        return

    return stock(match[0].encode("utf8"))


on_bot_message = on_message
