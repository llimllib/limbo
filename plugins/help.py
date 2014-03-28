"""!help [<command>] prints help on all commands if no command given, or a specific command"""

import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!help( .*)?", text)
    if not match: return

    helptopic = match[0].strip()
    if helptopic:
        return server["hooks"]["help"].get(helptopic, "No help found for %s" % helptopic)
    else:
        return "\n".join(val for _, val in server["hooks"]["help"].iteritems())
