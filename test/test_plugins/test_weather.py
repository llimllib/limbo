# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from weather import on_message

def msgobj(msg):
    return {
        "text": msg,
        "channel": "abc123"
    }

def test_basic():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/weather_basic.yaml'):
        on_message(msgobj(u"!weather Oahu, HI"), server)
        attachment = json.loads(server.slack.posted_messages[0][1]['attachments'])[0]
        assert "Weather for Honolulu, HI" in attachment['pretext']
        assert attachment['fields'][0]['value'] == u':sun_small_cloud: 73°f'

def test_unicode():
    server = limbo.FakeServer()
    with vcr.use_cassette('test/fixtures/weather_unicode.yaml'):
        on_message(msgobj(u"!weather กรุงเทพมหานคร"), server)
        # not blowing up == success
