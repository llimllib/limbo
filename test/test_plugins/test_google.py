# -*- coding: UTF-8 -*-
import os
import sys


DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from google import on_message

"""
These are a bit hard to test for SPECIFIC requirements.
Search results will change with time.
As long as no exceptions get thrown, it should be fine.
"""

def test_google():
    ret = on_message({"text": "!google this is a test"}, None)

def test_search():
    ret = on_message({"text": "!search this is a test"}, None)

def test_unicode():
    ret = on_message({"text": "!google Mötörhead"}, None)

def test_what_is():
    ret = on_message({"text": "!google what is banana"}, None)

def test_translate():
    ret = on_message({"text": "!google translate gracias to english"}, None)
