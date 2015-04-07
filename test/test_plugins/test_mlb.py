# -*- coding: UTF-8 -*-
import os
import sys

from nose.tools import eq_
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from mlb import on_message

def test_basic():
    with vcr.use_cassette('test/fixtures/mlb_basic.yaml'):
        ret = on_message({"text": u"!mlb Red Sox"}, None)
        assert "Boston Red Sox" in ret
