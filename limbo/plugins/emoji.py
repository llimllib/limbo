"""!emoji <n> will return n random emoji"""
import json
import re
import random
from emojicodedict import emojiCodeDict

ALL_EMOJI = None

def randomelt(dic):
    """return a random element from a dictionary with replacement"""
    keys = list(dic.keys())
    i = random.randint(0, len(keys) - 1)
    return dic[keys[i]]

def get_custom_emoji(server):
    """get a workspace's custom emoji and store them in ALL_EMOJI"""
    global ALL_EMOJI
    ALL_EMOJI = list(emojiCodeDict.keys())

    emoji_res = json.loads(server.slack.api_call("emoji.list"))
    for emo in emoji_res["emoji"]:
        url = emoji_res["emoji"][emo]
        emoji = ":{}:".format(emo)
        # duplicate emoji will start with "alias:" instead of an "http"; we
        # don't want to include dupes in our list so we don't bias towards them
        # https://api.slack.com/methods/emoji.list
        if url.startswith("http") and emoji not in emojiCodeDict:
            ALL_EMOJI.append(emoji)

def emoji_list(server, n=1):
    """return a list of `n` random emoji"""
    if ALL_EMOJI is None:
        get_custom_emoji(server)
    random.shuffle(ALL_EMOJI)
    return "".join(ALL_EMOJI[:n])

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(!emoji)\s*(\d+)*", text)
    if not match:
        return

    n = 1 if not match[0][1] else int(match[0][1])

    return emoji_list(server, n)

on_bot_message = on_message
