# -*- coding: UTF-8 -*-
import json
import os
import re
import sys

import limbo
from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from image import on_message

def msgobj(msg):
    return {
        "text": msg,
        "channel": "abc123"
    }

def test_image():
    server = limbo.FakeServer()
    with VCR.use_cassette('test/fixtures/image_bananas.yaml'):
        on_message(msgobj(u"!image bananas"), server)

    url = json.loads(server.slack.posted_message[1]["attachments"])[0]['image_url']
    assert re.match('https?://\S+$', url), url

def test_unicode():
    server = limbo.FakeServer()
    with VCR.use_cassette('test/fixtures/image_unicode.yaml'):
        on_message(msgobj(u"!image Mötörhead"), server)
        # not blowing up == success, for our purposes
