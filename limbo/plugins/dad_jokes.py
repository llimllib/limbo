"""!dad_joke returns a dad joke"""
import re
import requests


def dad_joke():
    headers = {'Accept': 'application/json'}
    return requests.get("https://icanhazdadjoke.com/", headers=headers).json()["joke"]


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!dad_joke( .*)?", text)
    if not match:
        return

    return dad_joke()


on_bot_message = on_message
