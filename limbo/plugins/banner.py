# -*- coding: utf-8 -*-
"""!banner <text> [--font <font>] [-l] return a banner displaying <text>. Use the -l option to list available fonts"""

import argparse
import re
import pyfiglet

FIGLET = pyfiglet.Figlet()
FONTS = FIGLET.getFonts()

ARGPARSE = argparse.ArgumentParser()
ARGPARSE.add_argument('--font')
ARGPARSE.add_argument('-l', action='store_const', const=True)
ARGPARSE.add_argument('bannertext', nargs='*')

def make_banner(query):
    # Slack turns -- into an emdash; un-turn it
    query = query.replace(u"\u2014", u"--")

    ns = ARGPARSE.parse_args(query.split(" "))
    if ns.l:
        return "```{0}```".format(", ".join(FONTS))
    font = ns.font or "standard"

    if font not in FONTS:
        return "Unable to find font {0}".format(font)

    banner = pyfiglet.figlet_format(" ".join(ns.bannertext), font=font).rstrip()
    if not banner:
        return

    return "```{0}```".format(banner)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!banner (.*)", text)
    if not match:
        return

    return make_banner(match[0])
