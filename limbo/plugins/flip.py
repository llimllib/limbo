"""!flip [alpha,beta,gamma] - flip a coin n times or shuffle a comma separated list"""
import random
import re

def flip(lst):
    random.shuffle(lst)
    return ", ".join(lst)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!flip( .*)?", text)
    if not match:
        return

    lst = ["heads", "tails"] if not match[0] else match[0].strip().split(',')

    return flip(lst)
