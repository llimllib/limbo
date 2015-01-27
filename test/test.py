# -*- coding: UTF-8 -*-

import slask
import tempfile
import logging
from nose.tools import eq_

# TODO: kill logging output into stderr.
# TODO: test logging to STDERR

# test plugin hooks
#
# TODO: test init_plugins with unicode plugins
# TODO: test init_plugins with invalid plugins
# TODO: test init_plugins with plugin without on_
# TODO: test init_plugins __doc__ handling

def test_plugin_success():
    hooks = slask.init_plugins("test/plugins")
    eq_( len(hooks) ,  1)
    assert "message" in hooks
    assert isinstance(hooks, dict)
    assert isinstance(hooks["message"], list)
    eq_( len(hooks["message"]) ,  1)
    eq_( hooks["message"][0]({"text": u"bananas"}, None) ,  u"bananas")

def test_plugin_invalid_dir():
    hooks = slask.init_plugins("invalid/package")
    eq_( len(hooks) ,  0)

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
    assert "DEBUG:attaching plugins." in log

# test run_hook

def test_run_hook():
    hooks = slask.init_plugins("test/plugins")
    eq_(slask.run_hook(hooks, "message", {"text": u"bananas"}, None), [u"bananas"])

def test_missing_hook():
    hooks = slask.init_plugins("test/plugins")
    eq_(slask.run_hook(hooks, "nonexistant", {"text": u"bananas"}, None), [])

# test handle_message

def test_handle_message_subtype():
    eq_(slask.handle_message(None, {"subtype": "bot_message"}, None, None), None)
    eq_(slask.handle_message(None, {"subtype": "message_changed"}, None, None), None)

class FakeClient(object):
    def __init__(self, server=None):
        self.server = server or FakeServer()

class FakeServer(object):
    def __init__(self, botname="slask_test"):
        self.login_data = {
            "self": {
                "name": botname,
            }
        }

        self.users = {
            "slask_test": {"name": "slask_test"},
            "msguser": {"name": "msguser"},
            "slackbot": {"name": "slackbot"},
        }

def test_handle_message_ignores_self():
    client = FakeClient()
    event = {"user": "slask_test"}
    eq_(slask.handle_message(client, event, None, None), None)

def test_handle_message_ignores_slackbot():
    client = FakeClient()
    event = {"user": "slackbot"}
    eq_(slask.handle_message(client, event, None, None), None)

def test_handle_message_basic():
    client = FakeClient()

    msg = u"Iñtërnâtiônàlizætiøn"
    event = {"user": "msguser", "text": msg}

    hooks = slask.init_plugins("test/plugins")
    eq_(slask.handle_message(client, event, hooks, None), msg)
