"""!help [<command>] prints help on all commands if no command given, or a specific command"""

import re


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!help( .*)?", text)
    if not match:
        return

    helptopic = match[0].strip()
    if helptopic:
        return server.hooks["extendedhelp"].get(
            helptopic, "No help found for {0}".format(helptopic))
    else:
        # if no plugin has a docstring, there's no help key
        helpdict = server.hooks.get("help", {})
        return "\n".join(sorted(helpdict[key] for key in helpdict))


on_bot_message = on_message
