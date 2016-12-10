# -*- coding: UTF-8 -*-
import os
import sys

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, '../../limbo/plugins'))

from help import on_message
import limbo

def test_basic():
    hooks = {"help": {"test": "!test help system"}}
    server = limbo.FakeServer(hooks=hooks)
    ret = on_message({"text": u"!help"}, server)
    assert ret == hooks["help"]["test"]

def test_nonexistent():
    hooks = {}
    server = limbo.FakeServer(hooks=hooks)
    ret = on_message({"text": u"!help"}, server)
    assert ret == ''

def test_extended():
    hooks = {"extendedhelp": {"test": "!test help system\nline 2"}}
    server = limbo.FakeServer(hooks=hooks)
    ret = on_message({"text": u"!help test"}, server)
    assert ret == hooks["extendedhelp"]["test"]

def test_extended_not_there():
    hooks = {"extendedhelp": {"test": "!test help system\nline 2"}}
    server = limbo.FakeServer(hooks=hooks)
    ret = on_message({"text": u"!help not_there"}, server)
    assert ret == 'No help found for not_there'
