# -*- coding: UTF-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))

from banner import on_message


def test_basic():
    ret = on_message({"text": "!banner llimllib --font morse"}, None)
    assert ret == "```.-.. .-.. .. -- .-.. .-.. .. -...```"


def test_unicode():
    # Figlet just swallows unicode
    ret = on_message({"text": "!banner Харито́н"}, None)
    assert ret == None

    # Though it will print the other characters
    ret = on_message({"text": "!banner Mötörhead --font morse"}, None)
    assert ret == "```-- ---. - ---. .-. .... . .- -..```"
