"""!gif <search term> return a random result from the  google gif search result for <search term>"""

import re
from safygiphy import Giphy
import json

def gif(searchterm, rating="pg-13"):
    g=Giphy()
    gif = g.random(tag=searchterm, rating=rating)
    try:
        return str(gif['data']['image_url'])
    except Exception:
        return "Oops, Something went wrong, please try again. Sucker"

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if not match:
        return
    searchterm = match[0]
    return gif(searchterm.encode("utf8"))


