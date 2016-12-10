# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from calc import on_message

def test_calc():
    with vcr.use_cassette('test/fixtures/calc_basic.yaml'):
        ret = on_message({"text": u"!calc 2469*5"}, None)
        assert '12,345' in ret

def test_unicode():
    with vcr.use_cassette('test/fixtures/calc_unicode.yaml'):
        # บาท is the Thai Bhat (spelled in Thai, obvs)
        ret = on_message({"text": u"!calc 10 dollars in บาท"}, None)
        # no exception == success
