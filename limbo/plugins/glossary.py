# -*- coding: utf-8 -*-
"""
!glossary `term` returns the definition for `term` or "I don't know that term."
!glossary add `term`: `definition` adds the definition to limbo's glossary
!glossary remove `term` removes `term` from the glossary
"""

import re

def on_init(server):
    server.query("""
CREATE TABLE IF NOT EXISTS glossary(term text, definition text)
""")

def get(term, server):
    results = server.query("""
SELECT term, definition FROM glossary WHERE term LIKE ?
""", term)
    return results[0] if results else None

def add(term, definition, server):
    results = get(term, server)
    if not results:
        server.query("""
INSERT INTO glossary(term, definition) VALUES (?, ?)
""", term, definition)
        return "Successfully added {}".format(term)
    else:
        server.query("""
UPDATE glossary SET definition=? WHERE term=?
        """, definition, results[0])
        return "Successfully updated {}".format(term)

def remove(term, server):
    results = get(term, server)
    if not results:
        return "No definition found for {}".format(term)
    else:
        # if case is different, stick with the version in the DB.
        # this prevents separate definitions for FOO and Foo
        term = results[0]

    server.query("""
DELETE FROM glossary WHERE term=?
""", term)

    return "Removed definition for {}".format(term)

def lookup(term, server):
    results = get(term, server)
    if not results:
        return ("No definition found for {}. Add a definition with "
        "'!glossary add <term>: <definition>'.".format(term))

    return "{}: {}".format(*results)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.match(r'!gloss(ary)? (add|remove\s+)?([^:]*)(.*)?', text, re.IGNORECASE)

    if not match:
        return

    groups = match.groups()
    if groups[1]:
        action = groups[1].strip()
        if action == 'add':
            term = groups[2].strip()
            definition = groups[3].lstrip(':').strip()
            return add(term, definition, server)
        elif action == 'remove':
            return remove(groups[2], server)
    else:
        return lookup(groups[2], server)

on_bot_message = on_message
