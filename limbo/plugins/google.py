"""!search <query> will return the top google result for that query (!google is an alias)"""
from bs4 import BeautifulSoup
import re
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests


def google(q):
    query = quote(q)
    url = "https://encrypted.google.com/search?q={0}".format(query)
    soup = BeautifulSoup(requests.get(url).text, "html5lib")

    answer = soup.findAll("h3", attrs={"class": "r"})
    if not answer:
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    try:
        return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])
    except IndexError:
        # in this case there is a first answer without a link, which is a
        # google response! Let's grab it and display it to the user.
        return ' '.join(answer[0].stripped_strings)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:google|search) (.*)", text)
    if not match:
        return

    return google(match[0])


on_bot_message = on_message
