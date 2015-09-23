"""!github <command> <arguments> is a command line interface to github

like, document the commands and arguments here or something"""

import json
import os
import re

import requests

HUB_URL = 'https://api.github.com/{}'

class Github(object):
    def __init__(self, username, password):
        self.auth = username, password

    def _get(self, url_fragment):
        return requests.get(
                 HUB_URL.format(url_fragment),
                 auth=self.auth
               ).json()

    def issues(self, repo):
        # defaults to only open issues
        return self._get('repos/{}/issues'.format(repo))

HUB = Github(os.environ.get("GITHUB_USER"), os.environ.get("GITHUB_PASS"))

def github(cmd, *args):
    if cmd == "issues":
        issues = HUB.issues(args[0])

        l = len(issues)
        if l > 5:
            text = "{} open issues, showing the 5 most recent".format(l)
        else:
            text = "{} open issues".format(l)

        attachments = json.dumps([{
                "author_icon": i["user"]["avatar_url"],
                "author_name": i["user"]["login"],
                "author_link": i["user"]["html_url"],
                "fallback": i["body"],
                "title": "[{}] {}".format(i["number"], i["title"]),
                "title_link": i["url"],
                "color": "good"
            }
            for i in issues[:5]])

        return {
            "attachments": attachments,
            "text": text,
        }

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!hub (.*)", text)
    if not match:
        return

    cmdargs = match[0].encode("utf8").split(' ')
    cmd = cmdargs[0]
    args = cmdargs[1:]
    kwargs = github(cmd, *args)
    server.slack.post_message(
            msg['channel'],
            '',
            as_user=server.slack.server.username,
            **kwargs)
