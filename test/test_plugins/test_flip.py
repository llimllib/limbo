# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from flip import on_message

def test_no_args():
    ret = on_message({"text": u"!flip"}, None)
    assert "heads" in ret
    assert "tails" in ret

# costs about .3 seconds on my laptop
def test_count_flips_no_args():
    n = 1000
    heads = 0
    for i in range(n):
        ret = on_message({"text": u"!flip"}, None)
        if ret.startswith("heads"):
            heads += 1

    # 99.86% chance of being true
    assert 450 < heads < 550

def test_some_args():
    ret = on_message({"text": u"!flip peter, paul, mary"}, None)
    assert "peter" in ret
    assert "paul" in ret
    assert "mary" in ret

def test_unicode():
    ret = on_message({"text": u"!flip Харито́н, Ки́р, Кири́лл"}, None)
    assert u"Кири́лл" in ret
    assert u"Ки́р" in ret
    assert u"Кири́лл" in ret
