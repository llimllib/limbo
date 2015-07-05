# -*- coding: UTF-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from giphy import on_message



def test_obscure_tag():
    """
    Obscure tags yeild no result
    """
    return on_message({"text": "!giphy kangaroo eating a banana"}, None) == "Oops, No gifs found for that tag. Try again!"
    # This shouldn't ever yeild a result.

def test_unicode():
    ret = on_message({"text": u"!giphy Banana"}, None)
    return ret not in ["Oops, No gifs found for that tag. Try again!",
                       "Oops, something went wrong. Contact your admin if this happens again!"]


