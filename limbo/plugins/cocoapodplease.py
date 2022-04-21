"""!cocoapod <parameter> returns search results from cocoapods.org"""
import re
import requests
import json


def cocoapods(q):
    url = "http://search.cocoapods.org/api/pods?query={0}".format(q)
    rawText = requests.get(url).text
    data = json.loads(rawText)
     
    docs = data.get("allocations")[0][5]
    result = '```'

    for x in docs:
        result +='\'' + x + '\'\n'

    result += '```'
    return result


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!cocoapod (.*)", text)
    if not match:
        return

    return cocoapods(match[0])