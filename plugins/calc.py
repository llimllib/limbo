"""!calc <equation> will return the google calculator result for <equation>"""
from bs4 import BeautifulSoup
import re
from urllib import quote
import requests

def calc(eq):
    query = quote(eq)
    url = "https://encrypted.google.com/search?hl=en&q={}".format(query)
    soup = BeautifulSoup(requests.get(url).text)

    answer = soup.findAll("h2", attrs={"class": "r"})
    if not answer:
        print "returning a string"
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    print "returning ", answer[0].text
    return unicode(answer[0].text)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!calc (.*)", text)
    if not match: return

    return calc(match[0])
