# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from youtube import on_message

def test_basic():
    with VCR.use_cassette('test/fixtures/youtube_basic.yaml'):
        ret = on_message({"text": u"!youtube live long and prosper"}, None)
        assert 'https://www.youtube.com/watch?v=' in ret, ret

def test_unicode():
    with VCR.use_cassette('test/fixtures/youtube_unicode.yaml'):
        _ = on_message({"text": u"!youtube 崖の上のポニョ"}, None)
        # not blowing up == success
