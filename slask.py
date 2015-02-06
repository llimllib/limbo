#!/usr/bin/env python
from __future__ import print_function
from glob import glob
import importlib
import logging
import os
import re
import sys
import time
import traceback

from slackclient import SlackClient

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
    hooks = {}

    for plugin in glob(os.path.join(plugindir, "[!_]*.py")):
        logging.debug("plugin: {0}".format(plugin))
        try:
            mod = importlib.import_module(plugin.replace(os.path.sep, ".")[:-3])
            modname = mod.__name__.split('.')[1]
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
            logging.info("import failed on module {0}, module not loaded".format(plugin))
            logging.info("{0}".format(sys.exc_info()[0]))
            logging.info("{0}".format(traceback.format_exc()))

    return hooks

def run_hook(hooks, hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def handle_message(client, event, hooks, config):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed": return

    botname = client.server.login_data["self"]["name"]
    try:
        msguser = client.server.users.get(event["user"])
    except KeyError:
        logging.debug("event {0} has no user".format(event))
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    return "\n".join(run_hook(hooks, "message", event, {"client": client, "config": config, "hooks": hooks}))

event_handlers = {
    "message": handle_message
}

def handle_event(client, event, hooks, config):
    handler = event_handlers.get(event.get("type"))
    if handler:
        return handler(client, event, hooks, config)
    return None

def main(config):
    init_log(config)
    hooks = init_plugins("plugins")

    client = SlackClient(config["token"])
    if client.rtm_connect():
        users = client.server.users
        while True:
            events = client.rtm_read()
            for event in events:
                logging.debug("got {0}".format(event.get("type", event)))
                response = handle_event(client, event, hooks, config)
                if response:
                    client.rtm_send_message(event["channel"], response)
            time.sleep(1)
    else:
        logging.warn("Connection Failed, invalid token <{0}>?".format(config["token"]))

def run_cmd(client, cmd, hook):
    hooks = init_plugins("plugins")
    event = { 'type': hook, 'text': cmd, "user": "msguser" }
    return handle_event(client, event, hooks, config)

def repl(config, client, hook):
    try:
        while 1:
            cmd = raw_input("slask> ")
            if cmd.lower() == "quit" or cmd.lower() == "exit":
                return

            print(run_cmd(client, cmd, hook))
    except (EOFError, KeyboardInterrupt):
        print()
        pass

if __name__=="__main__":
    from config import config
    import argparse

    parser = argparse.ArgumentParser(description="Run the slask chatbot for Slack")
    parser.add_argument('--test', '-t', dest='test', action='store_true', required=False,
                        help='Enter command line mode to enter a slask repl')
    parser.add_argument('--hook', dest='hook', action='store', default='message',
                        help='Specify the hook to test. (Defaults to "message")')
    parser.add_argument('-c', dest="command", help='run a single command')
    args = parser.parse_args()

    if args.test:
        from test import FakeClient
        repl(config, FakeClient(), args.hook)
    elif args.command:
        from test import FakeClient
        print(run_cmd(FakeClient(), args.command, args.hook))
    else:
        main(config)
