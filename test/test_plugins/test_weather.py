# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from weather import on_message

DEFAULT_API_KEY = "abcdef"
os.environ["WEATHER_API_KEY"] = DEFAULT_API_KEY

def __skip_tests():
    # we don't run tests if LIMBO_NETWORK_TESTS is on and the user hasn't provided a non-default
    # API key; network tests will always without an API key
    running_network_tests = os.environ.get('LIMBO_NETWORK_TESTS', False)
    using_default_key = os.environ["WEATHER_API_KEY"] == DEFAULT_API_KEY
    return running_network_tests and using_default_key

def test_basic():
    if __skip_tests():
        print('skipping weather test')
        return

    with VCR.use_cassette('test/fixtures/weather_basic.yaml'):
        ret = on_message({"text": u"!weather Oahu, HI"}, None)
        assert ":cloud: Sat 71" in ret

def test_unicode():
    if __skip_tests():
        print('skipping weather test')
        return

    with VCR.use_cassette('test/fixtures/weather_unicode.yaml'):
        ret = on_message({"text": u"!weather Provençal"}, None)
        # not blowing up == success
