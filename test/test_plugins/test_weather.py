# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from weather import on_message

os.environ["WEATHER_API_KEY"] = "abcdef"

def test_basic():
    with VCR.use_cassette('test/fixtures/weather_basic.yaml'):
        ret = on_message({"text": u"!weather Oahu, HI"}, None)
        assert ":cloud: Sat 71" in ret

def test_unicode():
    with VCR.use_cassette('test/fixtures/weather_unicode.yaml'):
        ret = on_message({"text": u"!weather Provençal"}, None)
        # not blowing up == success
