import os
import sys

from nose.tools import eq_
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))
FIX = os.path.join(DIR, "../../test/fixtures")

from stock import on_message, stockprice

def test_apple():
    with vcr.use_cassette('test/fixtures/apple.yaml'):
        ret = on_message({"text": u"$aapl"}, None)
        assert ':chart_with_upwards_trend:' in ret
        assert 'Apple Inc.' in ret
        assert '130.41' in ret
        assert '+1.62' in ret
