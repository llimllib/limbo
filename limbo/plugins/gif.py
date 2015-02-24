"""
!gif <search term> return a random result from the google gif search result for <search term>
!gif or !hitme to return another result for the same query
"""

from urllib import quote
import logging
import re
import requests
from random import shuffle

logger = logging.getLogger(__name__)

_last_gifs = []


def gif(searchterm, unsafe=False):
    global _last_gifs
    searchterm = quote(searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    _last_gifs = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(_last_gifs)
    one = _last_gifs.pop()
    logger.debug("got %d gifs, chose=%r", len(_last_gifs)+1, one)
    return one


def on_message(msg, server):
    global _last_gifs
    one = None
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if match:
        searchterm = match[0]
        one = gif(searchterm)
    elif re.findall(r"!gif$", text) or re.findall(r"!hitme$", text):
        if len(_last_gifs) > 0:
            # todo: re-query if we run out
            one = _last_gifs.pop()
            logger.debug("have %d gifs, chose=%r", len(_last_gifs)+1, one)
        else:
            logger.debug("ran out of gifs!")
    return one if one else ""
