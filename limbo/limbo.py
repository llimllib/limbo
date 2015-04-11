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

from slackclient import SlackClient
from server import LimboServer
from fakeserver import FakeServer

CURDIR = os.path.abspath(os.path.dirname(__file__))
DIR = functools.partial(os.path.join, CURDIR)

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
        msguser = server.slack.server.users.get(event["user"])
    except KeyError:
        logger.debug("event {0} has no user".format(event))
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
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

def init_server(args, Server=LimboServer, Client=SlackClient):
    config = init_config()
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

def main(args):
    if args.test:
        config = init_config()
        init_log(config)
        return repl(FakeServer(), args)
    elif args.command is not None:
        config = init_config()
        init_log(config)
        print(run_cmd(args.command, FakeServer(), args.hook, args.pluginpath).encode("utf8"))
        return

    server = init_server(args)

    if server.slack.rtm_connect():
        # run init hook. This hook doesn't send messages to the server (ought it?)
        run_hook(server.hooks, "init", server)

        loop(server)
    else:
        logger.warn("Connection Failed, invalid token <{0}>?".format(config["token"]))

def run_cmd(cmd, server, hook, pluginpath):
    server.hooks = init_plugins(pluginpath)
    if type(cmd) == str:
        cmd = cmd.decode("utf8")
    event = {'type': hook, 'text': cmd, "user": "msguser", 'ts': time.time(), 'team': None, 'channel': None}
    return handle_event(event, server)

def repl(server, args):
    try:
        while 1:
            cmd = raw_input("limbo> ").decode("utf8")
            if cmd.lower() == "quit" or cmd.lower() == "exit":
                return

            print(run_cmd(cmd, server, args.hook, args.pluginpath).encode("utf8"))
    except (EOFError, KeyboardInterrupt):
        print()
        pass

def init_db(database_file):
    return sqlite3.connect(database_file)
