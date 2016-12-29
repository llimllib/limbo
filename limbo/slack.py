from collections import namedtuple
import json
import requests
from ssl import SSLError
import time
from websocket import create_connection

# python 2.7.9+ and python 3 have this error
try:
    from ssl import SSLWantReadError
except ImportError:
    SSLWantReadError = SSLError

try:
    # Try for Python3
    from urllib.parse import urlencode
    from urllib.request import urlopen
except:
    # Looks like Python2
    from urllib import urlencode
    from urllib2 import urlopen

# Exceptions
class SlackNotConnected(Exception): pass
class SlackConnectionError(Exception): pass
class SlackLoginError(Exception): pass

User = namedtuple('User', 'server name id real_name tz')
Bot = namedtuple('Bot', 'id name icons deleted')

class Channel(object):
    def __init__(self, server, name, id, members=[]):
        self.server = server
        self.name = name
        self.id = id
        self.members = members

    def __eq__(self, compare_str):
        if self.name == compare_str or self.name == "#" + compare_str or self.id == compare_str:
            return True
        else:
            return False

    def __str__(self):
        data = ""
        for key in list(self.__dict__.keys()):
            data += "{0} : {1}\n".format(key, str(self.__dict__[key])[:40])
        return data

    def __repr__(self):
        return self.__str__()

    def send_message(self, message):
        message_json = {"type": "message", "channel": self.id, "text": message}
        self.server.send_to_websocket(message_json)

class SlackClient(object):
    def __init__(self, token):
        self.token = token
        self.username = None
        self.userid = None
        self.domain = None
        self.login_data = None
        self.websocket = None
        self.users = {}
        self.channels = {}
        self.bots = {}
        self.connected = False
        self.pingcounter = 0

    def api_call(self, method, **kwargs):
        return self.server.api_call(method, **kwargs)

    def rtm_read(self):
        data = [json.loads(d) for d in self.websocket_safe_read()]

        # update client state
        for item in data:
            self.process_changes(item)

        return data

    def rtm_send_message(self, channel_id, message):
        return self.channels[channel_id].send_message(message)

    def post_message(self, channel_id, message, **kwargs):
        params = {
            "post_data": {
                "text": message,
                "channel": channel_id,
            }
        }
        params["post_data"].update(kwargs)

        self.api_call("chat.postMessage", **params)

    def process_changes(self, data):
        if "type" in data.keys():
            if data["type"] in ('channel_created', 'group_joined'):
                channel = data["channel"]
                self.attach_channel(channel["name"], channel["id"], [])
            if data["type"] == "im_created":
                channel = data["channel"]
                self.attach_channel(channel["user"], channel["id"], [])
            elif data["type"] == "team_join":
                user = data["user"]
                self.parse_user_data([user])
            pass

    def rtm_connect(self, reconnect=False):
        reply = self.do("rtm.start")
        if reply.status_code != 200:
            raise SlackConnectionError
        else:
            login_data = reply.json()
            if login_data["ok"]:
                self.ws_url = login_data['url']
                if not reconnect:
                    self.parse_slack_login_data(login_data)
                self.connect_slack_websocket(self.ws_url)
            else:
                raise SlackLoginError

    def parse_slack_login_data(self, login_data):
        self.login_data = login_data
        self.domain = self.login_data["team"]["domain"]
        self.username = self.login_data["self"]["name"]
        self.userid = self.login_data["self"]["id"]
        self.parse_channel_data(login_data["channels"])
        self.parse_channel_data(login_data["groups"])
        self.parse_channel_data(login_data["ims"])
        self.parse_user_data(login_data["users"])
        self.parse_bot_data(login_data["bots"])

    def connect_slack_websocket(self, ws_url):
        try:
            self.websocket = create_connection(ws_url)
            self.websocket.sock.setblocking(0)
        except:
            raise SlackConnectionError

    def parse_channel_data(self, channel_data):
        for channel in channel_data:
            if "name" not in channel:
                channel["name"] = channel["id"]
            if "members" not in channel:
                channel["members"] = []

            self.attach_channel(channel['name'], channel['id'], channel['members'])

    def parse_user_data(self, user_data):
        for user in user_data:
            if "tz" not in user:
                user["tz"] = "unknown"
            if "real_name" not in user:
                user["real_name"] = user["name"]

            id = user['id']
            name = user['name']
            real_name = user['real_name']
            tz = user['tz']

            self.users[user['id']] = User(self, name, id, real_name, tz)

    def parse_bot_data(self, bot_data):
        for bot in bot_data:
            self.bots[bot['id']] = Bot(bot['id'], bot['name'], bot.get('icons', ''), bot['deleted'])

    def send_to_websocket(self, data):
        """Send (data) directly to the websocket."""
        try:
            data = json.dumps(data)
            self.websocket.send(data)
        except:
            self.rtm_connect(reconnect=True)

    def ping(self):
        return self.send_to_websocket({"type": "ping"})

    def websocket_safe_read(self):
        """ Returns data if available, otherwise ''. Newlines indicate multiple
            messages
        """
        data = []
        while True:
            try:
                data.append(self.websocket.recv())
            except (SSLError, SSLWantReadError) as e:
                if e.errno == 2:
                    # errno 2 occurs when trying to read or write data, but more
                    # data needs to be received on the underlying TCP transport
                    # before the request can be fulfilled.
                    return data
                raise

    def attach_channel(self, name, id, members=[]):
        self.channels[id] = Channel(self, name, id, members)

    def join_channel(self, name):
        print(self.do("channels.join?name={0}".format(name)).read())

    def api_call(self, method, **kwargs):
        reply = self.do(method, **kwargs)
        return reply.text

    def do(self, request, post_data={}, files=None):
        url = 'https://slack.com/api/{0}'.format(request)
        post_data["token"] = self.token
        return requests.post(url, data=post_data, files=files)
