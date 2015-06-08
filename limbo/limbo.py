#!/usr/bin/env python
from __future__ import print_function
import copy
import functools
from glob import glob
import importlib
import logging
import os
import re
import sqlite3
import sys
import time
import traceback

from slackrtm import SlackClient
from .server import LimboServer
from .fakeserver import FakeServer

CURDIR = os.path.abspath(os.path.dirname(__file__))
DIR = functools.partial(os.path.join, CURDIR)

PYTHON3 = sys.version_info[0] > 2

logger = logging.getLogger(__name__)

class InvalidPluginDir(Exception):
    def __init__(self, plugindir):
        self.message = "Unable to find plugin dir {0}".format(plugindir)

def init_log(config):
    loglevel = config.get("loglevel", logging.INFO)
    logformat = config.get("logformat", '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    if config.get("logfile"):
        logging.basicConfig(filename=config.get("logfile"), format=logformat, level=loglevel)
    else:
        logging.basicConfig(format=logformat, level=loglevel)

def init_plugins(plugindir):
    if not plugindir:
        plugindir = DIR("plugins")

    logger.debug("plugindir: {0}".format(plugindir))

    if not os.path.isdir(plugindir):
        raise InvalidPluginDir(plugindir)

    hooks = {}

    oldpath = copy.deepcopy(sys.path)
    sys.path.insert(0, plugindir)

    for plugin in glob(os.path.join(plugindir, "[!_]*.py")):
        logger.debug("plugin: {0}".format(plugin))
        try:
            mod = importlib.import_module(os.path.basename(plugin)[:-3])
            modname = mod.__name__
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                logger.debug("plugin: attaching %s hook for %s", hook, modname)
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        # bare except, because the modules could raise any number of errors
        # on import, and we want them not to kill our server
        except:
            logger.warning("import failed on module {0}, module not loaded".format(plugin))
            logger.warning("{0}".format(sys.exc_info()[0]))
            logger.warning("{0}".format(traceback.format_exc()))

    sys.path = oldpath
    return hooks

def run_hook(hooks, hook, *args):
    responses = []
    for hook in hooks.get(hook, []):
        try:
            h = hook(*args)
            if h:
                responses.append(h)
        except:
            logger.warning("Failed to run plugin {0}, module not loaded".format(hook))
            logger.warning("{0}".format(sys.exc_info()[0]))
            logger.warning("{0}".format(traceback.format_exc()))

    return responses

def handle_message(event, server):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed":
        return

    botname = server.slack.server.login_data["self"]["name"]
    try:
        msguser = server.slack.server.users[event["user"]]
    except KeyError:
        logger.debug("event {0} has no user".format(event))
        return

    # don't respond to ourself or slackbot
    if msguser.name == botname or msguser.name.lower() == "slackbot":
        return

    return "\n".join(run_hook(server.hooks, "message", event, server))

event_handlers = {
    "message": handle_message,
}

def handle_event(event, server):
    handler = event_handlers.get(event.get("type"))
    if handler:
        return handler(event, server)

def getif(config, name, envvar):
    if envvar in os.environ:
        config[name] = os.environ.get(envvar)

def init_config():
    config = {}
    getif(config, "token", "SLACK_TOKEN")
    getif(config, "loglevel", "LIMBO_LOGLEVEL")
    getif(config, "logfile", "LIMBO_LOGFILE")
    getif(config, "logformat", "LIMBO_LOGFORMAT")
    return config

def loop(server):
    try:
        while True:
            # This will cause a broken pipe to reveal itself
            server.slack.server.ping()

            events = server.slack.rtm_read()
            for event in events:
                logger.debug("got {0}".format(event.get("type", event)))
                response = handle_event(event, server)
                if response:
                    server.slack.rtm_send_message(event["channel"], response)

            time.sleep(1)
    except KeyboardInterrupt:
        if os.environ.get("LIMBO_DEBUG"):
            import ipdb; ipdb.set_trace()
        raise

def relevant_environ():
    return dict((key, val)
                for key, val in os.environ.iteritems()
                if key.startswith("SLACK") or key.startswith("LIMBO"))

def init_server(args, config, Server=LimboServer, Client=SlackClient):
    init_log(config)
    logger.debug("config: {0}".format(config))
    db = init_db(args.database_name)
    hooks = init_plugins(args.pluginpath)
    try:
        slack = Client(config["token"])
    except KeyError:
        logger.error("""Unable to find a slack token. The environment variables
limbo sees are:
{0}

and the current config is:
{1}

Try setting your bot's slack token with:

export SLACK_TOKEN=<your-slack-bot-token>
""".format(relevant_environ(), config))
        raise
    server = Server(slack, config, hooks, db)
    return server

# decode a string. if str is a python 3 string, do nothing.
def decode(str_, codec='utf8'):
    if PYTHON3:
        return str_
    else:
        return str_.decode(codec)

# encode a string. if str is a python 3 string, do nothing.
def encode(str_, codec='utf8'):
    if PYTHON3:
        return str_
    else:
        return str_.encode(codec)

def main(args):
    config = init_config()
    if args.test:
        init_log(config)
        return repl(FakeServer(), args)
    elif args.command is not None:
        init_log(config)
        cmd = decode(args.command)
        print(run_cmd(cmd, FakeServer(), args.hook, args.pluginpath))
        return

    server = init_server(args, config)

    if server.slack.rtm_connect():
        # run init hook. This hook doesn't send messages to the server (ought it?)
        run_hook(server.hooks, "init", server)

        loop(server)
    else:
        logger.warn("Connection Failed, invalid token <{0}>?".format(config["token"]))

# run a command. cmd should be a unicode string (str in python3, unicode in python2).
# returns a string appropriate for printing (str in py2 and py3)
def run_cmd(cmd, server, hook, pluginpath):
    server.hooks = init_plugins(pluginpath)
    event = {'type': hook, 'text': cmd, "user": "2", 'ts': time.time(), 'team': None, 'channel': None}
    return encode(handle_event(event, server))

# raw_input in 2.6 is input in python 3. Set `input` to the correct function
try:
    input = raw_input
except NameError:
    pass

def repl(server, args):
    try:
        while 1:
            cmd = decode(input("limbo> "))
            if cmd.lower() == "quit" or cmd.lower() == "exit":
                return

            print(run_cmd(cmd, server, args.hook, args.pluginpath))
    except (EOFError, KeyboardInterrupt):
        print()
        pass

def init_db(database_file):
    return sqlite3.connect(database_file)
