# -*- coding: utf-8 -*-
import json
import os
import re

"""
!glossary <term> returns the term definition OR "I don't know that term."
!glossary add <term>: <definition> adds the definition to limbo's glossary
"""

GLOSSARY_FILE = os.environ.get('LIMBO_GLOSSARY_FILE', "/tmp/glossary.json")


def add(term, definition):
    with open(GLOSSARY_FILE, 'r') as f:
        try:
            glossary = json.loads(f.read())
        except ValueError:
            glossary = {}

    action = bool(glossary.get(term, False)) and "Updated" or "Added"
    glossary[term] = definition

    with open(GLOSSARY_FILE, 'w') as f:
        f.write(json.dumps(glossary))

    return "%s a definition for %s"% (action, term)

def remove(term):
    with open(GLOSSARY_FILE, 'r') as f:
        try:
            glossary = json.loads(f.read())
        except ValueError:
            return "There aren't any definitions to remove yet! Add a definition with '!glossary add <term>: <definition>'"

    del(glossary[term])

    with open(GLOSSARY_FILE, 'w') as f:
        f.write(json.dumps(glossary))

    return "Removed definition for %s" % term

def lookup(term):
    not_found = "I don't know that term. Add a definition with '!glossary add <term>: <definition>'."

    try:
        with open(GLOSSARY_FILE, 'r') as f:
            try:
                glossary = json.loads(f.read())
            except ValueError:
                glossary = {}
            definition = glossary.get(term, None)
            if not definition:
                return not_found
            return definition
    except IOError:
        return not_found


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.match(r'!gloss(ary)? (add|remove\s+)?([^:]*)(.*)?', text, re.IGNORECASE)

    if not match:
        return

    if not os.path.isfile(GLOSSARY_FILE):
        open(GLOSSARY_FILE, 'a').close()

    groups = match.groups()
    if groups[1]:
        action = groups[1].strip()
        if action == 'add':
            term = groups[2].strip()
            definition = groups[3].lstrip(':').strip()
            return add(term, definition)
        elif action == 'remove':
            return remove(groups[2])
    else:
        return lookup(groups[2])

on_bot_message = on_message
