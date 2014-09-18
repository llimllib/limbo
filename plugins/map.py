# -*- coding: utf-8 -*-
"""!map <place> return a map of place. Optional "zoom" and "maptype" parameters are accepted."""
# example queries:
# !map new york city
# !map united states zoom=4
# !map united states zoom=4 maptype=satellite

from urllib import quote
import re

def makemap(query):
    querywords = []
    args = {
        "zoom": 13,
        "maptype": "roadmap",
    }
    for word in query.split(" "):
        if '=' in word:
            opt, val = word.split("=")
            args[opt] = val
        else:
            querywords.append(word)

    query = quote(" ".join(querywords))

    # Slack seems to ignore the size param?
    url = "https://maps.googleapis.com/maps/api/staticmap?center={}&zoom={}&size=800x400&&maptype={}"
    url = url.format(query, args["zoom"], args["maptype"])

    return url

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!map (.*)", text)
    if not match: return

    return makemap(match[0])
