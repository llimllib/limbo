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

        return [
            {
                "fallback": i["body"],
                "title": "[{}] {}".format(i["number"], i["title"]),
                "title_link": i["url"],
                "text": i["body"],
                "color": "good"
            }
            for i in issues
        ]

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!hub (.*)", text)
    if not match:
        return

    cmdargs = match[0].encode("utf8").split(' ')
    cmd = cmdargs[0]
    args = cmdargs[1:]
    attachments = github(cmd, *args)
    # msg: {u'text': u'!hub issues llimllib/limbo', u'ts': u'1443022795.000033', u'user': u'U02L9JD0Y', u'team': u'T02L9JD0W', u'type': u'message', u'channel': u'C02L9JD16'}
    import ipdb; ipdb.set_trace()
    server.slack.post_message(msg['channel'], '', attachments=json.dumps(attachments), as_user=server.slack.server.username)
