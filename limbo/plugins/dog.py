"""!dog returns an image of a doggo or puppo."""
import re
import requests


def dog():
    return requests.get("https://dog.ceo/api/breeds/image/random").json()[
        'message']


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!dog( .*)?", text)
    if not match:
        return

    return dog()


on_bot_message = on_message
