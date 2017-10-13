# -*- coding: UTF-8 -*-
import os
import sys

from .utils import VCR

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from dog import on_message


def test_dog():
    with VCR.use_cassette('test/fixtures/dog.yaml'):
        ret = on_message({"text": u"!dog"}, None)
        assert "https://dog.ceo/api/img/" in ret
