"""!emoji <n> will return n random emoji"""
import json
import re
import random
from time import time
from emojicodedict import emojiCodeDict

EMOJI = None


class EmojiCache(object):
    def __init__(self, server):
        self.server = server
        self.last_updated = 0
        self.emoji = []

    def __len__(self):
        return len(self.emoji)

    def __getitem__(self, idx):
        return self.emoji[idx]

    def __setitem__(self, idx, val):
        self.emoji[idx] = val

    def get(self, n):
        if time() - self.last_updated > 60 * 60:
            self.update()
            self.last_updated = time()
        random.shuffle(self.emoji)
        return "".join(self.emoji[:n])

    def update(self):
        self.emoji = list(emojiCodeDict.keys())
        emoji_res = json.loads(self.server.slack.api_call("emoji.list"))
        for emo in emoji_res["emoji"]:
            url = emoji_res["emoji"][emo]
            emoji = ":{}:".format(emo)
            # duplicate emoji will start with "alias:" instead of an "http"; we
            # don't want to include dupes in our list so we don't bias towards them
            # https://api.slack.com/methods/emoji.list
            if url.startswith("http") and emoji not in emojiCodeDict:
                self.emoji.append(emoji)


def emoji_list(server, n=1):
    """return a list of `n` random emoji"""
    global EMOJI
    if EMOJI is None:
        EMOJI = EmojiCache(server)
    return EMOJI.get(n)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(!emoji)\s*(\d+)*", text)
    if not match:
        return

    n = 1 if not match[0][1] else int(match[0][1])

    return emoji_list(server, n)


on_bot_message = on_message
