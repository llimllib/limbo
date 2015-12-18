# -*- coding: UTF-8 -*-# -*- coding: UTF-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from giphy import on_message

def test_giphy():
    # Checking it can pull a gif correctly
    ret = on_message({"text":"miley"}, None) # Random tag that should always have a gif, thanks Miley!
    assert ret != "Oops, no Gifs found for the tag {miley}. Please try a different tag"


def test_unicode():
    # Handling unicode
    ret = on_message({"text":"Mötörhead"}, None)