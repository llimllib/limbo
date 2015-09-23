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

    def _get(self, url_fragment, **params):
        return requests.get( HUB_URL.format(url_fragment), auth=self.auth, params=params).json()
        return requests.get(
                 HUB_URL.format(url_fragment),
                 auth=self.auth,
                 params=params
               ).json()

    def _post(self, url_fragment, data={}, **params):
        return requests.post(
                 HUB_URL.format(url_fragment),
                 auth=self.auth,
                 data=data,
                 params=params
               ).json()

    def issues(self, repo):
        # defaults to only open issues
        return self._get('repos/{}/issues'.format(repo))

    def create_issue(self, repo, title, body=''):
        return self._post(
                'repos/{}/issues'.format(repo),
                data=json.dumps({
                    "title": title,
                    "body": body}))

    def search_issue_in_repo(self, repo, query):
        return self._get(
                'search/issues',
                q="{} repo:{}".format(query, repo))

HUB = Github(os.environ.get("GITHUB_USER"), os.environ.get("GITHUB_PASS"))

def format_issue(issue_json):
    return {
        "author_icon": issue_json["user"]["avatar_url"],
        "author_name": issue_json["user"]["login"],
        "author_link": issue_json["user"]["html_url"],
        "fallback": issue_json["title"],
        "title": "[{}] {}".format(issue_json["number"], issue_json["title"]),
        "title_link": issue_json["html_url"],
        "color": "good"
    }

def github(cmd, *args):
    if cmd == "issues":
        issues = HUB.issues(args[0])

        l = len(issues)
        if l > 5:
            text = "{} open issues, showing the 5 most recent".format(l)
        else:
            text = "{} open issues".format(l)

        attachments = json.dumps([format_issue(i) for i in issues[:5]])

        return {
            "attachments": attachments,
            "text": text,
        }
    if cmd in ["create", "new"]:
        repo = args[0]
        title = ' '.join(args[1:])
        issue = HUB.create_issue(repo, title)
        attachments = json.dumps([format_issue(issue)])

        return {
            "attachments": attachments,
            "text": "",
        }
    if cmd in ["search"]:
        repo = args[0]
        query = ' '.join(args[1:])
        response = HUB.search_issue_in_repo(repo, query)

        if response["total_count"] == 0:
            return {
                "text": "sorry, no issues found"
            }

        issues = response["items"]
        attachments = json.dumps([format_issue(i) for i in issues[:5]])
        text = "Found {} items".format(response["total_count"])
        return {
            "attachments": attachments,
            "text": text
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
