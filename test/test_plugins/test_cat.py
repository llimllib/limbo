# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from cat import on_message


def test_cat():
    with vcr.use_cassette("test/fixtures/cat.yaml"):
        ret = on_message({"text": "!cat"}, None)
        assert "https://cdn2.thecatapi.com/images/MTY3MzM3OA.jpg" in ret
