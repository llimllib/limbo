# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from stockphoto import on_message

def test_basic():
    with vcr.use_cassette('test/fixtures/stockphoto_basic.yaml'):
        ret = on_message({"text": u"!stock woman eating salad"}, None)
        assert '.jpg' in ret

def test_unicode():
    with vcr.use_cassette('test/fixtures/stockphoto_unicode.yaml'):
        ret = on_message({"text": u"!stock übermensch"}, None)
        # not blowing up == success
