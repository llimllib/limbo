"""!commit returns a useful commit message"""
import re
import requests


def commit():
    return requests.get("http://whatthecommit.com/index.txt").text


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!commit( .*)?", text)
    if not match:
        return

    return commit()


on_bot_message = on_message
