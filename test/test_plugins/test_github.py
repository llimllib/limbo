# -*- coding: UTF-8 -*-
import os
import sys
import sqlite3

from nose.tools import eq_
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from github import on_message
from limbo.server import LimboServer
from limbo.fakeserver import FakeServer

SERVER = FakeServer(db=sqlite3.connect(":memory:"))

def test_basic():
    with vcr.use_cassette('test/fixtures/github_issues.yaml'):
        ret = on_message({"text": u"!hub issue 5 -r llimllib/limbo", "channel": "test_channel"}, SERVER)
        #import ipdb; ipdb.set_trace()
        expected = ('', {'text': '', 'attachments': '[{"title": "[5] Create an emoji translator", "color": "good", "text": "i.e. if you type \\"I love to eat bananas\\", the plugin does *something* to try and convert that into a string of emoji. It probably involves a list of synonyms? Maybe even a word model? Or it does something really simple? I don\'t know, but it would be an awesome feature.", "author_link": "https://github.com/llimllib", "author_name": "llimllib", "title_link": "https://github.com/llimllib/limbo/issues/5", "fallback": "Create an emoji translator", "author_icon": "https://avatars.githubusercontent.com/u/7150?v=3"}]', 'as_user': 'replbot'})
        assert SERVER.slack.posted_message == expected
