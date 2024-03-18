"""Add items to a list and get items from a list or get existing lists, use !list add|get|getlists [listname] [item]"""
import re


def add(server, listname, item, msg):
    server.query("INSERT INTO lists VALUES (?, ?, ?, ?, ?, ?)",
                listname, item, msg["user"], msg["ts"], msg["team"], msg["channel"])


def get(server, list):
    result = server.query("SELECT msg FROM lists WHERE list == ? ORDER BY random() LIMIT 1", listname)
    if len(result) == 1:
        return result[0][0]
    else:
        return "List not found"

def get_lists(server):
    result = server.query("SELECT DISTINCT list FROM lists ORDER BY list")
    if len(result) > 1:
        # todo: better formatting
        res = ""
        for r in result:
            res+=r[0]+"\n"
        return res[:-1]
    else:
        return "No lists found"

def on_message(msg, server):
    """
    :type server: limbo.server.LimboServer
    :return:
    """
    text = msg.get("text", "")
    match = re.findall(r"!list\s+(.*)", text)
    if not match:
        return

    command = match[0].split(" ")

    if command[0] == "add":
        if len(command) > 1:
            item = " ".join(command[2:])
            return add(server, command[1], item, msg)
    elif command[0] == "get":
        if len(command) == 2:
            return get(server, command[1])
    elif command[0] == "getlists":
        return get_lists(server)
    return "Command wrongly formated, use 'add <list> msg' or 'get <list>' to get random element form list or 'get_lists' to get existing lists"

def on_reaction(msg, server):
    print("here")

def on_init(server):
    server.query("""
CREATE TABLE IF NOT EXISTS lists
    (list STRING, msg STRING, sender STRING, time STRING, team STRING, channel STRING)
""")
