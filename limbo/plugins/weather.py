# -*- coding: utf-8 -*-
"""!weather <zip or place name> return the 5-day forecast"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import json
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
    "5": ":snow_cloud:",
    "6": ":snow_cloud:",
    "7": ":snow_cloud:",
    "8": ":snow_cloud:",
    "9": ":rain_cloud:",
    "10": ":snow_cloud:",
    "11": ":rain_cloud:",
    "12": ":rain_cloud:",
    "13": ":snow_cloud:",
    "14": ":snow_cloud:",
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


class WeatherException(Exception):
    """An exception finding the weather"""
    pass


def weather(searchterm):
    """Get the weather for a place given by searchterm

    Returns a title and a list of forecasts.

    The title describes the location for the forecast (i.e. "Portland, ME USA")
    The list of forecasts is a list of dictionaries in slack attachment fields
        format (see https://api.slack.com/docs/message-attachments)

    Throws WeatherException if the location given by `searchterm` can't be
    found.
    """
    yql = u'select * from weather.forecast where woeid in '\
          '(select woeid from geo.places(1) where text="{}")'.format(
              searchterm)

    unit = "c" if os.environ.get("WEATHER_CELSIUS") else "f"
    if unit == "c":
        yql += u' AND u="c"'

    url = 'https://query.yahooapis.com/v1/public/yql?'\
          'q={}&format=json'.format(quote(yql.encode('utf8')))

    dat = requests.get(url).json()
    if 'query' not in dat or not dat['query']['results']:
        logging.warning('weather response missing fields. response: %s', dat)
        raise WeatherException(
            ":crying_cat_face: Sorry, weather request failed"
            ":crying_cat_face:")

    forecast = dat['query']['results']['channel']['item']['forecast']
    location = dat['query']['results']['channel']['location']

    region = location['region'].strip()
    if region == location["city"].strip():
        region = ""
    else:
        region = "{} ".format(region)

    title = "Weather for {}, {}{}: ".format(location["city"], region,
                                            location['country'])

    forecasts = []
    for day in forecast:
        day_of_wk = time.strftime("%A", time.strptime(day["date"], "%d %b %Y"))
        icon = ICONMAP.get(day["code"], ":question:")
        forecasts.append({
            "title": day_of_wk,
            "value": u"{} {}°{}".format(icon, day["high"], unit),
            "short": True,
        })

    return title, forecasts


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!weather (.*)", text)
    if not match:
        return

    try:
        title, forecasts = weather(match[0])
    except WeatherException as err:
        return err.args[0]

    attachment = {
        "fallback": title,
        "pretext": title,
        "fields": forecasts[0:4]
    }
    server.slack.post_message(
        msg['channel'],
        '',
        as_user=server.slack.username,
        attachments=json.dumps([attachment]))


on_bot_message = on_message
