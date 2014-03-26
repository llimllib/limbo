"""!gif <search term> return the first google gif search result for <search term>"""

import urllib2
from urllib import quote
import re
from random import shuffle

def gif(searchterm, unsafe=False):
    searchterm = quote(searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]
    result = opener.open(searchurl).read()

    gifs = re.findall(r'imgurl.*?(http.*?)\\', result)
    shuffle(gifs)

    return gifs[0] if gifs else ""

def on_message(msg):
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if not match: return

    searchterm = match[0]
    return gif(searchterm)
