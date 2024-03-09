# -*- coding: UTF-8 -*-
import os
import sys

import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from dog import on_message


def test_dog():
    with vcr.use_cassette("test/fixtures/dog.yaml"):
        ret = on_message({"text": "!dog"}, None)
        assert "https://images.dog.ceo/breeds/spaniel-welsh/n02102177_1833.jpg" in ret
