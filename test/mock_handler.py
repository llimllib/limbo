# -*- coding: utf-8 -*-
import logging

class MockHandler(logging.Handler):
    """A handler class which stores logging records in a list.

    From http://nessita.pastebin.com/mgc85uQT
    """
    def __init__(self, *args, **kwargs):
        """Create the instance, and add a records attribute."""
        logging.Handler.__init__(self, *args, **kwargs)
        self.records = []

    def emit(self, record):
        """Just add the record to self.records."""
        self.records.append(record)

    def check(self, level, msg):
        """Check that something is logged."""
        for rec in self.records:
            if rec.levelname == level and str(msg) in rec.getMessage():
                return True
        return False
