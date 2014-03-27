import re
from urllib import quote

import requests

def youtube(searchterm):
    searchterm = quote(searchterm)
    url = "https://gdata.youtube.com/feeds/api/videos?q={}&orderBy=relevance&alt=json"
    url = url.format(searchterm)

    j = requests.get(url).json()

    results = j["feed"]
    if "entry" not in results:
        return "sorry, no videos found"

    video = results["entry"][0]["link"][0]["href"]
    video = re.sub("&feature=youtube_gdata", "", video)

    return video

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!youtube (.*)", text)
    if not match: return

    searchterm = match[0]
    return youtube(searchterm)
