# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from urban import on_message

def test_unicode():
    ret = on_message({"text": u"!urban Mötörhead"}, None)
    # not blowing up == success, for our purposes

def test_message():
    ret = on_message({"text": u"!urban Test"}, None)
    assert "Example" in ret
