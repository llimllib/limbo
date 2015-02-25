"""!emoji <n> will return n random emoji"""
import re
import random
from emojicodedict import emojiCodeDict

def randomelt(dic):
    keys = dic.keys()
    i = random.randint(0, len(keys) - 1)
    return dic[keys[i]]

def emoji(n=1):
    emoji = []
    for i in range(n):
        emoji.append(randomelt(emojiCodeDict))

    return "".join(emoji)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(!emoji)\s*(\d+)*", text)
    if not match:
        return

    n = 1 if not match[0][1] else int(match[0][1])

    return emoji(n)
