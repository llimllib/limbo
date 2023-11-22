"""!or option1 or option2 or option3 - returns one of the options in a random way"""
import random
import re


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!or (.+)", text)
    if not match:
        return
    options = re.split(" or ", match[0].strip())

    return random.choice(options)


on_bot_message = on_message
