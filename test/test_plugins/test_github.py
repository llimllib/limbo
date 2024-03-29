# -*- coding: UTF-8 -*-
import json
import os
import sys
import sqlite3

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from github import on_message
from limbo.server import LimboServer
from limbo.fakeserver import FakeServer

SERVER = FakeServer(db=sqlite3.connect(":memory:"))


def dicteq(a, b):
    assert sorted(a.items()) == sorted(b.items())


def test_basic():
    with vcr.use_cassette("test/fixtures/github_issues.yaml"):
        ret = on_message(
            {"text": "!hub issue 5 -r llimllib/limbo", "channel": "test_channel"},
            SERVER,
        )
        # import ipdb; ipdb.set_trace()
        expected = {
            "author_icon": "https://avatars.githubusercontent.com/u/7150?v=4",
            "author_link": "https://github.com/llimllib",
            "author_name": "llimllib",
            "color": "good",
            "fallback": "Create an emoji translator",
            "text": 'i.e. if you type "I love to eat bananas", the plugin does _something_ to try and convert that into a string of emoji. It probably involves a list of synonyms? Maybe even a word model? Or it does something really simple? I don\'t know, but it would be an awesome feature.\n',
            "title": "[5] Create an emoji translator",
            "title_link": "https://github.com/llimllib/limbo/issues/5",
        }
        actual = json.loads(SERVER.slack.posted_messages[0][1]["attachments"])
        assert len(actual) == 1
        dicteq(expected, actual[0])
