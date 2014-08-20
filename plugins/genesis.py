from bs4 import BeautifulSoup
from urllib import quote
import re
import requests
from random import shuffle, randint

def genesis():
    page = randint(1,8)
    r = requests.get("https://secure.flickr.com/photos/textfiles/sets/72157646180733361/page%s/"%page)
    soup = BeautifulSoup(r.text)
    images = soup.findAll("img", attrs={"data-defer-src": True})
    images = [i.attrs["data-defer-src"] for i in images]

    shuffle(images)

    return images[0] if images else ""

def on_message(msg, server):
    return genesis()
