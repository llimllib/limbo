"""!youtube <search term> return the first youtube search result for <search term>"""

import re
try:
    from urllib import quote
except ImportError:
    from urllib.request import quote

import requests

def youtube(searchterm):
    url = "https://www.youtube.com/results?search_query={0}"
    url = url.format(quote(searchterm))

    r = requests.get(url)
    results = re.findall('a href="(/watch[^&]*?)"', r.text)

    if not results:
        return "sorry, no videos found"

    return "https://www.youtube.com{0}".format(results[0])

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!youtube (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return youtube(searchterm.encode("utf8"))

on_bot_message = on_message
