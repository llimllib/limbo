# -*- coding: UTF-8 -*-
import logging
import os
import sqlite3
import tempfile
from nose.tools import eq_

import slask

# TODO: kill logging output into stderr.
# TODO: test logging to STDERR

# test plugin hooks
#
# TODO: test init_plugins with unicode plugins
# TODO: test init_plugins with invalid plugins
# TODO: test init_plugins with plugin without on_
# TODO: test init_plugins __doc__ handling
# TODO: test plugin that throws exception (on import, init and message)
# TODO: test command line interface

DIR = os.path.dirname(os.path.realpath(__file__))
PARENT = os.path.split(DIR)[0]

def test_plugin_success():
    hooks = slask.init_plugins("test/plugins")
    eq_(len(hooks), 2)
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    eq_(len(hooks["message"]), 2)
    eq_(hooks["message"][0]({"text": u"!echo bananas"}, None), u"!echo bananas")

def test_plugin_invalid_dir():
    try:
        hooks = slask.init_plugins("invalid/package")
    except slask.InvalidPluginDir:
        return
    1/0

def test_plugin_logs():
    tfh = tempfile.NamedTemporaryFile()

    slask.init_log(config={
        "logfile": tfh.name,
        "loglevel": logging.DEBUG,
    })
    slask.init_plugins("test/plugins")

    tfh.seek(0)
    log = tfh.read()

    assert "DEBUG:plugin: test/plugins/echo.py" in log
    assert "DEBUG:attaching" in log

# test run_hook

def test_run_hook():
    hooks = slask.init_plugins("test/plugins")
    eq_(slask.run_hook(hooks, "message", {"text": u"!echo bananas"}, None), [u"!echo bananas"])

def test_missing_hook():
    hooks = slask.init_plugins("test/plugins")
    eq_(slask.run_hook(hooks, "nonexistant", {"text": u"!echo bananas"}, None), [])

# test handle_message

def test_handle_message_subtype():
    server = slask.FakeServer()
    eq_(slask.handle_message({"subtype": "bot_message"}, server), None)
    eq_(slask.handle_message({"subtype": "message_changed"}, server), None)

def test_handle_message_ignores_self():
    server = slask.FakeServer()
    event = {"user": "slask_test"}
    eq_(slask.handle_message(event, server), None)

def test_handle_message_ignores_slackbot():
    server = slask.FakeServer()
    event = {"user": "slackbot"}
    eq_(slask.handle_message(event, server), None)

def test_handle_message_basic():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    event = {"user": "msguser", "text": msg}

    hooks = slask.init_plugins("test/plugins")
    server = slask.FakeServer(hooks=hooks)

    eq_(slask.handle_message(event, server), msg)

def test_init_db():
    tf = tempfile.NamedTemporaryFile()
    db = slask.init_db(tf.name)
    eq_(type(db), type(sqlite3.connect(":memory:")))

class FakeSlackClient(object):
    def __init__(self, connect=True):
        self.connect = connect
    
    def rtm_connect(self):
        return self.connect
