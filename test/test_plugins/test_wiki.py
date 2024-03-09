# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from wiki import on_message


def test_basic():
    with vcr.use_cassette("test/fixtures/wiki_basic.yaml"):
        ret = on_message({"text": "!wiki dog"}, None)
        assert "Canis familiaris" in ret
        assert "http://en.wikipedia.org/wiki/Dog" in ret


def test_unicode():
    with vcr.use_cassette("test/fixtures/wiki_unicode.yaml"):
        ret = on_message({"text": "!wiki नेपाल"}, None)
        # not blowing up == success
