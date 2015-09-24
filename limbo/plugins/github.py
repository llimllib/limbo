"""!github <command> <arguments> is a command line interface to github

like, document the commands and arguments here or something"""

import argparse
import json
import os
import re

import requests

HUB_URL = 'https://api.github.com/{}'

class Github(object):
    def __init__(self, username, password):
        self.auth = username, password

    def _get(self, url_fragment, **params):
        return requests.get(
                 HUB_URL.format(url_fragment),
                 auth=self.auth,
                 params=params
               )

    def _post(self, url_fragment, data={}, **params):
        return requests.post(
                 HUB_URL.format(url_fragment),
                 auth=self.auth,
                 data=data,
                 params=params
               )

    def issues(self, repo):
        # defaults to only open issues
        return self._get('repos/{}/issues'.format(repo)).json()

    def create_issue(self, repo, title, body=''):
        return self._post(
                'repos/{}/issues'.format(repo),
                data=json.dumps({
                    "title": title,
                    "body": body})).json()

    def search_issue_in_repo(self, repo, query):
        return self._get(
                'search/issues',
                q="{} repo:{}".format(query, repo)).json()

    def get_all_repos(self):
        repos = self._get('user/repos', per_page=100)
        repo_names = [repo["full_name"] for repo in repos.json()]
        last = re.findall(r'rel="last"', repos.headers['link'])

        page = 2
        while last:
            repos = self._get('user/repos', per_page=100, page=page)
            repo_names += [repo["full_name"] for repo in repos.json()]
            last = re.findall(r'rel="last"', repos.headers['link'])
            page += 1

        return repo_names

# create an authed github object
HUB = Github(os.environ.get("GITHUB_USER"), os.environ.get("GITHUB_PASS"))

# Gather all repo names available to the authed user. Eventually this will
# need to be refreshed; but for now just assume this is good enough.
# ALL_REPOS = HUB.get_all_repos()

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

def get_default_repo(server, room):
    rows = server.query('''
        SELECT repo FROM github_room_repo_defaults WHERE room=?''', room)

    if rows:
        return rows[0][0]
    return None

def set_default_repo(server, room, repo):
    server.query('''
        INSERT INTO github_room_repo_defaults(room, repo)
        VALUES (?, ?)''', room, repo)

def github(server, room, cmd, body, repo):
    # If repo wasn't passed in explicitly, grab it from the database
    if not repo:
        repo = get_default_repo(server, room)

    # If we still couldn't find one in the database, either it's a command to
    # set it or we can instrcut the user how to do so
    if not repo:
        if cmd == "setdefault":
            set_default_repo(server, room, body[0])
            return "Default repo for this room set to `{}`".format(body[0])
        else:
            return "Unable to find default repo for this channel. "\
                   "Run `!hub setdefault <repo_name>`"

    if cmd == "issues":
        issues = HUB.issues(repo)
        if not isinstance(issues, list):
            return "Unable to find repository {}".format(repo)

        l = len(issues)
        if l == 0:
            return "0 open issues on repository {}".format(repo)
        elif l > 5:
            text = "{} open issues, showing the 5 most recent".format(l)
        else:
            text = "{} open issues".format(l)

        attachments = json.dumps([format_issue(i) for i in issues[:5]])

        return {
            "attachments": attachments,
            "text": text,
        }
    if cmd in ["create", "new"]:
        title = ' '.join(body)
        issue = HUB.create_issue(repo, title)
        attachments = json.dumps([format_issue(issue)])

        return {
            "attachments": attachments,
            "text": "",
        }
    if cmd in ["search"]:
        query = ' '.join(body)
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
    if cmd == "getdefault":
        return "Default repo for this room is `{}`. " \
               "To change it, run `!hub setdefault <repo_name>`".format(repo)

FIRST=True
def create_database(server):
    server.query('''
        CREATE TABLE IF NOT EXISTS github_room_repo_defaults
            (room text, repo text)''')
    FIRST=False

ARGPARSE = argparse.ArgumentParser()
ARGPARSE.add_argument('-r', dest="repo")
ARGPARSE.add_argument('command', nargs=1)
ARGPARSE.add_argument('body', nargs='*')

def on_message(msg, server):
    if FIRST:
        create_database(server)

    text = msg.get("text", "")
    match = re.findall(r"!hub (.*)", text)
    if not match:
        return

    ns = ARGPARSE.parse_args(match[0].encode("utf8").split(' '))

    # if the user calls !hub with no arguments, print help
    if not len(ns.command):
        return "TODO: Help message"

    kwargs = github(server, msg["channel"], ns.command[0], ns.body, ns.repo)

    # if github() didn't return anything, or returned any non-dict arg,
    # just return it
    if not kwargs or not isinstance(kwargs, dict):
        return kwargs

    # otherwise, post the message via the slack API; this lets us use fancy
    # formatting rather than the plain formatting the RTM API allows
    server.slack.post_message(
            msg['channel'],
            '',
            as_user=server.slack.server.username,
            **kwargs)
