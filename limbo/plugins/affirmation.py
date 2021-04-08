"""!affirmation to combat against imposter syndrome"""
import re
import requests

def affirmation():
    return requests.get("https://www.affirmations.dev").json()["affirmation"]
       
def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!affirmation( .*)?", text)
    if not match:
        return
    return affirmation()


on_bot_message = on_message
