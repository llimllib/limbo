"""!gif <search term> return a random result from the  google gif search result for <search term>"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import re
import requests
from random import shuffle

def octal_to_html_escape(re_match):
    # an octal escape of the form '\75' (which ought to become '%3d', the
    # url-escaped form of "=". Strip the leading \
    s = re_match.group(0)[1:]

    # convert octal to hex and strip the leading '0x'
    h = hex(int(s, 8))[2:]

    return "%{0}".format(h)

def unescape(url):
    # google uses octal escapes for god knows what reason
    return re.sub(r"\\..", octal_to_html_escape, url)

def gif(searchterm, unsafe=False):
    searchterm = quote(searchterm)

    safe = "&safe=" if unsafe else "&safe=active"
    searchurl = "https://www.google.com/search?tbs=itp:animated&tbm=isch&q={0}{1}".format(searchterm, safe)

    # this is an old iphone user agent. Seems to make google return good results.
    useragent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Versio  n/4.0.5 Mobile/8A293 Safari/6531.22.7"

    result = requests.get(searchurl, headers={"User-agent": useragent}).text

    gifs = list(map(unescape, re.findall(r"var u='(.*?)'", result)))
    shuffle(gifs)

    if gifs:
        return gifs[0]
    else:
        return ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!gif (.*)", text)
    if not match:
        return

    searchterm = match[0]
    return gif(searchterm.encode("utf8"))
