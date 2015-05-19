# -*- coding: UTF-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from map import on_message

def test_unicode():
    ret = on_message({"text": u"!map Moscow, россия"}, None)
    assert "googleapis" in ret
    assert "Moscow" in ret
