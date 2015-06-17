# -*- coding: UTF-8 -*-
from collections import namedtuple
import logging
from .mock_handler import MockHandler
import os
import sqlite3
import tempfile
from nose.tools import eq_

import limbo

# test plugin hooks
#
# TODO: test init_plugins with unicode plugins
# TODO: test init_plugins with invalid plugins
# TODO: test init_plugins with plugin without on_
# TODO: test init_plugins __doc__ handling
# TODO: test plugin that throws exception (on import, init and message)

# copied from slackrtm
User = namedtuple('User', 'server name id real_name tz')

DIR = os.path.dirname(os.path.realpath(__file__))
PARENT = os.path.split(DIR)[0]

os.environ["LIMBO_LOGFILE"] = "/tmp/deleteme"

def test_plugin_success():
    hooks = limbo.init_plugins("test/plugins")
    eq_(len(hooks), 3)
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    eq_(len(hooks["message"]), 2)

def test_plugin_invalid_dir():
    try:
        limbo.init_plugins("invalid/package")
    except limbo.InvalidPluginDir:
        return
    1 / 0

def test_plugin_logs():
    mhdr = MockHandler()
    logging.getLogger("limbo.limbo").addHandler(mhdr)
    limbo.init_plugins("test/plugins")
    mhdr.check("debug", "attaching message hook for echo")

# test run_hook

def test_run_hook():
    hooks = limbo.init_plugins("test/plugins")
    eq_(limbo.run_hook(hooks, "message", {"text": u"!echo bananas"}, None), [u"!echo bananas"])

def test_missing_hook():
    hooks = limbo.init_plugins("test/plugins")
    eq_(limbo.run_hook(hooks, "nonexistant", {"text": u"!echo bananas"}, None), [])

# test handle_message

def test_handle_message_subtype():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    server = limbo.FakeServer()
    event = {"bot_id": "1", "text": msg}
    event["subtype"] = "message_changed"
    eq_(limbo.handle_message(event, server), None)

def test_handle_message_ignores_self():
    server = limbo.FakeServer()
    event = {"user": "limbo_test"}
    eq_(limbo.handle_message(event, server), None)

def test_handle_message_ignores_slackbot():
    server = limbo.FakeServer()
    event = {"user": "slackbot"}
    eq_(limbo.handle_message(event, server), None)

def test_handle_message_basic():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    event = {"user": "2", "text": msg}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    eq_(limbo.handle_message(event, server), msg)

# Under unclear circumstances, slack can return a None user.
# https://github.com/llimllib/limbo/issues/40
def test_handle_message_slack_user_nil():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    event = {"user": "msguser", "text": msg}
    users = {"0": User(None, "nobody", 0, "", 0)}

    hooks = limbo.init_plugins("test/plugins")
    slack = limbo.FakeSlack(users=users)
    server = limbo.FakeServer(slack=slack, hooks=hooks)

    eq_(limbo.handle_message(event, server), None)

def test_handle_bot_message():
    msg = u"!echo Iñtërnâtiônàlizætiøn bot"
    event = {"bot_id": "1", "text": msg, "subtype": "bot_message"}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    eq_(limbo.handle_message(event, server), msg)

def test_init_db():
    tf = tempfile.NamedTemporaryFile()
    db = limbo.init_db(tf.name)
    eq_(type(db), type(sqlite3.connect(":memory:")))

class FakeSlackClient(object):
    def __init__(self, connect=True):
        self.connect = connect

    def rtm_connect(self):
        return self.connect
