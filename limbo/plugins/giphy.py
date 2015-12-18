"""!gif <search term> return a random result from the  google gif search result for <search term>"""

import re
from safygiphy import Giphy
import json

def gif(searchterm, rating="pg-13"):
    g=Giphy()
    res = g.random(tag=searchterm, rating=rating)
    print res
    try:
        return str(res['data']['image_url'])
    except TypeError:
        return "Oops, no Gifs found for the tag {}. Please try a different tag".format(searchterm)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return gif(searchterm.encode("utf8"))


