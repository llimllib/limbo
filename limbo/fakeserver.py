from slackrtm.server import User, Bot

class FakeServer(object):
    def __init__(self, slack=None, config=None, hooks=None, db=None):
        self.slack = slack or FakeSlack()
        self.config = config
        self.hooks = hooks
        self.db = db

    def query(self, sql, *params):
        # XXX: what to do with this?
        return None

class FakeSlack(object):
    def __init__(self, server=None, users=None):
        self.server = server or FakeSlackServer(users=users)

    def post_message(self, channel, message, **kwargs):
        print("message {} posted to channel {} with kwargs {}"\
                .format(message, channel, kwargs))

class FakeSlackServer(object):
    def __init__(self, botname="limbo_test", users=None, bots=None):
        self.login_data = {
            "self": {
                "name": botname,
            }
        }
        self.username = "replbot"

        if  users:
            self.users = users
        else:
            self.users = {
                "1": User(self, "limbo_test", 1, "", 0),
                "2": User(self, "msguser", 2, "", 0),
                "3": User(self, "slackbot", 3, "", 0),
            }

        if bots:
            self.bots = bots
        else:
            self.bots = {
                "1": Bot("1", "otherbot", [], False)
            }
