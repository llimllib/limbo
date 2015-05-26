from .slackclient._util import SearchList
from .slackclient._user import User

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

class FakeSlackServer(object):
    def __init__(self, botname="limbo_test", users=None):
        self.login_data = {
            "self": {
                "name": botname,
            }
        }

        if  users:
            self.users = users
        else:
            self.users = SearchList([
                User(self, "limbo_test", 1, "", 0),
                User(self, "msguser", 2, "", 0),
                User(self, "slackbot", 3, "", 0),
            ])
