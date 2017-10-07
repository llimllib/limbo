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

User = namedtuple('User', 'id name real_name tz')
Bot = namedtuple('Bot', 'id name icons deleted')
Channel = namedtuple('Channel', 'id name')

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

    def rtm_read(self):
        data = [json.loads(d) for d in self.websocket_safe_read()]

        # update client state
        for item in data:
            self.process_changes(item)

        return data

    def rtm_send_message(self, channel_id, message):
        message_json = {"type": "message", "channel": channel_id, "text": message}
        self.send_to_websocket(message_json)

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
                self.channels[channel["id"]] = Channel(channel["id"], channel["name"])
            if data["type"] == "im_created":
                channel = data["channel"]
                self.channels[channel["id"]] = Channel(channel["id"], channel["name"])
            elif data["type"] == "team_join":
                user = data["user"]
                self.parse_users([user])
            pass

    def rtm_connect(self, reconnect=False):
        reply = self.do("rtm.connect")
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

        self.get_channel_list()
        self.get_user_list()

    def parse_slack_login_data(self, login_data):
        self.login_data = login_data
        self.team_id = self.login_data["team"]["id"]
        self.domain = self.login_data["team"]["domain"]
        self.username = self.login_data["self"]["name"]
        self.userid = self.login_data["self"]["id"]

    def connect_slack_websocket(self, ws_url):
        try:
            self.websocket = create_connection(ws_url)
            self.websocket.sock.setblocking(0)
        except:
            raise SlackConnectionError

    def _dig(self, obj, *keys):
        for key in keys:
            if not obj or key not in obj:
                return None
            obj = obj[key]
        return obj

    def get_all(self, api_method, collection_name):
        """
        Return all objects in an api_method and handle pagination.

        For example, "users.list" returns an object like:

        {
            "members": [{<member_obj>}, {<member_obj_2>}],
            "response_metadata": {
                "next_cursor": "cursor_id"
            }
        }

        so if you call `get_all("users.list", "members")`, this function
        will return all member objects to you while handling pagination
        """
        objs = []
        # if you don't provide a limit, the slack API won't return a cursor to you
        page = json.loads(self.api_call(api_method, limit=25))
        while 1:
            for obj in page[collection_name]:
                objs.append(obj)

            cursor = self._dig(page, "response_metadata", "next_cursor")
            if cursor:
                page = json.loads(self.api_call(api_method, cursor=cursor))
            else:
                break

        return objs

    def get_channel_list(self):
        # this call may or may not provide members for each channel, so
        # let's not rely on the members being in it. If we need them
        # (which I don't think we do?) we can get them later
        for ch in self.get_all("channels.list", "channels"):
            self.channels[ch["id"]] = Channel(ch['id'], ch["name"])

    def get_user_list(self):
        self.parse_users(self.get_all("users.list", "members"))

    def parse_users(self, users):
        for user in users:
            if "tz" not in user:
                user["tz"] = "unknown"
            if "real_name" not in user:
                user["real_name"] = user["name"]

            if user["is_bot"]:
                self.parse_bot_data(user)
                continue

            id = user['id']
            name = user['name']
            real_name = user['real_name']
            tz = user['tz']

            self.users[user['id']] = User(id, name, real_name, tz)

    def parse_bot_data(self, bot):
        self.bots[bot['id']] = Bot(bot['id'], bot['name'], bot.get('icons', ''), bot['deleted'])

    def send_to_websocket(self, data):
        """Send (data) directly to the websocket."""
        data = json.dumps(data)
        self.websocket.send(data)

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

    def join_channel(self, name):
        print(self.do("channels.join?name={0}".format(name)).read())

    def api_call(self, method, **kwargs):
        reply = self.do(method, **kwargs)
        return reply.text

    def do(self, request, post_data={}, files=None, **kwargs):
        url = 'https://slack.com/api/{0}'.format(request)
        post_data["token"] = self.token
        post_data.update(kwargs)
        return requests.post(url, data=post_data, files=files)
