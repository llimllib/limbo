"""!image <search term> return a random result from the google image search result for <search term>"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import json
import re
from random import shuffle

import requests


def unescape(url):
    # for unclear reasons, google replaces url escapes with \x escapes
    return url.replace(r"\x", "%")


def image(search, unsafe=False):
    """given a search string, return a image URL via google search"""
    searchb = quote(search.encode("utf8"))

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbm=isch&q={0}{1}".format(
        searchb, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us)" \
        " AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    images = list(map(unescape, re.findall(r"imgres[?]imgurl=(.*?)&amp;", result)))
    shuffle(images)

    if images:
        return images[0]
    return ""


def on_message(msg, server):
    """handle a message and return an image"""
    text = msg.get("text", "")
    match = re.findall(r"!image (.*)", text)
    if not match:
        return

    res = image(match[0])
    if not res:
        return

    attachment = {
        "fallback": match[0],
        "title": match[0],
        "title_link": res,
        "image_url": res
    }
    server.slack.post_message(
        msg['channel'],
        '',
        as_user=server.slack.username,
        attachments=json.dumps([attachment]))


on_bot_message = on_message
