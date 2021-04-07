"""!cat returns an image of a cat"""
import re
import requests


def cat():
    return requests.get("https://api.thecatapi.com/v1/images/search").json()[0]["url"]


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!cat( .*)?", text)
    if not match:
        return

    return cat()


on_bot_message = on_message
