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
from server import SlaskServer
from fakeserver import FakeServer

CURDIR = os.path.abspath(os.path.dirname(__file__))
DIR = functools.partial(os.path.join, CURDIR)

class InvalidPluginDir(Exception):
    def __init__(self, plugindir):
        self.message = "Unable to find plugin dir {0}".format(plugindir)

def init_log(config):
    loglevel = config.get("loglevel", logging.INFO)
    logformat = config.get("logformat", '%(asctime)s:%(levelname)s:%(message)s')
    if config.get("logfile"):
        logfile = config.get("logfile", "slask.log")
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()

    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(loglevel)
    handler.setLevel(loglevel)

    # create formatter
    formatter = logging.Formatter(logformat)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # make it the root logger (I hate the logging module)
    logging.root = logger

def init_plugins(plugindir):
    if not plugindir:
        plugindir = DIR("plugins")

    logging.debug("plugindir: {0}".format(plugindir))

    if not os.path.isdir(plugindir):
        raise InvalidPluginDir(plugindir)

    hooks = {}

    oldpath = copy.deepcopy(sys.path)
    sys.path.insert(0, plugindir)

    for plugin in glob(os.path.join(plugindir, "[!_]*.py")):
        logging.debug("plugin: {0}".format(plugin))
        try:
            mod = importlib.import_module(os.path.basename(plugin)[:-3])
            modname = mod.__name__
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                logging.debug("attaching {0}.{1} to {2}".format(modname, hookfun, hook))
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            logging.warning("import failed on module {0}, module not loaded".format(plugin))
            logging.warning("{0}".format(sys.exc_info()[0]))
            logging.warning("{0}".format(traceback.format_exc()))

    sys.path = oldpath
    return hooks

def run_hook(hooks, hook, *args):
    responses = []
    for hook in hooks.get(hook, []):
        try:
            h = hook(*args)
            if h: responses.append(h)
        except:
            logging.warning("Failed to run plugin {0}, module not loaded".format(hook))
            logging.warning("{0}".format(sys.exc_info()[0]))
            logging.warning("{0}".format(traceback.format_exc()))

    return responses

def handle_message(event, server):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed": return

    botname = server.slack.server.login_data["self"]["name"]
    try:
        msguser = server.slack.server.users.get(event["user"])
    except KeyError:
        logging.debug("event {0} has no user".format(event))
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    return "\n".join(run_hook(server.hooks, "message", event, server))

event_handlers = {
    "message": handle_message
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
    getif(config, "loglevel", "SLASK_LOGLEVEL")
    getif(config, "logfile", "SLASK_LOGFILE")
    getif(config, "logformat", "SLASK_LOGFORMAT")
    return config

def loop(server):
    while True:
        events = server.slack.rtm_read()
        for event in events:
            logging.debug("got {0}".format(event.get("type", event)))
            response = handle_event(event, server)
            if response:
                server.slack.rtm_send_message(event["channel"], response)
        time.sleep(1)

def init_server(args, Server=SlaskServer, Client=SlackClient):
    config = init_config()
    init_log(config)
    logging.debug("config: {0}".format(config))
    db = init_db(args.database_name)
    hooks = init_plugins(args.pluginpath)
    slack = Client(config["token"])
    server = Server(slack, config, hooks, db)
    return server

def main(args):
    if args.test:
        return repl(FakeServer(), args)
    elif args.command is not None:
        print(run_cmd(args.command, FakeServer(), args.hook, args.pluginpath).encode("utf8"))
        return

    server = init_server(args)

    if server.slack.rtm_connect():
        #run init hook. This hook doesn't send messages to the server (ought it?)
        run_hook(server.hooks, "init", server)

        loop(server)
    else:
        logging.warn("Connection Failed, invalid token <{0}>?".format(config["token"]))

def run_cmd(cmd, server, hook, pluginpath):
    server.hooks = init_plugins(pluginpath)
    if type(cmd) == str:
        cmd = cmd.decode("utf8")
    event = { 'type': hook, 'text': cmd, "user": "msguser", 'ts': time.time(), 'team': None, 'channel': None}
    return handle_event(event, server)

def repl(server, args):
    try:
        while 1:
            cmd = raw_input("slask> ").decode("utf8")
            if cmd.lower() == "quit" or cmd.lower() == "exit":
                return

            print(run_cmd(cmd, server, args.hook, args.pluginpath).encode("utf8"))
    except (EOFError, KeyboardInterrupt):
        print()
        pass

def init_db(database_file):
    return sqlite3.connect(database_file)
