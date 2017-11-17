# -*- coding: utf-8 -*-
"""!weather <zip or place name> return the 5-day forecast"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import logging
import os
import re
import time

import requests

# https://developer.yahoo.com/weather/documentation.html
ICONMAP = {
    "0": ":tornado:",
    "1": ":cyclone:",
    "2": ":cyclone:",
    "3": ":thunder_cloud_and_rain:",
    "4": ":thunder_cloud_and_rain:",
    "5": ":snowflake:",
    "6": ":snowflake:",
    "7": ":snowflake:",
    "8": ":snowflake:",
    "9": ":rain_cloud:",
    "10": ":snowflake:",
    "11": ":rain_cloud:",
    "12": ":rain_cloud:",
    "13": ":snowflake",
    "14": ":snowflake:",
    "15": ":snowflake:",
    "16": ":snowflake:",
    "17": ":thunder_cloud_and_rain:",
    "18": ":rain_cloud:",
    "19": ":desert:",
    "20": ":cloud:",
    "21": ":cloud:",
    "22": ":smoking:",
    "23": ":wind_blowing_face:",
    "24": ":wind_blowing_face:",
    "25": ":snowman_without_snow:",
    "26": ":cloud:",
    "27": ":sun_behind_cloud:",
    "28": ":sun_behind_cloud:",
    "29": ":sun_small_cloud:",
    "30": ":sun_small_cloud:",
    "32": ":sunny:",
    "33": ":sunny:",
    "34": ":sunny:",
    "35": ":thunder_cloud_and_rain:",
    "36": ":sunny:",
    "37": ":thunder_cloud_and_rain:",
    "38": ":thunder_cloud_and_rain:",
    "39": ":thunder_cloud_and_rain:",
    "40": ":rain_cloud:",
    "41": ":snowflake:",
    "42": ":snowflake:",
    "43": ":snowflake:",
    "44": ":partly_sunny:",
    "45": ":thunder_cloud_and_rain:",
    "46": ":snowflake:",
    "47": ":thunder_cloud_and_rain:",
}

def weather(searchterm):
    yql = 'select * from weather.forecast where woeid in '\
          '(select woeid from geo.places(1) where text="{}")'.format(
              searchterm)
    if os.environ.get("WEATHER_CELSIUS"):
        yql += ' AND u="c"'

    url = 'https://query.yahooapis.com/v1/public/yql?'\
          'q={}&format=json'.format(quote(yql.encode('utf8')))

    dat = requests.get(url).json()
    if 'query' not in dat or not dat['query']['results']:
        logging.warning('weather response missing fields. response: %s', dat)
        return ":crying_cat_face: Sorry, weather request failed :crying_cat_face:"

    forecast = dat['query']['results']['channel']['item']['forecast']
    location = dat['query']['results']['channel']['location']

    msg = ["{}, {}: ".format(location["city"], location['region'].strip())]
    for day in forecast[:5]:
        name = time.strftime("%a", time.strptime(day["date"], "%d %b %Y"))
        icon = ICONMAP.get(day["code"], ":question:")
        msg.append(u"{0} {1}° {2}".format(name, day["high"], icon))

    return " ".join(msg)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!weather (.*)", text)
    if not match:
        return

    return weather(match[0])

on_bot_message = on_message
