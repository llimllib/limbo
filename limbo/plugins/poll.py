"""!poll 'question' 'option A' 'option b' ... 'option x' create a poll"""

import argparse
import json
import re
import shlex

POLL_EMOJIS = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "keycap_ten"
]

ERROR_WRONG_NUMBER_OF_ARGUMENTS = "A Poll must have at least a question and " \
    "between two to ten options"
ERROR_INVALID_FORMAT = "Sorry, your poll contains unbalanced quotation marks"

ARGPARSE = argparse.ArgumentParser()
ARGPARSE.add_argument('poll', nargs='*')


def remove_smart_quotes(text):
    return text.replace(u"\u2018", "'") \
        .replace(u"\u2019", "'") \
        .replace(u"\u201c", '"') \
        .replace(u"\u201d", '"')


def poll(poll, msg, server):
    """Given a question and answers, present a poll"""
    poll = remove_smart_quotes(poll.replace(u"\u2014", u"--"))

    try:
        args = ARGPARSE.parse_args(shlex.split(poll)).poll
    except ValueError:
        return ERROR_INVALID_FORMAT

    if not 2 < len(args) < len(POLL_EMOJIS) + 1:
        return ERROR_WRONG_NUMBER_OF_ARGUMENTS

    result = ["Poll: {}\n".format(args[0])]
    for emoji, answer in zip(POLL_EMOJIS, args[1:]):
        result.append(":{}: {}\n".format(emoji, answer))

    # for this we are going to need to post the message to Slack via Web API in order to
    #  get the TS and add reactions
    msg_posted = server.slack.post_message(
        msg['channel'], "".join(result), as_user=server.slack.username)
    ts = json.loads(msg_posted)["ts"]
    for i in range(len(args) - 1):
        server.slack.post_reaction(msg['channel'], ts, POLL_EMOJIS[i])


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!poll (.*)", text)
    if not match:
        return

    return poll(match[0], msg, server)


on_bot_message = on_message
