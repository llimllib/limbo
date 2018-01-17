import json
import time

from .slack import User, Bot


class FakeServer(object):
    def __init__(self, slack=None, config=None, hooks=None, db=None):
        self.slack = slack or FakeSlack()
        self.config = config
        self.hooks = hooks
        self.db = db

    def query(self, sql, *params):
        if not self.db:
            return None

        c = self.db.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        c.close()
        self.db.commit()
        return rows


class FakeSlack(object):
    def __init__(self,
                 server=None,
                 users=None,
                 events=None,
                 bots=None,
                 botname="test"):
        self.posted_messages = []
        self.posted_reactions = {}
        self.events = events if events else []
        self.login_data = {
            "self": {
                "name": botname,
            }
        }
        self.username = "limbo_test"
        self.userid = "1"

        self.users = users if users else {
            "1": User("limbo_test", 1, "", 0),
            "2": User("msguser", 2, "", 0),
            "3": User("slackbot", 3, "", 0),
            "4": User("replbot", 4, "", 0),
        }

        self.bots = bots if bots else {"1": Bot("1", "otherbot", [], False)}

    def post_message(self, channel, message, **kwargs):
        self.posted_messages.append((message, kwargs))
        return json.dumps({"ts": time.time()})

    def post_reaction(self, channel, ts, reaction):
        self.posted_reactions.setdefault(ts, []).append(reaction)

    def rtm_read(self):
        return self.events.pop() if self.events else []
