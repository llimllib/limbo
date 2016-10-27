"""!geocities <search term> return a gif from the internet archive's geocities collection"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import re
import requests
from random import shuffle

def gif(searchterm, unsafe=False):
    searchterm = quote(searchterm)
    searchurl = "https://wbgrp-svc060.us.archive.org/api/v1/gifsearch?q={0}&notrack=1".format(searchterm)
    results = requests.get(searchurl).json()
    gifs = list(map(lambda x: "https://web.archive.org/web/{0}".format(x['gif']), results))
    shuffle(gifs)

    if gifs:
        return gifs[0]
    else:
        return ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!geo.* (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return gif(searchterm.encode("utf8"))
