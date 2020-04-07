# -*- coding: utf-8 -*-
"""!weather <zip or place name> return the 5-day forecast

Three environment variables control the behavior of this plugin:
    MAPBOX_API_TOKEN: must be set to a valid Mapbox API token
                      https://docs.mapbox.com/api/search/#geocoding
    OPENWEATHER_API_KEY: must be set to a valid OpenWeather API key
                      https://openweathermap.org/current
                      https://openweathermap.org/forecast5
    WEATHER_CELSIUS: if this environment variable is present with any value,
                     the plugin will report temperatures in celsius instead of
                     farenheit
"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import json
import os
import re
from datetime import datetime
from itertools import groupby

import requests

# https://openweathermap.org/weather-conditions
ICONMAP = {
    "01d": ":sunny:",
    "01n": ":moon:",
    "02d": ":sun_behind_cloud:",
    "02n": ":sun_behind_cloud:",
    "03d": ":cloud:",
    "03n": ":cloud:",
    "04d": ":cloud:",
    "04n": ":cloud:",
    "09d": ":rain_cloud:",
    "09n": ":rain_cloud:",
    "10d": ":sun_behind_rain_cloud:",
    "10n": ":sun_behind_rain_cloud:",
    "11d": ":thunder_cloud_and_rain:",
    "11n": ":thunder_cloud_and_rain:",
    "13d": ":snowflake:",
    "13n": ":snowflake:",
    "50d": ":fog:",
    "50n": ":fog:",
}
CELSIUS = "metric"
IMPERIAL = "imperial"

MAPBOX_API_TOKEN = os.environ.get("MAPBOX_API_TOKEN")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")


def weather(searchterm):
    """Get the weather for a place given by searchterm

    Returns a title and a list of forecasts.

    The title describes the location for the forecast (i.e. "Portland, ME USA")
    The list of forecasts is a list of dictionaries in slack attachment fields
        format (see https://api.slack.com/docs/message-attachments)
    """
    unit = CELSIUS if os.environ.get("WEATHER_CELSIUS") else IMPERIAL

    geo = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?limit=1&access_token={}".format(
            quote(searchterm.encode("utf8")), MAPBOX_API_TOKEN
        )
    ).json()
    citystate = geo["features"][0]["place_name"]
    lon, lat = geo["features"][0]["center"]

    forecast = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast?lat={:.2f}&lon={:.2f}&units={}&appid={}".format(
            lat, lon, unit, OPENWEATHER_API_KEY
        )
    ).json()

    if forecast["cod"] != "200":
        raise KeyError("Invalid OpenWeatherMap key")

    title = "Weather for {}: ".format(citystate)

    # relies on the forecast list being sorted
    days = groupby(forecast["list"], lambda i: i["dt_txt"].split(" ")[0])
    messages = []
    for dt, forecasts in days:
        dayname = datetime.strptime("2020-04-07", "%Y-%m-%d").strftime("%A")
        high = max(
            (int(round(cast["main"]["temp_max"])), cast["weather"][0]["icon"])
            for cast in forecasts
        )
        icon = ICONMAP.get(high[1], ":question:")
        unit_abbrev = "f" if unit == IMPERIAL else "c"

        messages.append(
            {
                "title": dayname,
                "value": u"{} {}°{}".format(icon, high[0], unit_abbrev),
                "short": True,
            }
        )

    return title, messages[:4]


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!weather (.*)", text)
    if not match:
        return

    try:
        title, forecasts = weather(match[0])
    except KeyError as err:
        return "KeyError: {}".format(err.args[0])

    attachment = {"fallback": title, "pretext": title, "fields": forecasts[0:4]}
    server.slack.post_message(
        msg["channel"],
        "",
        as_user=server.slack.username,
        attachments=json.dumps([attachment]),
    )


on_bot_message = on_message
