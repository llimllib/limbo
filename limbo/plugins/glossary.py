# -*- coding: utf-8 -*-
"""
!glossary `term` returns the definition for `term` or "I don't know that term."
!glossary add `term`: `definition` adds the definition to limbo's glossary
!glossary remove `term` removes `term` from the glossary
!glossary search `term` to search all entries for `term`
"""

import re


def on_init(server):
    server.query("""
CREATE TABLE IF NOT EXISTS glossary(term text, definition text)
""")


def get(term, server):
    results = server.query(
        """
SELECT term, definition FROM glossary WHERE term LIKE ?
""", term)
    return results[0] if results else None


def search(term, server):
    wildterm = f"%{term}%"
    results = server.query(
        """
select term, definition from glossary WHERE term LIKE ? OR definition LIKE ?;
""", wildterm, wildterm)
    if not results:
        return f"No results found for {term}"
    else:
        return "\n".join(f"*{result[0]}*: {result[1]}" for result in results)


def add(term, definition, server):
    results = get(term, server)
    if not results:
        server.query(
            """
INSERT INTO glossary(term, definition) VALUES (?, ?)
""", term, definition)
        return f"Successfully added {term}"
    else:
        server.query(
            """
UPDATE glossary SET definition=? WHERE term=?
        """, definition, results[0])
        return f"Successfully updated {term}"


def remove(term, server):
    results = get(term, server)
    if not results:
        return f"No definition found for {term}"
    else:
        # if case is different, stick with the version in the DB.
        # this prevents separate definitions for FOO and Foo
        term = results[0]

    server.query("""
DELETE FROM glossary WHERE term=?
""", term)

    return f"Removed definition for {term}"


def lookup(term, server):
    results = get(term, server)
    if not results:
        return (f"No definition found for {term}. Add a definition with "
                "'!glossary add <term>: <definition>'.")

    return f"*{results[0]}*: {results[1]}"


def sanitize_definition(definition):
    # if there are links, de-slackify them and remove the leading ':'
    # slack links can be of the form <http://google.com> or of the form
    # <http://google.com|title of the link>.
    return re.sub("<(.*?)>", lambda x: x.group(1).split("|")[0], definition) \
            .lstrip(':') \
            .strip()


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.search(r'!gloss(ary)? (add|remove\s+|search)?([^:]*)(.*)?',
                      text, re.IGNORECASE)

    if not match:
        return

    groups = match.groups()
    if groups[1]:
        action = groups[1].strip()
        if action == 'add':
            term = groups[2].strip()
            definition = sanitize_definition(groups[3])
            return add(term, definition, server)
        elif action == 'remove':
            return remove(groups[2].strip(), server)
        elif action == 'search':
            return search(groups[2].strip(), server)
    else:
        return lookup(groups[2], server)


on_bot_message = on_message
