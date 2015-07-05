"""!giphy <search term> return a random result from the giphy library, with the tag <search term>"""

import re
from safygiphy import Giphy
import json

def gif(searchterm, rating="pg-13"):
    g=Giphy()
    gif = g.random(tag=searchterm, rating=rating)
    try:
        return str(gif['data']['image_url'])
    except TypeError:
        return "Oops, No gifs found for that tag. Try again!"
    except Exception:
        return "Oops, something went wrong. Contact your admin if this happens again!" # Better than crashing the entire script

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!giphy (.*)", text)
    if not match:
        return
    searchterm = match[0]
    return gif(searchterm.encode("utf8"))


