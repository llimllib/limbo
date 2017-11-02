# -*- coding: UTF-8 -*-
import os
import re
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from gif import on_message

def test_gif():
    with VCR.use_cassette('test/fixtures/gif_bananas.yaml'):
        ret = on_message({"text": u"!gif bananas"}, None)
        assert re.match('https?://\S+$', ret), ret

def test_unicode():
    with VCR.use_cassette('test/fixtures/gif_unicode.yaml'):
        _ = on_message({"text": u"!gif Mötörhead"}, None)
        # not blowing up == success, for our purposes
