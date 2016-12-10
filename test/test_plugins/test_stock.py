# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from stock import on_message, stockprice

def test_apple():
    with vcr.use_cassette('test/fixtures/stock_apple.yaml'):
        ret = on_message({"text": u"$aapl"}, None)
        assert ':chart_with_upwards_trend:' in ret
        assert 'Apple Inc.' in ret
        assert '130.41' in ret
        assert '+1.62' in ret

def test_nonexistent():
    with vcr.use_cassette('test/fixtures/stock_none'):
        ret = on_message({"text": u"bana"}, None)
        assert ret == None

def test_unicode():
    with vcr.use_cassette('test/fixtures/stock_unicode.yaml'):
        ret = on_message({"text": u"$äapl"}, None)
        assert ret == None

def test_multiple():
    with vcr.use_cassette('test/fixtures/stock_multiple.yaml'):
        ret = on_message({"text": u"$goog $aapl"}, None)
        assert 'Google Inc' in ret

def test_price():
    with vcr.use_cassette('test/fixtures/stock_none'):
        ret = on_message({"text": u"the price is $12.43"}, None)
        assert ret == None
