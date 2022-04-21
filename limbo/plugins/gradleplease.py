"""!gradle <parameter> returns search results from mavencentral in gradle format"""
import re
import requests
import json


def gradleplease(q):
    url = "http://gradleplease.appspot.com/search?q={0}".format(q)
    rawText = requests.get(url).text
    data = str(rawText[15:-1])
    asd = json.loads(data)
    docs = asd.get("response").get("docs")

    result = '```'

    for x in docs:
        result +='compile \'' + x.get("id") + ':' + x.get("latestVersion") + '\'\n'

    result += '```'
    return result


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!gradle (.*)", text)
    if not match:
        return

    return gradleplease(match[0])
