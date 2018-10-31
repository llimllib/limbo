"""posts titles of imagur images if exist when a link is posted"""
import re
import requests
from bs4 import BeautifulSoup


regex = re.compile("\\.imgur\\.com/(.+)\\..+", re.IGNORECASE)

generic_imgur_title = "Imgur: The most awesome images on the Internet".lower()


def get_image_title(url):
     soup = BeautifulSoup(requests.get(url).text, "html5lib")
     return soup.title.text.strip()


def on_message(msg, server):
    text = msg.get("text", "")
    match = regex.findall(text)
    if not match or len(match) < 1:
        return
    image_title = get_image_title("https://imgur.com/{}".format(match[0]))
    if not isGenericTitle(image_title):
        return image_title


def isGenericTitle(title):
    """
    :type title: str
    """
    if title.lower() == generic_imgur_title:
        return True
    else:
        return False