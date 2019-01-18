# -*- coding: utf-8 -*-
"""!weather <zip or place name> return the 5-day forecast

Three environment variables control the behavior of this plugin:
    MAPBOX_API_TOKEN: must be set to a valid Mapbox API token https://docs.mapbox.com/api/search/#geocoding
    DARKSKY_API_KEY: must be set to a valid Dark Sky API key https://darksky.net/dev/docs#data-point-object
    WEATHER_CELSIUS: if this environment variable is present with any value, the plugin will report
                     temperatures in celsius instead of farenheit
"""

try:
    from urllib import quote
except ImportError:
    from urllib.request import quote
import json
import os
import re
from datetime import datetime

import requests

# https://darksky.net/dev/docs#data-point-object
ICONMAP = {
    "clear-day": ":sunny:",
    "clear-night": ":moon:",
    "rain": ":rain_cloud:",
    "snow": ":snowflake:",
    "sleet": ":snow_cloud:",
    "wind": ":wind_blowing_face:",
    "fog": ":fog:",
    "cloudy": ":cloud:",
    "partly-cloudy-day": ":sun_behind_cloud:",
    "partly-cloudy-night": ":sun_behind_cloud:",
    "thunderstorm": ":thunder_cloud_and_rain:",
    "tornado": ":tornado:",
}

MAPBOX_API_TOKEN = os.environ.get("MAPBOX_API_TOKEN")
DARKSKY_API_KEY = os.environ.get("DARKSKY_API_KEY")


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
    unit = "si" if os.environ.get("WEATHER_CELSIUS") else "us"

    geo = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/{}.json?limit=1&access_token={}".format(
            quote(searchterm), MAPBOX_API_TOKEN
        )
    ).json()
    citystate = geo["features"][0]["place_name"]
    lon, lat = geo["features"][0]["center"]
    forecast = requests.get(
        "https://api.darksky.net/forecast/{}/{},{}?unit={}".format(
            DARKSKY_API_KEY, lat, lon, unit
        )
    ).json()

    title = "Weather for {}: ".format(citystate)

    forecasts = []
    unit_abbrev = "f" if unit == "us" else "c"
    for day in forecast["daily"]["data"][0:4]:
        day_of_wk = datetime.fromtimestamp(day["time"]).strftime("%A")
        icon = ICONMAP.get(day["icon"], ":question:")
        forecasts.append(
            {
                "title": day_of_wk,
                "value": u"{} {}°{}".format(
                    icon, round(day["temperatureHigh"]), unit_abbrev
                ),
                "short": True,
            }
        )

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

    attachment = {"fallback": title, "pretext": title, "fields": forecasts[0:4]}
    server.slack.post_message(
        msg["channel"],
        "",
        as_user=server.slack.username,
        attachments=json.dumps([attachment]),
    )


on_bot_message = on_message
