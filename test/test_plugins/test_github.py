# -*- coding: UTF-8 -*-
import json
import os
import sys
import sqlite3

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from github import on_message
from limbo.server import LimboServer
from limbo.fakeserver import FakeServer

SERVER = FakeServer(db=sqlite3.connect(":memory:"))

def dicteq(a, b):
    assert sorted(a.items()) == sorted(b.items())

def test_basic():
    with vcr.use_cassette('test/fixtures/github_issues.yaml'):
        ret = on_message({"text": u"!hub issue 5 -r llimllib/limbo", "channel": "test_channel"}, SERVER)
        #import ipdb; ipdb.set_trace()
        expected = {
            u'author_icon': u'https://avatars.githubusercontent.com/u/7150?v=3',
            u'author_link': u'https://github.com/llimllib',
            u'author_name': u'llimllib',
            u'color': u'good',
            u'fallback': u'Create an emoji translator',
            u'text': u'i.e. if you type "I love to eat bananas", the plugin does *something* to try and convert that into a string of emoji. It probably involves a list of synonyms? Maybe even a word model? Or it does something really simple? I don\'t know, but it would be an awesome feature.',
            u'title': u'[5] Create an emoji translator',
            u'title_link': u'https://github.com/llimllib/limbo/issues/5'
        }
        actual = json.loads(SERVER.slack.posted_messages[0][1]['attachments'])
        assert len(actual) == 1
        dicteq(expected, actual[0])
