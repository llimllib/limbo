"""!poll 'question' 'option A' 'option b' ... 'option x' create a poll"""

import re
import requests
import json

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten"]


def poll(question, answers, msg, server):
    result = "Poll: {}\n".format(question)
    for i in range(len(answers)):
        result += ":{}: {}\n".format(numbers[i], answers[i])
    
    # for this we are going to need to post the message to Slack via Web API in order to
    #  get the TS and add reactions
    msg_posted = server.slack.post_message(
            msg['channel'],
            result,
            as_user=server.slack.username)
    ts = json.loads(msg_posted)["ts"]
    for i in range(len(answers)):
        server.slack.post_reaction(msg['channel'], ts, numbers[i])


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!poll (.*)", text)
    if not match:
        return

    text = match[0]
    blocks = text.split()
    blocks = map(lambda x: x[1:-1], blocks)
    if len(blocks) < 3:
        return  # needs at least a question and 2 options to choose from
    return poll(blocks[0], blocks[1:], msg, server)


on_bot_message = on_message
