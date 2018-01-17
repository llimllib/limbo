"""Log all messages to the database

Only active if the LIMBO_LOG_EVERYTHING environment variable is set"""
import os

DO_LOG = os.environ.get("LIMBO_LOG_EVERYTHING", False)


def on_message(msg, server):
    if DO_LOG:
        server.query("INSERT INTO log VALUES (?, ?, ?, ?, ?)", msg["text"],
                     msg["user"], msg["ts"], msg["team"], msg["channel"])


def on_init(server):
    if DO_LOG:
        server.query("""
CREATE TABLE IF NOT EXISTS log
    (msg STRING, sender STRING, time STRING, team STRING, channel STRING)
""")


on_bot_message = on_message
