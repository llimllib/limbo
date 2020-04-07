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

    today = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat={:.2f}&lon={:.2f}&units={}&appid={}".format(
            lat, lon, unit, OPENWEATHER_API_KEY
        )
    ).json()
    forecast = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast?lat={:.2f}&lon={:.2f}&units={}&appid={}".format(
            lat, lon, unit, OPENWEATHER_API_KEY
        )
    ).json()

    title = "Weather for {}: ".format(citystate)

    # offset in seconds
    utc_offset = today["timezone"]
    current_time = datetime.fromtimestamp(today["dt"] + utc_offset)

    forecasts = [parse_forecast(today, current_time, unit)]

    for event in forecast["list"]:
        event_time = datetime.fromtimestamp(event["dt"] + utc_offset)
        hour = event_time.strftime("%H")
        # not today and is 3-hour forecast > 11am and <= 2pm
        if (
            current_time.strftime("%d") != event_time.strftime("%d")
            and hour > "11"
            and hour <= "14"
        ):
            forecasts.append(parse_forecast(event, event_time, unit))

    return title, forecasts[0:4]


def parse_forecast(event, time, unit):
    day_of_wk = time.strftime("%A")
    icon = ICONMAP.get(event["weather"][0]["icon"], ":question:")
    unit_abbrev = "f" if unit == IMPERIAL else "c"
    return {
        "title": day_of_wk,
        "value": u"{} {}°{}".format(
            icon, int(round(event["main"]["temp"])), unit_abbrev
        ),
        "short": True,
    }


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
