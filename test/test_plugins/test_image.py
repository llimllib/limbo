# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from image import on_message, unescape

def test_image():
    with VCR.use_cassette('test/fixtures/image_bananas.yaml'):
        ret = on_message({"text": u"!image bananas"}, None)
        assert '.jpg' in ret, ret

def test_unicode():
    with VCR.use_cassette('test/fixtures/image_unicode.yaml'):
        _ = on_message({"text": u"!image Mötörhead"}, None)
        # not blowing up == success, for our purposes
