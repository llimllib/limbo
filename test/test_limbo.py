# -*- coding: UTF-8 -*-
from collections import namedtuple
import logging
from .mock_handler import MockHandler
import os
import sqlite3
import tempfile

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
    assert len(hooks) == 9
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    assert len(hooks["message"]) == 2

def test_config_plugin_none_success():
    hooks = limbo.init_plugins("test/plugins", None)
    assert len(hooks) == 9
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    assert len(hooks["message"]) == 2

def test_config_plugin_empty_string_success():
    hooks = limbo.init_plugins("test/plugins", "")
    assert len(hooks) == 9
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    assert len(hooks["message"]) == 2

def test_config_plugin_success():
    hooks = limbo.init_plugins("test/plugins", "echo,loop")
    assert len(hooks) == 5
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    assert len(hooks["message"]) == 1

def test_config_plugin_doesnt_exist():
    hooks = limbo.init_plugins("test/plugins", "doesnotexist")
    assert len(hooks) == 0

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
    assert limbo.run_hook(hooks, "message", {"text": u"!echo bananas"}, None) == [u"!echo bananas"]

def test_missing_hook():
    hooks = limbo.init_plugins("test/plugins")
    assert limbo.run_hook(hooks, "nonexistant", {"text": u"!echo bananas"}, None) == []

# test handle_message

def test_handle_message_subtype():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    server = limbo.FakeServer()
    event = {"bot_id": "1", "text": msg}
    event["subtype"] = "message_changed"
    assert limbo.handle_message(event, server) == None

def test_handle_message_ignores_self():
    server = limbo.FakeServer()
    event = {"user": "1", "type": "message", "id": "1"}
    assert limbo.handle_message(event, server) == None

def test_handle_message_ignores_slackbot():
    server = limbo.FakeServer()
    event = {"user": "USLACKBOT"}
    assert limbo.handle_message(event, server) == None

def test_handle_message_basic():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    event = {"user": "2", "text": msg}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_message(event, server) == msg

def test_handle_channel_join():
    event = {
      "user": "2",
      "type": "message",
      "subtype": "channel_join",
      "text": "User has joined"
    }

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_message(event, server) == "saw user 2 join"

def test_handle_member_joined():
    event = {
      "type": "member_joined_channel",
      "user": "2"
    }

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_event(event, server) == "user 2 joined"

def test_handle_member_left():
    event = {
      "type": "member_left_channel",
      "user": "2"
    }

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_event(event, server) == "user 2 left"

# Under unclear circumstances, slack can return a None user.
# https://github.com/llimllib/limbo/issues/40
def test_handle_message_slack_user_nil():
    msg = u"!echo Iñtërnâtiônàlizætiøn"
    event = {"user": "msguser", "text": msg}
    users = {"0": User(None, "nobody", 0, "", 0)}

    hooks = limbo.init_plugins("test/plugins")
    slack = limbo.FakeSlack(users=users)
    server = limbo.FakeServer(slack=slack, hooks=hooks)

    assert limbo.handle_message(event, server) == u"!echo Iñtërnâtiônàlizætiøn"

def test_handle_bot_message():
    msg = u"!echo Iñtërnâtiônàlizætiøn bot"
    event = {"bot_id": "2", "text": msg, "subtype": "bot_message"}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_message(event, server) == msg

def test_handle_edit_message():
    oldmsg = u"old message"
    newmsg = u"!echo new message"
    event = {"type": "message",
            "subtype": "message_changed",
            "previous_message": {"text": oldmsg},
            "message": {"text": newmsg, "user": "msguser"}}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_message(event, server) == "Changed: {}".format(newmsg)

def test_handle_delete_message():
    oldmsg = u"!echo old message"
    event = {"type": "message",
            "subtype": "message_deleted",
            "previous_message": {"text": oldmsg, "user": "msguser"}}

    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)

    assert limbo.handle_message(event, server) == "Deleted: {}".format(oldmsg)

def test_init_db():
    tf = tempfile.NamedTemporaryFile()
    db = limbo.init_db(tf.name)
    assert type(db) == type(sqlite3.connect(":memory:"))

class FakeSlackClient(object):
    def __init__(self, connect=True):
        self.connect = connect

    def rtm_connect(self):
        return self.connect

def test_loop_hook():
    hooks = limbo.init_plugins("test/plugins")
    server = limbo.FakeServer(hooks=hooks)
    slack = limbo.FakeSlack()
    limbo.loop(server, test_loop=1)

    assert server._loop_plugin_ran == True
