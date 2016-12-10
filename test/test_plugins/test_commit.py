# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from commit import on_message

def test_commit():
  with vcr.use_cassette('test/fixtures/commit.yaml'):
    ret = on_message({"text": u"!commit"}, None)
    assert 'stuff' in ret
