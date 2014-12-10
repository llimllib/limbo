#!/usr/bin/env python
from config import config
import requests
from slackclient import SlackClient
import time

curdir = os.path.dirname(os.path.abspath(__file__))
os.chdir(curdir)

from config import config

hooks = {}
def init_plugins():
    for plugin in glob('plugins/[!_]*.py'):
        print "plugin: %s" % plugin
        try:
            mod = importlib.import_module(plugin.replace(os.path.sep, ".")[:-3])
            modname = mod.__name__.split('.')[1]
            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                print "attaching %s.%s to %s" % (modname, hookfun, hook)
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', {})[modname] = firstline
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            print "import failed on module %s, module not loaded" % plugin
            print "%s" % sys.exc_info()[0]
            print "%s" % traceback.format_exc()

init_plugins()

def run_hook(hook, data, server):
    responses = []
    for hook in hooks.get(hook, []):
        h = hook(data, server)
        if h: responses.append(h)

    return responses

API_BASE_URL = 'https://slack.com/api/{method}?token={token}'
def call(method, **params):
    url = API_BASE_URL.format(method=method, token=TOKEN)
    return requests.get(url, params=params).json()

#info = call("rtm.start")

def handle_message(client, event):
    # how to get our own username?
    botname = sc.server.login_data["self"]["name"]
    msguser = client.server.users.get(event["user"])

    if msguser["name"] == botname or msguser["name"].lower() == "slackbot":
        return

    text = "hello"

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
                print "got {}".format(event.get("type", event))
                handler = event_handlers.get(event.get("type"))
                if handler:
                    handler(sc, event)
            time.sleep(1)
    else:
        print "Connection Failed, invalid token <{}>?".format(config["token"])
