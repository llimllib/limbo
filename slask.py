#!/usr/bin/env python
from config import config
from glob import glob
import importlib
import os
import re
from slackclient import SlackClient
import sys
import time
import traceback

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)

from config import config

hooks = {}
def init_plugins():
    for plugin in glob('plugins/[!_]*.py'):
        print "plugin: {0}".format(plugin)
        try:
            mod = importlib.import_module(plugin.replace(os.path.sep, ".")[:-3])
            modname = mod.__name__.split('.')[1]
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                print "attaching {0}.{1} to {2}".format(modname, hookfun, hook)
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            print "import failed on module {0}, module not loaded".format(plugin)
            print "{0}".format(sys.exc_info()[0])
            print "{0}".format(traceback.format_exc())

init_plugins()

def run_hook(hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

def handle_message(client, event):
    # ignore bot messages and edits
    subtype = event.get("subtype", "")
    if subtype == "bot_message" or subtype == "message_changed": return

    botname = sc.server.login_data["self"]["name"]
    try:
        msguser = client.server.users.get(event["user"])
    except KeyError:
        print "event {0} has no user".format(event)
        return

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    text = "\n".join(run_hook("message", event, {"client": client, "config": config, "hooks": hooks}))

    if text:
        client.rtm_send_message(event["channel"], text)

event_handlers = {
    "message": handle_message
}

if __name__=="__main__":
    sc = SlackClient(config["token"])
    if sc.rtm_connect():
        users = sc.server.users
        while True:
            events = sc.rtm_read()
            for event in events:
                #print "got {0}".format(event.get("type", event))
                handler = event_handlers.get(event.get("type"))
                if handler:
                    handler(sc, event)
            time.sleep(1)
    else:
        print "Connection Failed, invalid token <{0}>?".format(config["token"])
