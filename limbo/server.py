class LimboServer(object):
    def __init__(self, slack, config, hooks, db):
        self.slack = slack
        self.config = config
        self.hooks = hooks
        self.db = db

    def query(self, sql, *params):
        c = self.db.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        c.close()
        self.db.commit()
        return rows
