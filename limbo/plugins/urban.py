"""!urban <term> returns the urban dictionary definition and example of a term"""
import requests
import re
import json

def urban(term):
    baseurl = "http://api.urbandictionary.com/v0/define?term={0}"
    data = requests.get(baseurl.format(term.decode("utf8"))).json()
    try:
        result = data['list'][0]
        string = "*{word}*: {definition}.\n*Example:*\n>_{example}_".format(**result)
        return string
    except IndexError:
        return ":cry: No results found for {0}, please try again".format(term)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!urban (.*)", text)
    if not match:
        return
    searchterm = match[0]
    return urban(searchterm.encode("utf8"))
